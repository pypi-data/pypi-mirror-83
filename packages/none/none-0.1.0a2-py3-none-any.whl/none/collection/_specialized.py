# none/collection/_specialized.py
# ===============================
#
# Copying
# -------
#
# Copyright (c) 2020 none authors and contributors.
#
# This file is part of the *none* project.
#
# None is a free software project. You can redistribute it and/or
# modify it following the terms of the MIT License.
#
# This software project is distributed *as is*, WITHOUT WARRANTY OF ANY
# KIND; including but not limited to the WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE and NONINFRINGEMENT.
#
# You should have received a copy of the MIT License along with
# *none*. If not, see <http://opensource.org/licenses/MIT>.
#
from collections.abc import Mapping, Sequence


class arguments(Sequence, Mapping):
    """Helper to store arbitrary arguments of a function."""
    __slots__ = ("args", "kwargs")

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        self.args = args
        self.kwargs = kwargs

        return self

    def __eq__(self, other):
        if not isinstance(other, arguments):
            return NotImplemented

        return (
            self.args == other.args
            and self.kwargs == other.kwargs
        )

    def __getitem__(self, item: ty.Union[int, str]) -> ty.Any:
        if isinstance(item, int):
            return self.args[item]
        elif isinstance(item, str):
            return self.kwargs[item]
        else:
            raise TypeError(item)

    def __iter__(self):
        yield self.args
        yield self.kwargs

    def items(self):
        return self.kwargs.items()

    def keys(self):
        return self.kwargs.keys()

    def values(self):
        return self.kwargs.values()
