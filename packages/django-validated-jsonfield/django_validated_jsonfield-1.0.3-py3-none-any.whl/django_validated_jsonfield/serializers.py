import copy

from jsonschema_to_openapi.convert import convert as convert_to_openapi
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .fields import ValidatedJSONField as ModelValidatedJSONField


class ValidatedJSONField(serializers.JSONField):
    def __init__(self, *args, initial=None, validators=[], **kwargs):
        self.schema = kwargs.pop("schema")
        self.coreapi_schema = convert_to_openapi(copy.deepcopy(self.schema) )
        self.json_validator_cls = kwargs.pop("json_validator_cls")

        #MIXING validators among multiple ModelValidatedJSONField, we should try not to use the validators argument
        def json_validator(value):
            if(self.json_validator_cls):
                errors = [ValidationError({str(error.path):error.message}) for error in self.json_validator_cls.iter_errors(value)]
                if(errors):
                    raise ValidationError(errors)

        self.validators =list([json_validator]+validators)

        super().__init__(*args, **kwargs)





class ValidatedJsonModelSerializerMixin(serializers.ModelSerializer):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.serializer_field_mapping[ModelValidatedJSONField] = ValidatedJSONField

    def build_standard_field(self, field_name, model_field):
        field_class, kwargs =  super().build_standard_field(field_name, model_field)

        if isinstance(model_field, ModelValidatedJSONField):
            kwargs['schema'] = model_field.schema
            kwargs['json_validator_cls'] = model_field.json_validator_cls

        return field_class, kwargs
