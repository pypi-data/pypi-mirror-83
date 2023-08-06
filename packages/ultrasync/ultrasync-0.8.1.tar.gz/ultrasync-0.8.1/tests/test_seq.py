# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Chris Caron <lead2gold@gmail.com>
# All rights reserved.
#
# This code is licensed under the MIT License.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions :
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import mock
import requests
from os.path import join
from os.path import dirname

from ultrasync import UltraSync

# Disable logging for a cleaner testing output
import logging
logging.disable(logging.CRITICAL)

# Reference Directory
TEST_VAR_DIR = join(dirname(__file__), 'var')


@mock.patch('requests.Session.post')
def test_sequence(mock_post):
    """
    test sequence

    """

    # A response object
    robj = mock.Mock()

    # Simulate a valid login return
    with open(join(TEST_VAR_DIR, 'seq.json-okay'), 'rb') as f:
        robj.content = f.read()
    robj.status_code = requests.codes.ok

    # Assign our response object to our mocked instance of requests
    mock_post.return_value = robj

    uobj = UltraSync()
    # Force valid authentication (for testing purposes)
    uobj._authenticated = True
    uobj.session_id = 'ABCD1234'

    response = uobj._sequence()
    assert isinstance(response, dict)
    # Response should look like so:
    # {
    #   'time': '2019-11-28 22:29:06',
    #   'area': [226, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #   'zone': [24, 0, 2, 57, 8, 38, 0, 0, 0, 10, 83, 36, 0, 0, 0, 0, 16, 0],
    #   'chime': [3, 0, 0, 0],
    #   'config': 25505,
    #   'zwdevice': 50398,
    # }
    assert response['time'] == '2019-11-28 22:29:06'
    assert response['area'] == [226, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert response['zone'] == \
        [24, 0, 2, 57, 8, 38, 0, 0, 0, 10, 83, 36, 0, 0, 0, 0, 16, 0]
    assert response['chime'] == [3, 0, 0, 0]
    assert response['config'] == 25505
    assert response['zwdevice'] == 50398
