import typing


class ObjectMapper:
    @classmethod
    def map(cls, data, target_class):
        instance = target_class()
        if isinstance(data, dict):
            cls.map_from_dict(data, target_class, instance)
        else:
            cls.map_from_instance(data, target_class, instance)

        return instance

    @classmethod
    def map_from_dict(cls, json_data, target_class, instance):
        for field_name, field_type in cls.get_fields(target_class):
            if field_name not in json_data and field_type is not typing.Union[str, type(None)]:
                raise ValueError(f"Field '{field_name}' is missing in the JSON data.")

            value = json_data.get(field_name, None)
            if value is None and field_type is not typing.Union[str, type(None)]:
                raise ValueError(f"Field '{field_name}' is marked as non-nullable but is set to None.")
            setattr(instance, field_name, value)

    @classmethod
    def map_from_instance(cls, source_instance, target_class, instance):
        for field_name, field_type in cls.get_fields(target_class):
            if not hasattr(source_instance, field_name) and field_type is not type(None):
                raise ValueError(f"Field '{field_name}' is missing in the source instance.")

            value = getattr(source_instance, field_name, None)
            if value is None and field_type is not type(None):
                raise ValueError(f"Field '{field_name}' is marked as non-nullable but is set to None.")

            setattr(instance, field_name, value)

    @staticmethod
    def get_fields(target_class):
        return [(name, type_) for name, type_ in target_class.__annotations__.items()]
