"""                                                                                                      
Copyright 2016-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                  
                                                                                                         
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at                                              
                                                                                                         
    http://aws.amazon.com/apache2.0/                                                                     
                                                                                                         
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.                                                 
"""

import cfn_flip
import collections
import yaml

def test_yaml_no_ordered_dict():
    """
    cfn-flip patches yaml to use OrderedDict by default
    Check that we don't do this for folks who import cfn_flip and yaml
    """

    yaml_string = "key: value"
    data = yaml.load(yaml_string)

    assert type(data) == dict

def test_yaml_no_ordered_dict_with_custom_loader():
    """
    cfn-flip patches yaml to use OrderedDict by default
    Check that we do this for normal cfn_flip use cases
    """

    yaml_string = "key: value"
    data = yaml.load(yaml_string, Loader=cfn_flip.CustomLoader)

    assert type(data) == collections.OrderedDict
