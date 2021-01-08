# Taken from http://www.sqlalchemy.org/trac/wiki/UsageRecipes/Enum

# # The MIT License

# Copyright (c) <year> <copyright holders>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from Products.CMFPlone.utils import safe_unicode
from sqlalchemy import types

import six
import uuid


class UUID(types.TypeEngine):
    def get_col_spec(self):
        return "UUID"

    def bind_processor(self, dialect):
        def convert(value):
            if isinstance(value, six.string_types):
                return value
            elif isinstance(value, uuid.UUID):
                return str(value)
            raise TypeError

        return convert

    def result_processor(self, dialect):
        def convert(value):
            return value

        return convert

    def convert_result_value(self, value, dialect):
        return value

    def convert_bind_param(self, value, dialect):
        return value


class Enum(types.TypeDecorator):
    impl = types.Unicode

    def __init__(self, values, empty_to_none=False, strict=False):
        """Emulate an Enum type.

        values:
           A list of valid values for this column
        empty_to_none:
           Optional, treat the empty string '' as None
        strict:
           Also insist that columns read from the database are in the
           list of valid values.  Note that, with strict=True, you won't
           be able to clean out bad data from the database through your
           code.
        """

        if values is None or len(values) == 0:
            raise TypeError("Enum requires a list of values")
        self.empty_to_none = empty_to_none
        self.strict = strict
        self.values = values[:]

        # The length of the string/unicode column should be the longest string
        # in values
        size = max([len(v) for v in values if v is not None])
        super(Enum, self).__init__(size)

    def process_bind_param(self, value, dialect):
        if self.empty_to_none and value == "":
            value = None
        if value not in self.values:
            raise ValueError('"%s" not in Enum.values' % value)
        if value is None:
            return None
        else:
            return safe_unicode(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if self.strict and value not in self.values:
            raise ValueError('"%s" not in Enum.values' % value)
        return safe_unicode(value)


if __name__ == "__main__":
    from sqlalchemy import Column
    from sqlalchemy import Integer
    from sqlalchemy import MetaData
    from sqlalchemy import Table

    t = Table(
        "foo",
        MetaData("sqlite:///"),
        Column("id", Integer, primary_key=True),
        Column("e", Enum([u"foobar", u"baz", u"quux", None])),
    )
    t.create()

    t.insert().execute(e=u"foobar")
    t.insert().execute(e=u"baz")
    t.insert().execute(e=u"quux")
    t.insert().execute(e=None)

    try:
        t.insert().execute(e=u"lala")
        assert False
    except AssertionError:
        pass

    print(list(t.select().execute()))
