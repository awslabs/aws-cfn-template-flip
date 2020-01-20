"""
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import collections


class OdictItems(list):
    """
    Helper class to ensure ordering is preserved
    """

    def __init__(self, items):
        new_items = []

        for item in items:
            class C(type(item)):
                def __lt__(self, *args, **kwargs):
                    return False

            new_items.append(C(item))

        return super(OdictItems, self).__init__(new_items)

    def sort(self):
        pass


class ODict(collections.OrderedDict):
    """
    A wrapper for OrderedDict that doesn't allow sorting of keys
    """

    def __init__(self, pairs=[]):
        if isinstance(pairs, dict):
            # Dicts lose ordering in python<3.6 so disallow them
            raise Exception("ODict does not allow construction from a dict")

        super(ODict, self).__init__(pairs)

    def items(self):
        old_items = super(ODict, self).items()
        return OdictItems(old_items)
