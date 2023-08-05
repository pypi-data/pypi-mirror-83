import json
import unittest
from typing import Any, Dict

from django_extensions import fields


class JSONFieldTests(unittest.TestCase):

    def test_to_python(self):
        json_field = fields.JSONField()
        self.assertIsNone(json_field.to_python(''))

        params: Dict[str, Any] = {
            'string': 'hello', 'integer': 13, 'dict': {'hey': 'yo'}
        }
        dic: Dict[str, Any] = json_field.to_python(json.dumps(params))
        self.assertDictEqual(params, dic)

    def test_from_db_value(self):
        inputs: str = json.dumps({'hey': 'yo'})
        json_field = fields.JSONField()
        self.assertDictEqual(
            json_field.to_python(inputs),
            json_field.from_db_value(inputs)
        )

    def test_get_db_prep_save(self):
        inputs: Dict[str, str] = {'hey': 'yo'}
        inputs_str: str = json.dumps(inputs)
        json_field = fields.JSONField()
        self.assertEqual(
            json_field.get_db_prep_save(inputs),
            inputs_str
        )
        self.assertIsNone(json_field.get_db_prep_save(''))
