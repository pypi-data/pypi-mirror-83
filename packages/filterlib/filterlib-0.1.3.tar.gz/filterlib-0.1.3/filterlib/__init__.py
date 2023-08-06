import re
from typing import *
import json

__author__ = "Fabian Becker <fab.becker@outlook.de>"


class Filter:
    default_quotes = "\""

    replacements = {"__eq__": "=",
                    "__ne__": "!=",
                    "__lt__": "<",
                    "__gt__": ">",
                    "__lte__": "<=",
                    "__gte__": ">=",
                    "__contains__": " BETWEEN "}

    def __init__(self,
                 operator: str = "AND",
                 quote_type: str = "",
                 *args,
                 **kwargs):
        self.operator = operator
        self.quote_type = quote_type
        self.__dict__.update({a: None for a in args})
        self.ignored_attributes = [x for x in self.__dir__()] + ["ignored_attributes"]
        # any argument matching the pattern is accepted
        for attr in kwargs:
            if not (re.match(r'\S*__\w+__$', attr) or attr in self.ignored_attributes or type(kwargs[attr]) == Filter):
                raise ValueError(f"{attr} does not match expected attribute format.")
        self.__dict__.update(kwargs)

        assert self.operator in ["AND", "OR"], "An operator has to be chosen."

    def __eq__(self, other):
        # check for all/any non hidden attributes of this class
        # if they are present in another object
        # and equal the corresponding attributes of another object
        patterns = [attr for attr in self.__dir__()
                    if attr not in self.ignored_attributes]
        results = []
        for pattern in patterns:
            if type(self.__getattribute__(pattern)) != Filter:
                # Check for equality with any object other than filter
                attributes = [
                    x for x in pattern.split("__")[0:-2]
                    if x
                ]
                magic_method = "__" + pattern.split("__")[-2] + "__"
                vo = other
                r = False
                try:
                    for attr in attributes:
                        vo = vo.__getattribute__(attr)
                    r = vo.__getattribute__(magic_method)(self.__getattribute__(pattern))
                except AttributeError:
                    if self.operator == "AND":
                        # Exit with False result
                        return False
                    if self.operator == "OR":
                        # Give another chance without storing the result
                        continue
                results.append(bool(r))
            else:
                # Check for compatibility with filters
                results.append(bool(self.__getattribute__(pattern) == other))
        if self.operator == "AND":
            return False not in results
        if self.operator == "OR":
            return True in results

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self, logical_condition: Optional[str] = None, quotes: str = ""):
        # Returns a string to be used for sql style databases
        attributes = [a for a in self.__dir__()
                      if not (a.startswith("__") or a in self.ignored_attributes)]
        quotes = quotes or self.quote_type or Filter.default_quotes
        for attr in range(len(attributes)):
            name = attributes[attr]
            value = self.__getattribute__(name)
            use_brackets = (True if type(value) == Filter and len(value) > 1 else False)
            use_quotes = (True if type(value) == str else False)
            a = (name if type(value) != Filter else "") \
                + (quotes if use_quotes else "") \
                + ("(" if use_brackets else "") \
                + str(value) \
                + (")" if use_brackets else "") \
                + (quotes if use_quotes else "")
            for element in self.replacements:
                a = a.replace(element, self.replacements[element])
            attributes[attr] = a
        return str.join(f" {(logical_condition or self.operator).upper()} ", attributes)

    def __repr__(self):
        # returns a string to be used for storage in text files or sql databases
        d = {x: (self.__dict__[x] if type(self.__dict__[x]) is not Filter else self.__dict__[x].__repr__())
             for x in self.__dir__() if x not in self.ignored_attributes}
        d["operator"] = self.operator
        r = f"<Filter: {json.dumps(d)}>"
        return r

    def __len__(self):
        # returns the number of attributes the filter checks for
        return len([x for x in self.__dir__() if x not in self.ignored_attributes])

    def __bool__(self):
        # returns of the number of attributes the filter checks for is greater than or equal to one
        return bool(self.__len__()) or "any" in dir(self)


def filter_from_repr(representation: str) -> Filter:
    f = Filter()
    f.__dict__.update(json.loads(representation.lstrip("<Filter: ").rstrip(">")))
    return f


if __name__ == "__main__":
    from tests.tests import main
    main()
