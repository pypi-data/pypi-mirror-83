# MIT License
#
# Copyright (c) 2020 Aki Mäkinen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from typing import Dict


def Metadocument(cls):
    newclass = DocumentMetaclass(cls.__name__, cls.__bases__, dict(cls.__dict__))
    return newclass

class DocumentMetaclass(type):
    def __new__(cls, clsname, bases, clsdict):
        fields = []
        class_dictionaries = []
        if bases is not None:
            class_dictionaries = [base.__dict__ for base in bases]
        class_dictionaries.append(dict(clsdict))
        new_class_dict = {**dict(clsdict)}

        for class_dict in class_dictionaries:
            for key, value in class_dict.items():
                if not str.startswith(key, "_") and not callable(value):
                    new_class_dict[key] = value
                    fields.append(key)

        new_class_dict["_fields"] = fields

        def to_dict(self) -> Dict:
            new_dict = {}
            for key in getattr(self, "_fields"):
                value = getattr(self, key)

                if type(value) is Field:
                    key = value.key
                    value = value.value

                if type(value.__class__) is DocumentMetaclass:
                    new_dict[key] = value.to_dict()
                else:
                    new_dict[key] = value
            return new_dict

        def to_json(self, *args, **kwargs) -> str:
            dictionary = self.to_dict()
            import json
            return json.dumps(dictionary, *args, **kwargs)

        def to_yaml(self, *args, **kwargs) -> str:
            dictionary = self.to_dict()
            import yaml
            return yaml.dump(dictionary, *args, **kwargs)

        def add(self, other) -> DocumentMetaclass:
            if type(other.__class__) is not DocumentMetaclass:
                raise TypeError(f"unsupported operand type(s) for +: {type(self.__class__)} and {type(other)}")

            self_values = {key: getattr(self, key) for key in getattr(self, "_fields")}
            other_values = {key: getattr(other, key) for key in getattr(other, "_fields")}

            return DocumentMetaclass(
                f"{self.__class__.__name__}_{other.__class__.__name__}",
                (object,),
                {**self_values, **other_values}
            )()

        def radd(self, other) -> type:
            if other == 0:
                return self
            return self.__add__(other)

        clsobj = super().__new__(cls, clsname, bases, new_class_dict)

        setattr(clsobj, to_dict.__name__, to_dict)
        setattr(clsobj, to_json.__name__, to_json)
        setattr(clsobj, to_yaml.__name__, to_yaml)

        setattr(clsobj, "__add__", add)
        setattr(clsobj, "__radd__", radd)

        return clsobj


@Metadocument
class FromKeywords(dict):
    def __init__(self, *args, **kwargs):
        fields = []
        for key, value in kwargs.items():
            fields.append(key)
            setattr(self, key, value)
        self._fields = fields
        dict.__init__(self, **kwargs)


class Field:
    def __init__(self, *, key=None, value=None):
        if not key:
            raise TypeError("key must be set and cannot be falsy")
        if not value:
            raise TypeError("value must be set and cannot be falsy")
        self.key = key
        self.value = value
