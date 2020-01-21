# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

json_edge = {
    'color': {
        'color': '#d7ffaf'
    },
    'title': 'JSON Parsing Functions',
    'label': 'JSON'
}


def run(unfurl, node):

    if node.data_type == 'url.query.pair':
        try:
            json_obj = json.loads(node.value)
            assert isinstance(json_obj, dict), 'Loaded object should be a dict'

        except json.JSONDecodeError:
            return

        except AssertionError:
            # Likely a "valid" JSON of 23 or 1 or some single value; not what we want
            return

        try:

            for json_key, json_value in json_obj.items():
                unfurl.add_to_queue(
                    data_type='json', key=json_key, value=json_value, label=f'{json_key}: {json_value}',
                    hover='This is the URL <b>network location</b> (or netloc), per <a href="'
                          'https://tools.ietf.org/html/rfc1808.html" target="_blank">RFC1808</a>',
                    parent_id=node.node_id, incoming_edge_config=json_edge)

        except Exception as e:
            print(f'Exception parsing JSON string: {e}')

    elif node.data_type == 'json':
        node_value = node.value
        if isinstance(node_value, str):
            try:
                node_value = json.loads(node_value)
            except json.JSONDecodeError as jde:
                pass
        if isinstance(node_value, dict):
            try:
                for key, value in node_value.items():
                    unfurl.add_to_queue(
                        data_type='json', key=key, value=value, label=f'{key}: {value}',
                        hover='This is the URL <b>network location</b> (or netloc), per <a href="'
                              'https://tools.ietf.org/html/rfc1808.html" target="_blank">RFC1808</a>',
                        parent_id=node.node_id, incoming_edge_config=json_edge)

            except Exception as e:
                print(f'Exception parsing JSON: {e}')
