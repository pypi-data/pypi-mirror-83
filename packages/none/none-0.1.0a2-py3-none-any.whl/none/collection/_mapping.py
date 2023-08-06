# none/collection/_mapping.py
# ===========================
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
import typing as ty
from collections.abc import Mapping


class frozendict(Mapping):
    """Generate a read-only dictionary. Both the keys and the elements of the
     dictionary must be hashable.

     """
    __slots__ = ("__it", "__set")

    def __init__(self, *args, **kwargs):
        self.__it = None
        self.__set = frozenset(((k, v) for k, v in dict(*args, **kwargs).items()))

    def __hash__(self):
        return hash(self.__set)

    def __iter__(self) -> ty.Iterator:
        self.__it = iter(self.__set)
        return self

    def __len__(self) -> int:
        return len(self.__set)

    def __next__(self):
        if self.__it is None:
            raise StopIteration

        try:
            return next(self.__it)[0]
        except StopIteration:
            self.__it = None
            raise

    def __getitem__(self, key: ty.Hashable) -> ty.Any:
        for k, v in self.__set:
            if key == k:
                return v
        raise KeyError(key)
