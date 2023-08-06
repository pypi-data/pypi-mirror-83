from .base import BaseFilterRuleSchema
from marshmallow import fields, post_load, pre_load


class AccessGroupsFilterSchema(BaseFilterRuleSchema):
    '''
    The Tenable.io API Access Groups filter format schema.

    This schema will output the data in the format typically seen for the
    Tenable.io access groups API.  It's a serialized using the following format:

    .. code-block:: javascript

        {
            "rules": [
                {
                    "type": "FILTER_NAME",
                    "operator": "FILTER_OPERATOR",
                    "terms": ["FILTER_VALUE"]
                }
            ]
        }

    This format is then typically passed into the query arguments of a GET call.
    '''
    value = fields.List(fields.String())

    @pre_load
    def serialize_tuple(self, rule, **kwargs):
        '''
        Handles serializing the standardized tuple format into a dictionary that
        can then be validated and processed.
        '''
        super(AccessGroupsFilterSchema, self).serialize_tuple(rule, **kwargs)
        rule['oper'] = rule.get('operator', rule.get('oper'))
        rule['value'] = rule.get('terms', rule.get('value'))
        return rule

    @post_load(pass_many=True)
    def reformat_many_filters(self, data, **kwargs):
        '''
        Performs the conversion of 1 or many filter rules.
        '''
        rules = list()

        # if only a single filter was passed, then wrap it in a list as we will
        # be using the index of the list.
        if not kwargs.get('many'):
            data = [data]

        # process each rule and then append the results into the rules list.
        for idx, rule in enumerate(data):
            rules.append(self.reformat_filter(rule, idx=idx))

        # return the rules dict back to the caller.
        return {'rules': rules}

    def reformat_filter(self, rule, idx=0):
        '''
        Converts the basic filter rule format into the Nessus format.
        '''
        return {
            'name': rule['name'],
            'operator': rule['oper'],
            'terms': rule['value']
        }