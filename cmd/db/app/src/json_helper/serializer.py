import json
class MessageSerializer:

    def __init__(self, deserialized):
        self.serialized_data: dict = dict()
        self.serialized_header: dict = dict()
        self.deserialized = deserialized
        parsed_json = json.loads(self.deserialized)
        self.serialized_header = parsed_json['headers']
        self.serialized_data = self.serialize_dict(parsed_json['data'])
        self.serialized = {'headers': self.serialized_header, 'data': self.serialized_data}


    def serialize_dict(self, input_dict):
        output_dict = dict()
        for key, value in input_dict.items():
            output_dict[key] = self.serialize_value(value)
        return output_dict

    @staticmethod
    def serialize_value(input_value):
        if input_value['type'] == 'int':
            return str(input_value['value'])
        if input_value['type'] == 'str':
            return f"'{input_value['value']}'"
        if input_value['type'] in ['list', 'tuple']:
            if not input_value.get('value'):
                val = ['']
            else:
                val = input_value.get('value')
            string = ', '.join(val)
            return "'{%s}'" % string


    def as_dict(self):
        return dict(self.serialized)