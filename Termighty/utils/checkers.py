import numpy as np

from ..data import arr_types, str_types, real_types

def check_type(var, types, name = None, method = None, function = None):
    '''
        PURPOSE
        Confirms that 'var' is of desired type, otherwise raises a TypeError

        PARAMETERS
        var         anything
        types       <type> or list/array of <type>

        OPTIONAL PARAMETERS
        name        <str> name of the variable
        method      <str> name of the method from which this variable came
        function    <str> name of the function from which this variable came

        WARNING
        Cannot pass both 'method' and 'function', as these are mutually
        exclusive.

        RETURNS
        True
    '''
    # 'types' should be iterable
    if isinstance(types, type):
        types = [types]

    # To report errors in the arguments passed to this function
    fmt_msg = ('\n\nParameter \'{}\' in function \'check_type\' must be a '
                   'member of {}')
    if name is not None and not isinstance(name, str_types):
        raise TypeError(fmt_msg.format('name', 'str'))
    if method is not None and not isinstance(method, str_types):
        raise TypeError(fmt_msg.format('method', 'str'))
    if function is not None and not isinstance(function, str_types):
        raise TypeError(fmt_msg.format('function', 'str'))

    # Making sure that 'function' and 'method' are not both implemented
    if function is not None and method is not None:
        msg = ('\n\nCannot pass arguments \'function\' and \'method\' to '
               'function \'check_type\' simultaneously.')
        raise ValueError(msg)

    if isinstance(types, arr_types) and len(types) >= 1:
        for t in types:
            if not isinstance(t, type):
                fmt_msg += 'or a list/tuple with elements of {}'
                raise ValueError(fmt_msg.format('types', 'type', 'type'))

            elif t == type(var):
                return True

        if len(types) == 1:
            valid_types = str(types[0])

        elif len(types) == 2:
            valid_types = (f'{str(types[0])} or {str(types[1])}')
        else:
            valid_types = f'one of the following:'
            for t in types:
                valid_types += f'\n\t{str(t)}'

        if name is not None:
            msg = f'\n\nParameter \'{name}\' '
            if function is not None:
                msg += f'in function \'{function}\' '

            elif method is not None:
                msg += f'in method \'{method}\' '

            msg += (f'is a member of {str(type(var))}, but should '
                     'be a member of ')

        elif function is not None:
            msg = (f'Function \'{function}\' got an instance of '
                    f'{str(type(var))}, but expected an instance of ')

        elif method is not None:
            msg = (f'Method \'{method}\' got an instance of '
                    f'{str(type(var))}, but expected an instance of ')

        else:
            msg = (f'Got instance of {str(type(var))}, but expected an '
                    'instance of ')

        msg += valid_types
        raise TypeError(msg)

    else:
        fmt_msg += 'or a list/tuple with elements of {}'
        raise ValueError(fmt_msg.format('types', 'type', 'type'))

def check_type_arr(arr, types, name = None, method = None, function = None):
    '''
        PURPOSE
        Confirms that every element of 'arr' is of desired type, otherwise
        raises a TypeError.

        PARAMETERS
        arr         <list> or <tuple>
        types       <type> or list/array of <type>

        OPTIONAL PARAMETERS
        name        <str> name of the variable
        method      <str> name of the method from which this variable came
        function    <str> name of the function from which this variable came

        WARNING
        Cannot pass both 'method' and 'function', as these are mutually
        exclusive.

        RETURNS
        True
    '''
    check_type(arr, arr_types, name, method, function)
    for var in arr:
        check_type(var, types, name, method, function)

    return True

def check_type_arr_2D(arr, types, name = None, method = None, function = None):
    '''
        PURPOSE
        Confirms that 'arr' is a 2_D rectangular iterable whose elements are
        all of desired type, otherwise raises a TypeError.

        PARAMETERS
        arr         2-D iterable
        types       <type> or list/array of <type>

        OPTIONAL PARAMETERS
        name        <str> name of the variable
        method      <str> name of the method from which this variable came
        function    <str> name of the function from which this variable came

        WARNING
        Cannot pass both 'method' and 'function', as these are mutually
        exclusive.

        RETURNS
        True
    '''

    check_type(arr, arr_types, name, method, function)

    msg = '\n\nParameter \'arr\' must be a 2-D rectangular array.'
    row_length = None

    for row in arr:
        try:
            check_type(row, arr_types, name, method, function)
        except:
            raise TypeError(msg)
        if row_length is None:
            row_length = len(row)
        elif len(row) != row_length:
            raise ValueError(msg)
        for var in row:
            check_type(var, types, name, method, function)

    return True

