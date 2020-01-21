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

import urllib.parse
import re

urlparse_edge = {
    'color': {
        'color': '#4d4d4d'
    },
    'title': 'URL Parsing Functions',
    'label': 'u'
}


def run(unfurl, node):

    if node.data_type == 'url':
        parsed_url = urllib.parse.urlparse(node.value)

        if parsed_url.netloc:
            if parsed_url.scheme:
                unfurl.add_to_queue(
                    data_type='url.scheme', key='Scheme', value=parsed_url.scheme,
                    hover='This is the URL <b>scheme</b>, per <a href="'
                          'https://tools.ietf.org/html/rfc3986" target="_blank">RFC3986</a>',
                    parent_id=node.node_id, incoming_edge_config=urlparse_edge)

            if parsed_url.netloc == parsed_url.hostname:
                unfurl.add_to_queue(
                    data_type='url.hostname', key=None, value=parsed_url.hostname,
                    hover='This is the <b>host</b> subcomponent of authority (also often called '
                          'netloc), per <a href="https://tools.ietf.org/html/rfc3986" target="_blank">RFC3986</a>',
                    parent_id=node.node_id, incoming_edge_config=urlparse_edge)
            else:
                unfurl.add_to_queue(
                    data_type='url.authority', key=None, value=parsed_url.netloc,
                    hover='This is the <b>authority</b> (also often called '
                          'netloc), per <a href="https://tools.ietf.org/html/rfc3986" target="_blank">RFC3986</a>',
                    parent_id=node.node_id, incoming_edge_config=urlparse_edge)

            if parsed_url.path:
                unfurl.add_to_queue(
                    data_type='url.path', key=None, value=parsed_url.path,
                    hover='This is the URL <b>path</b>, per <a href="'
                          'https://tools.ietf.org/html/rfc3986" target="_blank">RFC3986</a>',
                    parent_id=node.node_id, incoming_edge_config=urlparse_edge)

            if parsed_url.query:
                unfurl.add_to_queue(
                    data_type='url.query', key=None, value=parsed_url.query,
                    hover='This is the URL <b>query</b>, per <a href="'
                          'https://tools.ietf.org/html/rfc3986" target="_blank">RFC3986</a>',
                    parent_id=node.node_id, incoming_edge_config=urlparse_edge,
                    extra_options={'widthConstraint': {'maximum': 500}})

            if parsed_url.fragment:
                unfurl.add_to_queue(
                    data_type='url.fragment', key=None, value=parsed_url.fragment,
                    hover='This is the URL <b>fragment</b>, per <a href="'
                          'https://tools.ietf.org/html/rfc3986" target="_blank">RFC3986</a>',
                    parent_id=node.node_id, incoming_edge_config=urlparse_edge)

    elif node.data_type == 'url.path':
        path_segments = node.value.split('/')
        if len(path_segments) > 2:
            for segment_number, path_segment in enumerate(path_segments):
                if path_segment != '':
                    unfurl.add_to_queue(
                        data_type='url.path.segment', key=segment_number, value=path_segment,
                        hover='This is a URL <b>path segment</b> (the URL path is split on "/"s). '
                              'Numbering starts at 1.', parent_id=node.node_id, incoming_edge_config=urlparse_edge)

    elif node.data_type == 'url.query' or node.data_type == 'url.fragment':
        parsed_qs = urllib.parse.parse_qs(node.value)
        for key, value in parsed_qs.items():
            assert type(value) is list, 'parsed_qs should result in type list, but did not.'
            # In the majority of cases, query string keys are unique, but the spec is ambiguous. In the case of
            # duplicate keys, urllib.parse.parsed_qs adds them to a list. Unfurl will loop over and create a
            # node for each value in that list of values (this is typically only one value, but could be more).
            for v in value:
                unfurl.add_to_queue(
                    data_type='url.query.pair', key=key, value=v, label=f'{key}: {v}',
                    parent_id=node.node_id, incoming_edge_config=urlparse_edge)

    # This should only occur when a URL node was parsed previously and netloc != hostname, which means there are
    # additional subcomponents of the authority to parse: user, password, and/or port. Reparsing this way lets the
    # simple case of authority = hostname look uncluttered, but still support all the other subcomponents if given.
    elif node.data_type == 'url.authority':
        # We need to add in a fake scheme here, as we stripped in the previous run and urlparse needs one.
        parsed_authority = urllib.parse.urlparse(f'https://{node.value}')

        if parsed_authority.username:
            unfurl.add_to_queue(
                data_type='url.username', key='Username', value=parsed_authority.username,
                hover='This is the <b>username</b> subcomponent of authority, '
                      'per <a href="https://tools.ietf.org/html/rfc3986" target="_blank">RFC3986</a>',
                parent_id=node.node_id, incoming_edge_config=urlparse_edge)

        if parsed_authority.password:
            unfurl.add_to_queue(
                data_type='url.password', key='Password', value=parsed_authority.password,
                hover='This is the <b>password</b> subcomponent of authority, '
                      'per <a href="https://tools.ietf.org/html/rfc3986" '
                      'target="_blank">RFC3986</a>',
                parent_id=node.node_id, incoming_edge_config=urlparse_edge)

        unfurl.add_to_queue(
            data_type='url.hostname', key='Host', value=parsed_authority.hostname,
            hover='This is the <b>host</b> subcomponent of authority (also often called '
                  'netloc), per <a href="https://tools.ietf.org/html/rfc3986" target="_blank">RFC3986</a>',
            parent_id=node.node_id, incoming_edge_config=urlparse_edge)

        if parsed_authority.port:
            unfurl.add_to_queue(
                data_type='url.port', key='Port', value=parsed_authority.port,
                hover='This is the <b>port</b> subcomponent of authority, '
                      'per <a href="https://tools.ietf.org/html/rfc3986" target="_blank">RFC3986</a>',
                parent_id=node.node_id, incoming_edge_config=urlparse_edge)

    else:
        if not isinstance(node.value, str):
            return

        try:
            # If we can recognize another URL inside a value, parse it
            parsed_url = urllib.parse.urlparse(node.value)
            if parsed_url.netloc and parsed_url.path:
                unfurl.add_to_queue(
                    data_type='url', key=None, value=node.value, parent_id=node.node_id,
                    incoming_edge_config=urlparse_edge)
                return
        except:
            # Guess it wasn't a URL
            pass

        # If the value contains more pairs of the form "a=b|c=d|e=f"
        pipe_delimited_pairs_re = re.compile(
            r'((?P<key>[^|=]+)=(?P<value>[^|=]+)\|)+(?P<last_key>[^|=]+)=(?P<last_value>[^|=]+)')
        m = pipe_delimited_pairs_re.fullmatch(node.value)
        if m:
            pipe_pairs = node.value.split('|')
            for pair in pipe_pairs:
                key, value = pair.split('=')
                unfurl.add_to_queue(
                    data_type='url.query.pair', key=key, value=value,
                    parent_id=node.node_id, incoming_edge_config=urlparse_edge)
            return

        # If the value contains more pairs of the form "a=b&c=d&e=f"
        amp_delimited_pairs_re = re.compile(
            r'((?P<key>[^&=]+)=(?P<value>[^&=]+)&)+(?P<last_key>[^&=]+)=(?P<last_value>[^&=]+)')
        m = amp_delimited_pairs_re.fullmatch(node.value)
        if m:
            amp_pairs = node.value.split('&')
            for pair in amp_pairs:
                key, value = pair.split('=')
                unfurl.add_to_queue(
                    data_type='url.query.pair', key=key, value=value,
                    parent_id=node.node_id, incoming_edge_config=urlparse_edge)
            return
