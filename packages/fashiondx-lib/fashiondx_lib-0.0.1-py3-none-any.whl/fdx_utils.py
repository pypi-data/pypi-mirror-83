import datetime
import numbers

from functools import reduce, partial

import numpy as np
import pandas as pd

"""
    TODO: MAKE SURE THAT EACH ARG IS A PANDAS SERIES

    Current support only for pandas Series
    TODO: Expand support
"""

class Operation(object):
    @staticmethod
    def pair(a, b, op):
        err = "Base class can not perform pair operations."
        raise NotImplementedError(err)

class BasicOp(Operation): pass

class ArithmeticOp(BasicOp):
    @staticmethod
    def pair(a, b, op):
        sa = isinstance(a, pd.Series)
        da = isinstance(a, pd.DataFrame)
        na = isinstance(a, numbers.Number)
        sb = isinstance(b, pd.Series)
        db = isinstance(b, pd.DataFrame)
        nb = isinstance(b, numbers.Number)
        series_op = sa and (sb or nb)
        frame_op = da and (db or nb)
        if series_op or frame_op:
            if op == "add":
                return a.add(b)
            elif op == "sub":
                return a.sub(b)
            elif op == "mul":
                return a.mul(b)
            elif op == "div":
                return a.div(b)
        elif na:
            if op == "add":
                return a + b
            elif op == "sub":
                return a - b
            elif op == "mul":
                return a * b
            elif op == "div":
                return a / b
        raise TypeError(("%s of %s and %s not supported as of now"
                         "." % (op, type(a), type(b))))

class BooleanOp(BasicOp):
    @staticmethod
    def pair(a, b, op):
        if op == "and":
            return a & b
        elif op == "or":
            return a | b
        sa = isinstance(a, pd.Series)
        da = isinstance(a, pd.DataFrame)
        na = isinstance(a, numbers.Number)
        sb = isinstance(b, pd.Series)
        db = isinstance(b, pd.DataFrame)
        nb = isinstance(b, numbers.Number)
        series_op = sa and (sb or nb)
        frame_op = da and (db or nb)
        if series_op or frame_op:
            if op == "lt":
                return a.lt(b)
            elif op == "gt":
                return a.gt(b)
            elif op == "le":
                return a.le(b)
            elif op == "ge":
                return a.ge(b)
            elif op == "ne":
                return a.ne(b)
            elif op == "eq":
                return a.eq(b)
        elif na:
            if op == "lt":
                return a < b
            elif op == "gt":
                return a > b
            elif op == "le":
                return a <= b
            elif op == "ge":
                return a >= b
            elif op == "ne":
                return a != b
            elif op == "eq":
                return a == b
        raise TypeError(("%s of %s and %s not supported as of now"
                         "." % (op, type(a), type(b))))

def _dnc(args, pair_func):
    l = len(args)
    if l == 0:
        err = "At least one argument must be provided for operation."
        raise ValueError(err)
    if l == 1:
        return args[0]
    m = l // 2
    left = _dnc(args[:m], op)
    right = _dnc(args[m:], op)
    return pair_func(left, right)

# BASIC BOOLEAN AND ARITHMETIC OPERATIONS

def add(**kwargs):
    return _dnc(list(kwargs.values()),
        partial(ArithmeticOp.pair, op="add"))

def subtract(**kwargs):
    return _dnc([kwargs["v1"], kwargs["v2"]],
        partial(ArithmeticOp.pair, op="sub"))

def multiply(**kwargs):
    return _dnc(list(kwargs.values()),
        partial(ArithmeticOp.pair, op="mul"))

def divide(**kwargs):
    return _dnc([kwargs["v1"], kwargs["v2"]],
        partial(ArithmeticOp.pair, op="div"))

def bool_and(**kwargs):
    return _dnc(list(kwargs.values()),
        partial(BooleanOp.pair, op="and"))

def bool_or(**kwargs):
    return _dnc(list(kwargs.values()),
        partial(BooleanOp.pair, op="or"))

def less_than(**kwargs):
    return _dnc([kwargs["v1"], kwargs["v2"]],
        partial(BooleanOp.pair, op="lt"))

def greater_than(**kwargs):
    return _dnc([kwargs["v1"], kwargs["v2"]],
        partial(BooleanOp.pair, op="gt"))

def less_equal(**kwargs):
    return _dnc([kwargs["v1"], kwargs["v2"]],
        partial(BooleanOp.pair, op="le"))

def greater_equal(**kwargs):
    return _dnc([kwargs["v1"], kwargs["v2"]],
        partial(BooleanOp.pair, op="ge"))

def not_equal(**kwargs):
    return _dnc([kwargs["v1"], kwargs["v2"]],
        partial(BooleanOp.pair, op="ne"))

def equal(**kwargs):
    return _dnc([kwargs["v1"], kwargs["v2"]],
        partial(BooleanOp.pair, op="eq"))


method_map = {
    "and": bool_and,
    "or": bool_or,
    "lt": less_than,
    "gt": greater_than,
    "le": less_equal,
    "ge": greater_equal,
    "ne": not_equal,
    "eq": equal,
    "add": add,
    "sub": subtract,
    "mul": multiply,
    "div": divide,
    "default": lambda **kwargs: kwargs["v1"]
}


