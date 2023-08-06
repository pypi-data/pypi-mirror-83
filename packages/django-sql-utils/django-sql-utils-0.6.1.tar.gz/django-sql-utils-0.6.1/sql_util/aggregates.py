from django.core.exceptions import FieldError
from django.db.models import Q, F, QuerySet, BooleanField, Sum, Avg
from django.db.models import Subquery as DjangoSubquery, OuterRef, IntegerField, Min, Max, Count
from django.db.models.constants import LOOKUP_SEP


class Subquery(DjangoSubquery):
    def __init__(self, queryset_or_expression, **extra):
        if isinstance(queryset_or_expression, QuerySet):
            self.queryset = queryset_or_expression
            self.query = self.queryset.query
            super(Subquery, self).__init__(queryset_or_expression, **extra)
        else:
            expression = queryset_or_expression
            if not hasattr(expression, 'resolve_expression'):
                expression = F(expression)
            self.expression = expression
            self.query = None
            self.queryset = None
            self.output_field = extra.get('output_field')
            self.extra = extra
            self.filter = extra.pop('filter', Q())
            self.distinct = extra.pop('distinct', None)
            self.outer_ref = extra.pop('outer_ref', None)
            self.unordered = extra.pop('unordered', self.unordered)

    def resolve_expression(self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False):
        # The parent class, Subquery, takes queryset as an initialization parameter
        # so self.queryset needs to be set before we call `resolve_expression`.
        # We can set it here because we now have access to the outer query object,
        # which is the first parameter of this method.
        if self.query is None or self.queryset is None:
            queryset = self.get_queryset(query.clone(), allow_joins, reuse, summarize)
            self.queryset = queryset
            self.query = queryset.query
        return super(Subquery, self).resolve_expression(query, allow_joins, reuse, summarize, for_save)

    def get_queryset(self, query, allow_joins, reuse, summarize):
        # This is a customization hook for child classes to override the base queryset computed automatically
        return self._get_base_queryset(query, allow_joins, reuse, summarize)

    def _get_base_queryset(self, query, allow_joins, reuse, summarize):
        resolved_expression = self.expression.resolve_expression(query, allow_joins, reuse, summarize)
        model = self._get_model_from_resolved_expression(resolved_expression)

        reverse, outer_ref = self._get_reverse_outer_ref_from_expression(model, query)

        outer_ref = self.outer_ref or outer_ref
        q = self.filter & Q(**{reverse: OuterRef(outer_ref)})
        queryset = model._default_manager.filter(q)
        if self.unordered:
            queryset = queryset.order_by()
        return queryset.values(reverse)

    def _get_model_from_resolved_expression(self, resolved_expression):
        """
        Retrieve the correct model from the resolved_expression.

        For simple expressions like F('child__field_name'), both of these are equivalent and correct:
        resolved_expression.field.model
        resolved_expression.target.model

        For many to many relations, resolved_expression.field.model goes one table deeper than
        necessary. We get more efficient SQL only going as far as we need. In this case only
        resolved_expression.target.model is correct.

        For functions of multiple columns like Coalesce, there is no resolved_expression.target,
        we have to recursively go through the source_expressions until we get to the bottom and
        get the target from there.
        """
        def get_target(res_expr):
            for expression in res_expr.get_source_expressions():
                return get_target(expression)
            return res_expr.field if res_expr.target.null else res_expr.target
        return get_target(resolved_expression).model

    def _get_fields_model_from_path(self, path, model, target_model):
        fields = []

        # We want the paths reversed because we have the forward join info
        # and we need the string that tells us how to go back
        paths = list(reversed(path))
        for p in paths:
            if p.to_opts.model == model and ((p.from_opts.model != target_model or p.m2m) or not fields):
                if getattr(p.join_field, 'related_query_name'):
                    try:
                        fields.append(p.join_field.related_query_name())
                    except TypeError:  # Sometimes related_query_name is a string instead of a callable that returns a string
                        fields.append(p.join_field.related_query_name)
                elif hasattr(p.join_field, 'field'):
                    fields.append(p.join_field.field.name)
                model = p.from_opts.model

        return fields, model

    def _get_reverse_outer_ref_from_expression(self, model, query):
        source = self.expression
        while hasattr(source, 'get_source_expressions'):
            source = source.get_source_expressions()[0]
        field_list = source.name.split(LOOKUP_SEP)
        path, _, _, _ = query.names_to_path(field_list, query.get_meta(), allow_many=True, fail_on_missing=True)

        fields, model = self._get_fields_model_from_path(path, model, query.model)
        reverse = LOOKUP_SEP.join(fields)

        join_field = path[0].join_field
        if model == query.model or len(path) == 1:
            try:
                outer_ref = join_field.get_related_field().name
            except AttributeError:
                outer_ref = 'pk'
        else:
            outer_ref = join_field.name

        return reverse, outer_ref


