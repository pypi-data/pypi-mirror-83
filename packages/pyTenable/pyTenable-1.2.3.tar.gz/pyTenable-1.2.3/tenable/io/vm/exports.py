'''
Exports
=======

Methods described in this section relate to the the exports APIs
under the vm section.  These methods can be accessed at
``TenableIO.vm.exports``.

.. rst-class:: hide-signature
.. autoclass:: ExportsAPI
    :members:
'''
from tenable.utils import dict_merge
from tenable.base.endpoint import APIEndpoint
from tenable.io.iterators import Version1Iterator
from marshmallow import Schema, fields, pre_load, post_load, validate as v


class VulnExportVPRFilterSchema(Schema):
    eq = fields.List(fields.Number())
    neq = fields.List(fields.Number())
    gt = fields.Number()
    gte = fields.Number()
    lt = fields.Number()
    lte = fields.Number()


class VulnExportFiltersSchema(Schema):
    cidr_range = fields.String()
    first_found = fields.Integer()
    last_found = fields.Integer()
    last_fixed = fields.Integer()
    plugin_family = fields.List(fields.String())
    network_id = fields.String(
        validate=v.Regexp('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'))
    severity = fields.List(fields.String(
        validate=v.OneOf(['info', 'low', 'medium', 'high', 'critical'])))
    since = fields.Integer()
    state = fields.List(fields.String(
        validate=v.OneOf(['open', 'reopened', 'fixed'])))
    tags = fields.Dict(keys=fields.String(), values=fields.List(fields.String()))
    vpr_score = fields.Nested(VulnExportVPRFilterSchema)


class VulnExportSchema(Schema):
    num_assets = fields.Integer(validate=v.Range(min=50, max=5000))
    include_unlicensed = fields.Boolean()
    filters = fields.Nested(VulnExportFiltersSchema)