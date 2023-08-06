#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains @decorators to help Mito sheet functions return and handle
types in a consistent way.
"""
import pandas as pd
from functools import wraps
from mitosheet.errors import make_invalid_arguments_error, make_function_execution_error

# Because type(1) = int, thus 1 is a 'number' in the Mito type system
MITO_PRIMITIVE_TYPE_MAPPING = {
    'number': [int, float],
    'string': [str],
    'boolean': [bool],
    'timestamp': [pd.Timestamp]
}

# NOTE: these are the dtype strings of series used by pandas!
MITO_SERIES_TYPE_MAPPING = {
    'number_series': ['int64', 'float64'],
    'string_series': ['str', 'object'],
    'boolean_series': ['bool'],
    'datetime_series': ['datetime64[ns]']
}

MITO_TYPE_PRIMITIVE_TO_SERIES_MAPPING = {
    'number': 'number_series',
    'string': 'string_series',
    'boolean': 'boolean_series',
    'timestamp': 'datetime_series'
}

def identity(x):
    """
    Helper function for the MITO_TYPE_CONVERSION_MAP, when turning from the conversion is from
    one type to itself (and so no work needs to be done).
    """
    return x

"""
A mapping of functions from converting from one Mito type to another. 

MITO_TYPE_CONVERSION_MAP['number']['string'] returns a function that 
converts from a number to a string. 

If there is no conversion possible the above is defined as None!

