from boto3.dynamodb.conditions import Key, ConditionExpressionBuilder
import re
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

ATTR_NAME_REGEX = re.compile(r'[^.\[\]]+(?![^\[]*\])')


class ClientBuilder(ConditionExpressionBuilder):
    def _build_value_placeholder(self, value, attribute_value_placeholders,
                                 has_grouped_values=False):
        # If the values are grouped, we need to add a placeholder for
        # each element inside of the actual value.
        serializer = TypeSerializer()
        if has_grouped_values:
            placeholder_list = []
            for v in value:
                value_placeholder = self._get_value_placeholder()
                self._value_count += 1
                placeholder_list.append(value_placeholder)
                attribute_value_plcaceholders[value_placeholder] = serializer.serialize(v)
            # Assuming the values are grouped by parenthesis.
            # IN is the currently the only one that uses this so it maybe
            # needed to be changed in future.
            return '(' + ', '.join(placeholder_list) + ')'
        # Otherwise, treat the value as a single value that needs only
        # one placeholder.
        else:
            value_placeholder = self._get_value_placeholder()
            self._value_count += 1
            attribute_value_placeholders[value_placeholder] = serializer.serialize(value)
            return value_placeholder


