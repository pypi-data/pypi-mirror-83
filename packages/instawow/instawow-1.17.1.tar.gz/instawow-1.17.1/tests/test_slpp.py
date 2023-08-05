# These tests are adapted from SLPP <https://github.com/SirAnthony/slpp>.
#
#   Copyright (c) 2010, 2011, 2012 SirAnthony <anthony at adsorbtion.org>
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#   THE SOFTWARE.

from instawow._custom_slpp import slpp


def test_numbers():
    # int and float
    assert slpp.decode('3') == 3
    assert slpp.decode('3.') == 3
    assert slpp.decode('3.1') == 3.1
    # negative float
    assert slpp.decode('-0.45') == -0.45
    # scientific
    assert slpp.decode('3e-07') == 3e-7
    assert slpp.decode('-3.23e+17') == -3.23e17
    # hex
    assert slpp.decode('0x3a') == 0x3A
    assert (
        slpp.decode(
            '''{
                ID = 0x74fa4cae,
                Version = 0x07c2,
                Manufacturer = 0x21544948
            }'''
        )
        == {'ID': 0x74FA4CAE, 'Version': 0x07C2, 'Manufacturer': 0x21544948}
    )


def test_bool():
    assert slpp.decode('true') == True
    assert slpp.decode('false') == False


def test_nil():
    slpp.decode('nil') == None


def test_singe_value_table():
    # bracketed string key
    assert slpp.decode('{ [10] = 1 }') == {10: 1}
    # keyword in table
    assert slpp.decode('{ true }') == [True]
    # void table
    assert slpp.decode('{ nil }') == {}
    # values-only table
    assert slpp.decode('{ "10" }') == ["10"]
    # last zero
    assert slpp.decode('{ 0, 1, 0 }') == [0, 1, 0]


def test_string_with_and_without_escape():
    assert slpp.decode("'test\\'s string'") == "test's string"
    assert slpp.decode('"test\\\'s string"') == "test\\'s string"
    assert slpp.decode('"test\'s string"') == "test's string"
    assert slpp.decode("[[test\\'s string]]") == "test\\'s string"
    assert slpp.decode("[[test's string]]") == "test's string"


def test_nested_table_with_variety_of_comments():
    assert slpp.decode(
        '''{ -- δκσξδφξ
        array = { 65, 23, 5 }, -- 3493
        dict = {  -- !!!,11
            string = "value",  -- wassup
            array = {  -- wassup
                3, 6,   -- wassup
                4 }, -- [2]
            mixed = { 43, 54.3, false, string = "value", 9 }    -- wassup
        }                   -- wassup
    }'''
    ) == {
        'array': [65, 23, 5],
        'dict': {
            'string': 'value',
            'array': [3, 6, 4],
            'mixed': {1: 43, 2: 54.3, 3: False, 'string': 'value', 4: 9},
        },
    }


def test_varied_tables():
    assert slpp.decode(
        '{ 43, 54.3, false, string = "value", 9, [4] = 111, [1] = 222, [2.1] = "text" }'
    ) == {
        1: 43,
        2: 54.3,
        3: False,
        4: 9,
        'string': 'value',
        2.1: 'text',
    }
    assert slpp.decode('{ 43, 54.3, false, 9, [5] = 111, [7] = 222 }') == {
        1: 43,
        2: 54.3,
        3: False,
        4: 9,
        5: 111,
        7: 222,
    }
    assert slpp.decode('{ [7] = 111, [5] = 222, 43, 54.3, false, 9 }') == {
        7: 111,
        5: 222,
        1: 43,
        2: 54.3,
        3: False,
        4: 9,
    }
    assert slpp.decode('{ 43, 54.3, false, 9, [4] = 111, [5] = 52.1 }') == [
        43,
        54.3,
        False,
        9,
        52.1,
    ]
    assert slpp.decode('{ [5] = 111, [4] = 52.1, 43, [3] = 54.3, false, 9 }') == {
        5: 111,
        4: 52.1,
        1: 43,
        2: False,
        3: 9,
    }
    assert slpp.decode('{ [1] = 1, [2] = "2", 3, 4, [5] = 5 }') == {
        1: 3,
        2: 4,
        5: 5,
    }