NOTE: the conversion functions may error and this should be handeled!
"""
MITO_TYPE_CONVERSION_MAP = {
    'number': {
        'number': identity,
        'string': lambda num: str(num),
        'boolean': lambda num: bool(num),
        'timestamp': None,
        'number_series': lambda num: pd.Series(data=[num]),
        'string_series': lambda num: pd.Series(data=[str(num)]),
        'boolean_series': lambda num: pd.Series(data=[bool(num)]),
        'datetime_series': None
    },
    'string': {
        'number': lambda string: float(string),
        'string': identity,
        'boolean': lambda string: bool(string),
        'timestamp': None,
        'number_series': lambda string: pd.Series(data=[float(string)]),
        'string_series': lambda string: pd.Series(data=[string]),
        'boolean_series': lambda string: pd.Series(data=[bool(string)]),
        'datetime_series': None
    },
    'boolean': {
        'number': lambda boolean: float(boolean),
        'string': lambda boolean: str(boolean),
        'boolean': identity,
        'timestamp': None,
        'number_series': lambda boolean: pd.Series(data=[float(boolean)]),
        'string_series': lambda boolean: pd.Series(data=[str(boolean)]),
        'boolean_series': lambda boolean: pd.Series(data=[boolean]),
        'datetime_series': None
    },
    'timestamp': {
        'number': None,
        'string': None,
        'boolean': None,
        'timestamp': identity,
        'number_series': None,
        'string_series': lambda timestamp: pd.Series(data=[timestamp.strftime('%Y-%m-%d')]),
        'boolean_series': None,
        'datetime_series': None
    },
    'number_series': {
        'number': None,
        'string': None,
        'boolean': None,
        'timestamp': None,
        'number_series': identity,
        'string_series': lambda num_series: num_series.astype('str'),
        'boolean_series': lambda num_series: num_series.astype('bool'),
        'datetime_series': None
    },
    'string_series': {
        'number': None,
        'string': None,
        'boolean': None,
        'timestamp': None,
        'number_series': lambda str_series: str_series.astype('float64'),
        'string_series': lambda str_series: str_series.astype('str'),
        'boolean_series': lambda str_series: str_series.astype('bool'),
        'datetime_series': None
    },
    'boolean_series': {
        'number': None,
        'string': None,
        'boolean': None,
        'timestamp': None,
        'number_series': lambda bool_series: bool_series.astype('float64'),
        'string_series': lambda bool_series: bool_series.astype('str'),
        'boolean_series': identity,
        'datetime_series': None
    },
    'datetime_series': {
        'number': None,
        'string': None,
        'boolean': None,
        'timestamp': None,
        'number_series': None,
        'string_series': lambda datetime_series: datetime_series.astype('str'),
        'boolean_series': None,
        'datetime_series': identity
    }
}

MITO_TYPES = set(MITO_PRIMITIVE_TYPE_MAPPING.keys()).union(MITO_SERIES_TYPE_MAPPING.keys())


def get_mito_type(obj):

    if isinstance(obj, pd.Series):
        dtype = obj.dtype
        for key, value in MITO_SERIES_TYPE_MAPPING.items():
            if dtype in value:
                return key

    elif isinstance(obj, pd.Timestamp):
        return 'timestamp'
    else:
        obj_type = type(obj)

        for key, value in MITO_PRIMITIVE_TYPE_MAPPING.items():
            if obj_type in value:
                return key

    return None

def is_in_type_set(type_set, obj):
    mito_type = get_mito_type(obj)

    if mito_type is None:
        return False

    return mito_type in type_set


def as_types(
        *args, 
        remaining=False, 
        ignore_conversion_failures=False, 
        num_optional=0,
        attempt_output_types=None
    ):
    """
    This generator factory will attempt to take the given arguments to the decorated sheet
    function and cast them to type arguments given in the decorator.

    This will primarily error if:
    0. If the wrong number of types are passed to the sheet function.
    1. A conversion cannot be made from the passed type to the target type:
        - You can't convert from a string_series to a string, for example
        - You can't convert from the string "hi" to a number
        - See the mappings defined above in the MITO_TYPE_CONVERSION_MAP above!

    However, if ignore_conversion_failures is True, will ignore errors of type (1), 
    and instead will just leave out the arguments that fail to convert.

    attempt_output_types is an optional parameter. If passed, it should be a function
    that takes all arguments as input, and returns the Mito type that it wants the result
    to be returned as.
    """

    types = args

    if set(args).difference(MITO_TYPES):
        raise Exception(f'Types to as_types must be from {MITO_TYPES}, not {args}')

    def wrap(sheet_function):
        @wraps(sheet_function)
        def wrapped_f(*args):
            # First, we check that the number of arguments passed is correct
            if not remaining:
                # If not remaining, then the function has a specific number of arguments
                if len(types) > len(args) + num_optional:
                    raise make_invalid_arguments_error(sheet_function.__name__)

            else:
                # Otherwise, the function takes a variable number of arguments, so we must have less
                # arguments than the number of given types
                if len(types) > len(args):
                    raise make_invalid_arguments_error(sheet_function.__name__)

            # Then, we fill the types to make sure there is a type for each of the passed arguments
            filled_types = [types[index] if index < len(types) else types[-1] for index, _ in enumerate(args)]
            new_arguments = []

            # Finially, we check that each given argument is of the valid type
            for to_type, argument in zip(filled_types, args):
                from_type = get_mito_type(argument)

                # We actually try and make a conversion
                conversion_function = MITO_TYPE_CONVERSION_MAP[from_type][to_type]

                # Error if no conversion is possible
                if conversion_function is None:
                    if not ignore_conversion_failures:
                        # Occurs if you cannot convert from {from_type} to {to_type}
                        raise make_invalid_arguments_error(sheet_function.__name__)

                    else:
                        continue

                try:
                    converted_arg = conversion_function(argument)
                except Exception as e:
                    if not ignore_conversion_failures:
                        # Occurs if you cannot convert from {from_type} to {to_type}
                        raise make_invalid_arguments_error(sheet_function.__name__)
                    else:
                        continue
                
                # If we can convert, then save the conversion as an argument!
                new_arguments.append(converted_arg)
                
            try:
                result = sheet_function(*new_arguments)
                # If we should cast the output, we try to cast it
                if attempt_output_types is not None:
                    attempt_output_type = attempt_output_types(*args)
                    # If there is no conversion available, we give up
                    if attempt_output_type is not None:
                        original_output_type = get_mito_type(result)
                        final_conversion_function = MITO_TYPE_CONVERSION_MAP[original_output_type][attempt_output_type]
                        if final_conversion_function is not None:
                            # NOTE: This can error during the conversion, in which case an error
                            # is reported back to the user that this function failed...
                            return final_conversion_function(result)
                # If we don't want to cast it, or if no cast is available, we just return the result as is
                return result
            except Exception as e:
                raise make_function_execution_error(sheet_function.__name__)

            return result
        return wrapped_f
    return wrap


def get_series_type_of_first_arg(*args):
    """
    Given a tuple of arguments, returns the Mito type of the first argument,
    in it's series interpretation.

    Useful for being passed as attempt_output_types for functions like 
    LEFT, RIGHT, MID, etc - where we want the function to preserve
    the output types if possible.
    """ 
    if len(args) == 0:
        return None

    mito_type = get_mito_type(args[0])

    # If it's a primitive type, we want it to be returned as a series
    if mito_type in MITO_PRIMITIVE_TYPE_MAPPING.keys():
        return MITO_TYPE_PRIMITIVE_TO_SERIES_MAPPING[mito_type]
    else:
        return mito_type


