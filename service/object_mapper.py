import json

class ObjectMapper:
    @classmethod
    def map(cls, json_data, target_class):
        instance = target_class()

        for field_name, field_type in cls.get_fields(target_class):
            if field_name not in json_data:
                raise ValueError(f"Field '{field_name}' is missing in the JSON data.")

            value = json_data[field_name]
            if value is None and field_type is not type(None):
                raise ValueError(f"Field '{field_name}' is marked as non-nullable but is set to None.")

            setattr(instance, field_name, value)

        return instance

    @staticmethod
    def get_fields(target_class):
        return [(name, type_) for name, type_ in target_class.__annotations__.items()]
