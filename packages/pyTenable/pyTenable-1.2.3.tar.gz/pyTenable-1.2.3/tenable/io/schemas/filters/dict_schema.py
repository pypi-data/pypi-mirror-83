from .base import BaseFilterRuleSchema
from marshmallow import post_load


class DictFilterSchema(BaseFilterRuleSchema):
    '''
    The Tenable.io API Version 1 filter format schema.

    This schema will output the data in the format typically seen from the
    Tenable.io API.  It's a serialized using the following format:

    .. code-block:: javascript

        {
            "filters": [
                {
                    "filter": "FILTER_NAME",
                    "quality": "FILTER_OPERATOR",
                    "value": "FILTER_VALUE"
                }
            ]
        }

    This format is then typically passed into the query arguments of a GET call.
    '''
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
        return {'filters': rules}

    def reformat_filter(self, rule, idx=0):
        '''
        Converts the basic filter rule format into the v1 (dict) format.
        '''
        return {
            'filter': rule['name'],
            'quality': rule['oper'],
            'value': rule['value']
        }