class SubqueryAggregate(Subquery):
    """
    The intention of this class is to provide an API similar to other aggregate
    classes like Count, Min, Max, Sum, etc but generate SQL that performs the
    calculation in a subquery instead of adding joins to the outer query. This
    is commonly a performance improvement. It also reduces the risk of
    forgetting to add `distinct` when the joins duplicate data.

    E.g.,
    queryset.annotate(min_field=Min('field'))

    is replaced by

    queryset.annotate(min_field=SubqueryAggregate('field', aggregate=Min))

    A child class of SubqueryAggregate with `aggregate=Min` allows:

    queryset.annotate(min_field=SubqueryMin('field'))

    """
    aggregate = None  # Must be set by the subclass, or passed as kwarg
    unordered = None

    def __init__(self, *args, **extra):
        self.aggregate = extra.pop('aggregate', self.aggregate)
        self.ordering = extra.pop('ordering', None)
        assert self.aggregate is not None, "Error: Attempt to instantiate a " \
                                           "SubqueryAggregate with no aggregate function"
        super(SubqueryAggregate, self).__init__(*args, **extra)

    def get_queryset(self, query, allow_joins, reuse, summarize):
        queryset = self._get_base_queryset(query, allow_joins, reuse, summarize)
        annotation = self._get_annotation(query, allow_joins, reuse, summarize)
        return queryset.annotate(**annotation).values('aggregation')

    def aggregate_kwargs(self):
        if self.distinct:
            return {'distinct': self.distinct}
        else:
            return dict()

    def _get_annotation(self, query, allow_joins, reuse, summarize):
        resolved_expression = self.expression.resolve_expression(query, allow_joins, reuse, summarize)
        model = self._get_model_from_resolved_expression(resolved_expression)
        queryset = model._default_manager.all()
        # resolved_expression was resolved in the outer query to get the model
        # target_expression is resolved in the subquery to get the field to aggregate
        target_expression = self._resolve_to_target(resolved_expression, queryset.query, allow_joins, reuse,
                                                    summarize)

        # Add test for output_field, distinct, and when resolved_expression.field.name isn't what we're aggregating

        if not self.output_field:
            self._output_field = self.output_field = target_expression.field

        kwargs = self.aggregate_kwargs()

        aggregation = self.aggregate(target_expression, **kwargs)

        annotation = {
            'aggregation': aggregation
        }

        return annotation

    def _resolve_to_target(self, resolved_expression, query, allow_joins, reuse, summarize):
        if resolved_expression.get_source_expressions():
            c = resolved_expression.copy()
            c.is_summary = summarize
            new_source_expressions = [self._resolve_to_target(source_expressions, query, allow_joins, reuse, summarize)
                                      for source_expressions in resolved_expression.get_source_expressions()]
            c.set_source_expressions(new_source_expressions)
            return c

        else:
            try:
                return F(resolved_expression.target.name).resolve_expression(query, allow_joins, reuse, summarize)
            except (FieldError, AttributeError):
                return resolved_expression


class SubqueryCount(SubqueryAggregate):
    template = 'COALESCE((%(subquery)s), 0)'
    aggregate = Count
    unordered = True

    def __init__(self, expression, reverse='', *args, **kwargs):
        kwargs['output_field'] = kwargs.get('output_field', IntegerField())
        super(SubqueryCount, self).__init__(expression, reverse=reverse, *args, **kwargs)


class SubqueryMin(SubqueryAggregate):
    aggregate = Min
    unordered = True


class SubqueryMax(SubqueryAggregate):
    aggregate = Max
    unordered = True


class SubquerySum(SubqueryAggregate):
    aggregate = Sum
    unordered = True


class SubqueryAvg(SubqueryAggregate):
    aggregate = Avg
    unordered = True


class Exists(Subquery):
    unordered = True
    template = 'EXISTS(%(subquery)s)'

    def __init__(self, *args, **kwargs):
        self.negated = kwargs.pop('negated', False)
        super(Exists, self).__init__(*args, **kwargs)
        self.output_field = BooleanField()

    def __invert__(self):
        # Be careful not to evaluate self.queryset on this line
        return type(self)(self.queryset if self.queryset is not None else self.expression, negated=(not self.negated), **self.extra)

    def as_sql(self, compiler, connection, template=None, **extra_context):
        sql, params = super(Exists, self).as_sql(compiler, connection, template, **extra_context)
        if self.negated:
            sql = 'NOT {}'.format(sql)
        return sql, params

    def as_oracle(self, compiler, connection, template=None, **extra_context):
        # Oracle doesn't allow EXISTS() in the SELECT list, so wrap it with a
        # CASE WHEN expression. Change the template since the When expression
        # requires a left hand side (column) to compare against.
        sql, params = self.as_sql(compiler, connection, template, **extra_context)
        sql = 'CASE WHEN {} THEN 1 ELSE 0 END'.format(sql)
        return sql, params

    def get_queryset(self, query, allow_joins, reuse, summarize):
        return self._get_base_queryset(query, allow_joins, reuse, summarize)
