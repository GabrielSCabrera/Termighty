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

    for t in types:
        if isinstance(var, t):
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

    return True

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

        raise ValueError(msg)
