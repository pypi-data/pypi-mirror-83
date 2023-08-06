from tenable.io.schemas.filters import ColonFilterSchema
from marshmallow import (
    Schema,
    fields,
    pre_load,
    post_load,
    validate as v,
    validates_schema,
    ValidationError,
)


class SortingSchema(Schema):
    field = fields.String()
    direction = fields.String()

    @pre_load
    def serialize_tuple(self, rule, **kwargs):
        if isinstance(rule, tuple):
            return {
                'field': rule[0],
                'direction': rule[1]
            }
        return rule


class PaginationSchemaV1(Schema):
    offset = fields.Integer()
    limit = fields.Integer()
    sort = fields.List(fields.Nested(SortingSchema))
    f = fields.List(fields.String())
    ft = fields.String(validate=v.OneOf(['and', 'or']))
    w = fields.String()
    wf = fields.List(fields.String())

    @pre_load
    def convert_inputs(self, data, **kwargs):
        '''
        Performs some simple conversion of the inputs to the expected field
        names used by the API.
        '''
        # the parameters that we will convert.  The API names are the first col,
        # whereas the more human-readable names documented in the library are
        # the second col.
        replacements = (
            ('ft', 'filter_type'),
            ('w', 'wildcard'),
            ('wf', 'wildcard_fields'),
        )
        for r in replacements:
            if data.get(r[1]):
                data[r[0]] = data.pop(r[1])

        # Perform the filter conversion and validation.  If a filterset was
        # provided as part of the input, then we will also pull that out and
        # pass it into the filter schema.
        filterset = data.pop('filterset', None)
        if data.get('filters'):
            filters = ColonFilterSchema()
            if filterset:
                filters.load_filters(filterset)
            f = filters.load(data.get('filters'))
            data['f'] = f['f']

        # return the transformed data back to the Schema.
        return data

    @post_load
    def reformat(self, data, **kwargs):
        if data.get('sort'):
            # convert the list of sort dictionaries into a single, comma-sep
            # string of sort definitions, which are field:direction formatted.
            data['sort'] = ','.join(
                ['{field}:{direction}'.format(**s) for s in data.get('sort')]
            )
        if data.get('wf'):
            data['wf'] = ','.join(data['wf'])
        return data
