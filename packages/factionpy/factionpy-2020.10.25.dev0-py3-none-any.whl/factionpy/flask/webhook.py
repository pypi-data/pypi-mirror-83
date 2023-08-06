import datetime
import json
import uuid
from dateutil.parser import parse

from typing import Dict

'''{
  "event": {
      "session_variables": [
        "var1": "test1",
        "var2": "test2"
      ],
      "op": "<op-name>",
      "data": {
          "old": null
          "new": [
            "data1": "test1",
            "data2": "test2"
          ],
      }
  },
  "created_at": "<timestamp>",
  "id": "<uuid>",
  "trigger": {
      "name": "<name-of-trigger>"
  },
  "table":  {
      "schema": "<schema-name>",
      "name": "<table-name>"
  }
}'''

class HasuraRequest:
    id: str = None
    trigger_name: str = None
    table_name: str = None
    table_schema: str = None
    created_at: datetime = None
    operation: str = None
    session_variables: Dict[str, object] = None
    old_data: Dict[str, object] = None
    new_data: Dict[str, object] = None
    def __init__(self, body: str):
        j = json.loads(body)
        self.id = j['id']
        self.trigger_name = j['trigger']['name']
        self.table_name = j['table']['name']
        self.table_schema = j['table']['schema']
        self.created_at = parse(j['created_at'])
        self.operation = j['event']['op']
        self.session_variables = j['event']['session_variables']
        self.old_data = j['event']['data']['old']
        self.new_data = j['event']['data']['new']




def parse_hasura_request(content: str) -> HasuraRequest:
    j = json.loads(content)
    hasura_req =