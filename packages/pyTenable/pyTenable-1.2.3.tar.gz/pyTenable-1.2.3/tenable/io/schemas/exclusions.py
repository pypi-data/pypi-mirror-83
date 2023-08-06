from .schedules import ScheduleSchema
from marshmallow import Schema, fields, pre_load

class ExclusionSchema(Schema):
    name = fields.String()
    members = fields.List(fields.String())
    description = fields.String()
    schedule = fields.Nested(ScheduleSchema)
    enabled = fields.Boolean()

    @pre_load
    def pass_unknowns_to_schedule(self, data, **kwargs):
        '''
        Convert any fields that aren't in the known defined fields listed above
        into schedule fields.
        '''
        data['schedule'] = data.get('schedule', dict())
        for k in data.keys():
            if k not in ['name', 'members', 'description', 'schedule']:
                data['schedule'][k] = data.pop(k)
        return data


class ExclusionCreateSchema(ExclusionSchema):
    name = fields.String(required=True)
    members = fields.List(fields.String(), required=True)
    enabled = fields.Boolean(default=True)