EXCEL_START_DATE = datetime.datetime(1900, 1, 1)
# BASIC DATE-TIME FUNCTIONS
def str_to_date(**kwargs):
    if isinstance(kwargs["date"], pd.Series):
        return pd.to_datetime(kwargs["date"], format=kwargs["format"])
    if isinstance(kwargs["date"], str):
        return datetime.datetime.strptime(kwargs["date"], kwargs["format"])
    raise TypeError("Method not supported for %s." % type(kwargs["date"]))

def excel_int_to_date(**kwargs):
    if isinstance(kwargs["date"], pd.Series):
        return pd.to_timedelta(kwargs["date"], unit='d') + EXCEL_START_DATE
    if isinstance(kwargs["date"], int):
        return EXCEL_START_DATE + datetime.timedelta(days=kwargs["date"])
    raise TypeError("Method not supported for %s." % type(kwargs["date"]))

def timedelta_to_days(**kwargs):
    if isinstance(kwargs["delta"], pd.Series):
        return kwargs["delta"].dt.days
    if isinstance(kwargs["delta"], datetime.timedelta):
        return datetime.timedelta(days=5)
    raise TypeError("Method not supported for %s." % type(kwargs["delta"]))

def timedelta_to_seconds(**kwargs):
    if isinstance(kwargs["delta"], pd.Series):
        return kwargs["delta"].dt.seconds
    if isinstance(kwargs["delta"], datetime.timedelta):
        return datetime.timedelta(seconds=5)
    raise TypeError("Method not supported for %s." % type(kwargs["delta"]))

def timedelta_to_musecs(**kwargs):
    if isinstance(kwargs["delta"], pd.Series):
        return kwargs["delta"].dt.microseconds
    if isinstance(kwargs["delta"], datetime.timedelta):
        return datetime.timedelta(microseconds=5)
    raise TypeError("Method not supported for %s." % type(kwargs["delta"]))

method_map.update({
    "str_to_date": str_to_date,
    "excel_int_to_date": excel_int_to_date,
    "timedelta_to_days": timedelta_to_days,
    "timedelta_to_seconds": timedelta_to_seconds,
    "timedelta_to_musecs": timedelta_to_musecs
})


# MORE BASIC FUNCTIONS
def _map_single(k, mapper):
    try:
        for arg in k.split('.'):
            if mapper == "":
                return mapper
            mapper = mapper[arg]
        return mapper
    except KeyError:
        return ""  # TODO: check how to handle this
def mapper_method(**kwargs):
    if isinstance(kwargs["v1"], pd.Series):
        return kwargs["v1"].map(kwargs["map"], na_action="")
    if isinstance(kwargs["v1"], str):
        return _map_single(kwargs["v1"], kwargs["map"])
    raise TypeError("Method not supported for %s." % type(kwargs["v1"]))

def slice_(**kwargs):
    if isinstance(kwargs["v1"], pd.Series):
        if "step" not in kwargs:
            return kwargs["v1"].str.slice(start=kwargs["start"],
                stop=kwargs["stop"])
        else:
            return kwargs["v1"].str.slice(start=kwargs["start"],
                stop=kwargs["stop"], step=kwargs["step"])
    if isinstance(kwargs["v1"], str):
        return kwargs["v1"][kwargs["start"]:kwargs["stop"]]

def lslice(**kwargs):
    if isinstance(kwargs["v1"], pd.Series):
        if "step" not in kwargs:
            return kwargs["v1"].str.slice(stop=kwargs["stop"])
        else:
            return kwargs["v1"].str.slice(stop=kwargs["stop"],
                step=kwargs["step"])
    if isinstance(kwargs["v1"], str):
        return kwargs["v1"][:kwargs["stop"]]

def rslice(**kwargs):
    if isinstance(kwargs["v1"], pd.Series):
        if "step" not in kwargs:
            return kwargs["v1"].str.slice(start=-kwargs["start"])
        else:
            return kwargs["v1"].str.slice(start=-kwargs["start"],
                step=kwargs["step"])
    if isinstance(kwargs["v1"], str):
        return kwargs["v1"][-kwargs["start"]:]

method_map.update({
    "str": lambda **kwargs: kwargs["v1"].map(str).str.strip() \
            if isinstance(kwargs["v1"], pd.Series()) else str(kwargs["v1"]),
    "map": mapper_method,
    "slice": slice_,
    "lslice": lslice,
    "rslice": rslice
})


# COMPOUND FUNCTIONS

def date_diff(**kwargs):
    # Function to calculate the difference between dates.
    # First argument is pandas Series containing dates from which to subtract,
    # Second argument is pandas Series containing dates to subtract and
    # Third argument is the kind of conversion needed for
    # final output day/month/etc
    for i in ("start", "end"):
        try:
            dt = kwargs[i].map(int)
            kwargs[i] = method_map["excel_int_to_date"](date=dt)
        except TypeError:
            kwargs[i] = method_map["str_to_date"](date=kwargs[i],
                format="%m/%d/%Y")
    res = method_map["sub"](v1=kwargs["end"], v2=kwargs["start"])
    op_format = "timedelta_to_%s" % kwargs["delta"]
    return method_map[op_format](delta=op_format)

def conditional(**kwargs):
    # Function to apply an if-else conditional. Make sure all args are
    # pandas Series with first arg as the condition, second arg as the value
    # to return for true third arg is the value to return for false
    def apply_condition(row):
        return row["true"] if row["condition"] else row["false"]

    df = pd.DataFrame(kwargs)
    return df.apply(apply_condition, axis=1)


method_map.update({
    "conditional": conditional,
    "date_diff": date_diff
})
