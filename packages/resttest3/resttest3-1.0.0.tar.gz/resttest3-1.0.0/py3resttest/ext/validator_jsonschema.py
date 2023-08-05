import json
import traceback

import jsonschema
import yaml

from py3resttest.contenthandling import ContentHandler
from py3resttest.utils import Parser
from py3resttest.validators import AbstractValidator, Failure
from py3resttest.constants import FAILURE_VALIDATOR_EXCEPTION


class JsonSchemaValidator(AbstractValidator):
    """ Json schema validator using the jsonschema library """
    schema = None

    def validate(self, body=None, headers=None, context=None):
        schema_text = self.schema.get_content(context=context)
        schema = yaml.safe_load(schema_text)

        try:
            if isinstance(body, bytes):
                body = body.decode()
            jsonschema.validate(json.loads(body), schema)
            return True
        except jsonschema.exceptions.ValidationError:
            trace = traceback.format_exc()
            return Failure(message="JSON Schema Validation Failed", details=trace, validator=self,
                           failure_type=FAILURE_VALIDATOR_EXCEPTION)

    def get_readable_config(self, context=None):
        return "JSON schema validation"

    @classmethod
    def parse(cls, config):
        validator = JsonSchemaValidator()
        config = Parser.lowercase_keys(config)
        if 'schema' not in config:
            raise ValueError(
                "Cannot create schema validator without a 'schema' configuration element!")
        validator.schema = ContentHandler.parse_content(config[
                                                            'schema'])
        return validator


VALIDATORS = {'json_schema': JsonSchemaValidator.parse}