def check_range(var, low = None, high = None, name = None, method = None, function = None):
    '''
        PURPOSE
        Checks that 'var' is a number within the selected range.  'low' is the
        lower boundary, and 'high' is the upper boundary.  Either can be set to
        None, which removes that particular boundary.

        PARAMETERS
        var         number or

        OPTIONAL PARAMETERS
        low         <float> or <int>
        high        <float> or <int>
        name        <str> name of the variable
        method      <str> name of the method from which this variable came
        function    <str> name of the function from which this variable came

        WARNING
        Cannot pass both 'method' and 'function', as these are mutually
        exclusive.

        RETURNS
        True
    '''
    check_type(var, real_types, name, method, function)
    if low is not None:
        check_type(low, real_types, name, method, function)
    if high is not None:
        check_type(low, real_types, name, method, function)

    if low is not None and high is not None:

        if low > high:
            msg = 'Parameter \'low\' must be lower than \'high\'.'
            raise ValueError(msg)
        elif var >= low and var <= high:
            return True
        else:
            val_range = f'in the range [{low:g},{high:g}]'

    elif low is not None and low <= var:
        return True

    elif high is not None and high >= var:
        return True

    elif low is None and high is None:
        return True

    elif low is not None and low > var:
        val_range = f'greater than {low:g}'

    elif high is not None and high < var:
        val_range = f'less than {high:g}'

    if name is not None:
        msg = f'\n\nParameter \'{name}\' '
        if function is not None:
            msg += f'in function \'{function}\' '

        elif method is not None:
            msg += f'in method \'{method}\' '

        msg += 'should be '

    elif function is not None:
        msg = (f'Function \'{function}\' expected a number ')

    elif method is not None:
        msg = (f'Method \'{method}\' expected a number ')

    else:
        msg = f'Expected a number '

    msg += val_range

    raise ValueError(msg)

def check_range_arr(arr, low = None, high = None, name = None, method = None, function = None):
    '''
        PURPOSE
        Checks that 'arr' is a list or tuple of numbers within the selected
        range.  'low' is the lower boundary, and 'high' is the upper boundary.
        Either can be set to None, which removes that particular boundary.

        PARAMETERS
        arr         iterable of numbers

        OPTIONAL PARAMETERS
        low         <float> or <int>
        high        <float> or <int>
        name        <str> name of the variable
        method      <str> name of the method from which this variable came
        function    <str> name of the function from which this variable came

        WARNING
        Cannot pass both 'method' and 'function', as these are mutually
        exclusive.

        RETURNS
        True
    '''
    check_type(arr, arr_types, name, method, function)
    for var in arr:
        check_range(var, low, high, name, method, function)

    return True

def check_range_arr_2D(arr, low = None, high = None, name = None, method = None, function = None):
    '''
        PURPOSE
        Checks that 'arr' is a 2-D rectangular iterable of numbers within the
        selected range.  'low' is the lower boundary, and 'high' is the upper
        boundary. Either can be set to None, which removes that particular
        boundary.

        PARAMETERS
        arr         2-D iterable of numbers

        OPTIONAL PARAMETERS
        low         <float> or <int>
        high        <float> or <int>
        name        <str> name of the variable
        method      <str> name of the method from which this variable came
        function    <str> name of the function from which this variable came

        WARNING
        Cannot pass both 'method' and 'function', as these are mutually
        exclusive.

        RETURNS
        True
    '''
    check_type(arr, arr_types, name, method, function)

    msg = '\n\nParameter \'arr\' must be a 2-D rectangular array.'
    row_length = None

    for row in arr:
        if row_length is None:
            row_length = len(row)
        elif len(row) != row_length:
            raise ValueError(msg)
        for var in row:
            check_range(var, low, high, name, method, function)

    return True

def check_shape_arr(arr, shape, name = None, method = None, function = None):
    '''
        PURPOSE
        Confirms that array 'arr' is of desired shape, otherwise raises a
        ValueError.

        PARAMETERS
        arr         <list>, <tuple>, or <np.ndarray>
        shape       <tuple> of <int>

        OPTIONAL PARAMETERS
        name        <str> name of the variable
        method      <str> name of the method from which this variable came
        function    <str> name of the function from which this variable came

        WARNING
        Cannot pass both 'method' and 'function', as these are mutually
        exclusive.

        RETURNS
        True
    '''
    check_type(arr, arr_types, 'arr', method, function)
    check_type(shape, arr_types, 'shape', method, function)

    # To report errors in the arguments passed to this function
    fmt_msg = ('\n\nParameter \'{}\' in function \'check_shape_arr\' must be a '
                   'member of {}')
    if name is not None and not isinstance(name, str_types):
        raise TypeError(fmt_msg.format('name', 'str'))
    if method is not None and not isinstance(method, str_types):
        raise TypeError(fmt_msg.format('method', 'str'))
    if function is not None and not isinstance(function, str_types):
        raise TypeError(fmt_msg.format('function', 'str'))

    # Making sure that 'function' and 'method' are not both implemented
    if function is not None and method is not None:
        msg = ('\n\nCannot pass arguments \'function\' and \'method\' to '
               'function \'check_shape_arr\' simultaneously.')
        raise ValueError(msg)

    if not isinstance(arr, np.ndarray):
        arr = np.array(arr)

    if not np.array_equal(arr.shape, shape):
        if name is not None:
            msg = f'\n\nParameter \'{name}\' '
            if function is not None:
                msg += f'in function \'{function}\' '

            elif method is not None:
                msg += f'in method \'{method}\' '

            msg += (f'is of shape {arr.shape}, but expected {shape}.')

        elif function is not None:
            msg = (f'Function \'{function}\' got an array of shape {arr.shape},'
                   f' but expected {shape}.')

        elif method is not None:
            msg = (f'Method \'{method}\' got an array of shape {arr.shape}, '
                    f'but expected {shape}.')

        else:
            msg = f'Got array of shape {arr.shape}, but expected {shape}.'

        raise TypeError(msg)
