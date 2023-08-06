from .base import BaseFilterRuleSchema
from marshmallow import post_load
from tenable.utils import dict_merge


class NessusFilterSchema(BaseFilterRuleSchema):
    '''
    The Nessus filter format schema.

    This schema will output the data in the format typically seen from the
    Nessus API.  It's a serialized using the following format:

    .. code-block:: javascript

        {
            "filter.INDEX.filter": "FILTER_NAME",
            "filter.INDEX.quality": "FILTER_OPERATOR",
            "filter.INDEX.value": "FILTER_VALUE"
        }

    This format is then typically passed into the query arguments of a GET call.
    '''
    @post_load(pass_many=True)
    def reformat_many_filters(self, data, **kwargs):
        '''
        Performs the conversion of 1 or many filter rules.
        '''
        rules = dict()

        # if only a single filter was passed, then wrap it in a list as we will
        # be using the index of the list.
        if not kwargs.get('many'):
            data = [data]

        # process each rule and then merge the results into the rules dict.
        for idx, rule in enumerate(data):
            rules = dict_merge(rules, self.reformat_filter(rule, idx=idx))

        # return the rules dict back to the caller.
        return rules

    def reformat_filter(self, rule, idx=0):
        '''
        Converts the basic filter rule format into the Nessus format.
        '''
        return {
            'filter.{idx:d}.filter'.format(idx=idx): rule['name'],
            'filter.{idx:d}.quality'.format(idx=idx): rule['oper'],
            'filter.{idx:d}.value'.format(idx=idx): rule['value']
        }