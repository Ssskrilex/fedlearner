# Copyright 2020 The FedLearner Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# coding: utf-8
from string import Template
from flatten_dict import flatten
from fedlearner_webconsole.proto.workflow_definition_pb2 import Slot
class _YamlTemplate(Template):
    delimiter = '$'
    # Which placeholders in the template should be interpreted
    idpattern = r'Slot_[a-z0-9_]*'

def format_yaml(yaml, **kwargs):
    """Formats a yaml template.

    Example usage:
        format_yaml('{"abc": ${x.y}}', x={'y': 123})
    output should be  '{"abc": 123}'
    """
    template = _YamlTemplate(yaml)
    try:
        return template.substitute(flatten(kwargs or {},
                                           reducer='dot'))
    except KeyError as e:
        raise RuntimeError(
            'Unknown placeholder: {}'.format(e.args[0])) from e

def generate_yaml_template(base_yaml, slots_proto):
    """
    Parse certificates from base64-encoded string to a dict
    Args:
        base_yaml: A string representation of one type job's base yaml.
        slots_proto: A proto map object representation of modification template's
        operable smallest units.
    Returns:
        string: A yaml_template
    """
    slots = {}
    for key in slots_proto:
        if slots_proto[key].variable_type == Slot.VariableType.DEFAULT:
            slots[key] = slots_proto[key].default
        else:
            slots[key] = slots_proto[key].variable
    return format_yaml(base_yaml, **slots)
