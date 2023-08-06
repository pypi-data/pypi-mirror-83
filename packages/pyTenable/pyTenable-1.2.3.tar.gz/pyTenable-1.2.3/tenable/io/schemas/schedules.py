from marshmallow import Schema, fields, pre_load, post_load, validate as v
from datetime import datetime


class RecurringRulesSchema(Schema):
    byweekday = fields.List(fields.String(
        validate=v.OneOf(['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'])))
    bymonthday = fields.Integer(validate=v.Range(1, 31))
    interval = fields.Integer(default=1)
    freq = fields.String(default='ONETIME',
        validate=v.OneOf(['ONETIME', 'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']))

    @pre_load
    def convert_inputs(self, data, **kwargs):
        if data.get('byweekday'):
            data['byweekday'] = [i.upper() for i in data.get('byweekday')]
        if data.get('freq'):
            data['freq'] = data.get('freq').upper()
        return data


class ScheduleSchema(Schema):
    enabled = fields.Boolean()
    starttime = fields.String(validate=v.Regexp('\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}'))
    endtime = fields.String(validate=v.Regexp('\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}'))
    timezone = fields.String(default='Etc/UTC')
    rrules = fields.Nested(RecurringRulesSchema)

    @pre_load
    def convert_inputs(self, data, **kwargs):
        # convert any rrules attributes into the rrules definitions.
        data['rrules'] = data.get('rrules', dict())
        rrules_defs = (
            ('freq', 'frequency'),
            ('interval', 'interval'),
            ('byweekday', 'weekdays'),
            ('bymonthday', 'day_of_month'),
        )
        for rr, f in rrules_defs:
            if data.get(f):
                data['rrules'][rr] = data.pop(f)

        for f in ['starttime', 'endtime']:
            if isinstance(data.get(f), (int, float)):
                data[f] = datetime.fromtimestamp(data.get(f))
            if isinstance(data.get(f), datetime):
                data[f] = data.get(f).strftime('%Y-%m-%d %H:%M:%S')
        return data