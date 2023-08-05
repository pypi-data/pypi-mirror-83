import json
from abc import ABC, abstractmethod
from aito.schema import AitoTableSchema, AitoAnalyzerSchema, AitoDelimiterAnalyzerSchema
import logging
import pandas as pd
from jsonschema import Draft7Validator, validate, Draft6Validator, Draft4Validator, Draft3Validator
from typing import TypeVar, Generic, Optional, overload


# class Tmp(ABC):
#     def __init__(self, str):
#         self.str = str
#
#     @classmethod
#     @abstractmethod
#     def validate(cls, str):
#         pass
#
#     @classmethod
#     @abstractmethod
#     def make(cls, str):
#         for sub_cls in cls.__subclasses__():
#             if sub_cls.validate(str):
#                 return sub_cls.make(str)
#
#
# class First(Tmp):
#     @classmethod
#     def make(cls, str):
#         if str == '11':
#             return XD1(str)
#         else:
#             return XD2(str)
#
#     @classmethod
#     def validate(cls, str):
#         return str.startswith('1')
#
#
# class XD1(First):
#     pass
#
# class XD2(First):
#     pass
#
#
# class Second(Tmp):
#     @classmethod
#     def make(cls, str):
#         return cls(str)
#
#     @classmethod
#     def validate(cls, str):
#         return str.startswith('2')
#
# print(type(Tmp.make('3')))


class Tmp:
    first = '1'

class Tmp2:
    first = '2'

class XD(Tmp, Tmp2):
    pass

print(XD().first)