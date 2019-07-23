from .config import *

# Exception Handling

def check_type_method(type_exp, obj, clss = None, mthd = None, arg = None):
    """
        Check that the argument "obj" is of the type "type_exp".  If it isn't,
        raises a TypeError with a generic message.  Specifies error details if
        given in "clss" (short for "class"), "mthd" (short for "method"),
        and "arg" (short for "argument").
    """
    # Checking if "type_exp" is a <type> or list/tuple of types
    msg = "\n\nArgument \"type_exp\" in function \"check_type_method()\" "
    msg += "must either be of type <type>, or must be a list/tuple "
    msg += "that only contains types (eg. <int>, <float>, etc...)"
    if isinstance(type_exp, (list, tuple)):
        for i in type_exp:
            if not isinstance(i, type) and i is not None:
                raise TypeError(msg)
    elif not isinstance(type_exp, type) and type_exp is not None:
        raise TypeError(msg)

    # Checking if "clss" is None or a string:
    msg = "\n\nArgument \"clss\" in function \"check_type_method()\" "
    msg += "must either be a <str>, or None."
    if not isinstance(clss, str) and clss is not None:
        raise TypeError(msg)

    # Checking if "mthd" is None or a string:
    msg = "\n\nArgument \"mthd\" in function \"check_type_method()\" "
    msg += "must either be a <str>, or None."
    if not isinstance(mthd, str) and mthd is not None:
        raise TypeError(msg)

    # Checking if "arg" is None or a string:
    msg = "\n\nArgument \"arg\" in function \"check_type_function()\" "
    msg += "must either be a <str>, or None."
    if not isinstance(arg, str) and arg is not None:
        raise TypeError(msg)

    # Checking if the types match
    if isinstance(type_exp, (list, tuple)):
        for t in type_exp:
            if type(obj) == t:
                return True
    elif isinstance(type_exp, type):
        if type(obj) == type_exp:
            return True

    # Generating an error message based on the given arguments
    if clss is not None and mthd is not None and arg is not None:
        msg = "\n\nArgument \"{}\" in method \"{}\" in ".format(arg, mthd)
        msg += "class \"{}\" should belong to:\n\n\t".format(clss)
    elif clss is not None and mthd is not None:
        msg = "\n\nAn argument in method \"{}\" in ".format(mthd)
        msg += "class \"{}\" should belong to:\n\n\t".format(clss)
    elif mthd is not None and arg is not None:
        msg = "\n\nArgument \"{}\" in method \"{}\" should belong to:\n\n\t"\
        .format(arg, mthd)
    elif clss is not None:
        msg = "\n\nArgument of a method in class \"{}\" ".format(clss)
        msg += "should belong to:\n\n\t"
    elif mthd is not None:
        msg = "\n\nAn argument in method \"{}\" should belong to:\n\n\t"\
        .format(mthd)
    elif arg is not None:
        msg = "\n\nArgument \"{}\" should belong to:\n\n\t".format(arg)
    else:
        msg = "\n\nExpected a:\n\n\t"

    if isinstance(type_exp, (list, tuple)):
        if len(type_exp) == 1:
            msg += "{}".format(type_exp[0])
        elif len(type_exp) == 2:
            msg += "{} or {}".format(type_exp[0], type_exp[1])
        else:
            for n,t in enumerate(type_exp):
                msg += str(t)
                if n < len(type_exp)-2:
                    msg += ", "
                elif n == len(type_exp)-2:
                    msg += ", or "
    else:
        msg += "{}".format(type_exp)

    msg += "\n\nGot a {} instead.".format(type(obj))

    raise TypeError(msg)

def check_type_function(type_exp, obj, func = None, arg = None):
    """
        Check that the argument "obj" is of the type "type_exp".  If it isn't,
        raises a TypeError with a generic message.  Specifies error details if
        given in "func" (short for "function") and "arg" (short for "argument").
    """
    # Checking if "type_exp" is a <type> or list/tuple of types
    msg = "\n\nArgument \"type_exp\" in function \"check_type_function()\" "
    msg += "must either be of type <type>, or must be a list/tuple "
    msg += "that only contains types (eg. <int>, <float>, etc...)"
    if isinstance(type_exp, (list, tuple)):
        for i in type_exp:
            if not isinstance(i, type) and i is not None:
                raise TypeError(msg)
    elif not isinstance(type_exp, type) and type_exp is not None:
        raise TypeError(msg)

    # Checking if "func" is None or a string:
    msg = "\n\nArgument \"func\" in function \"check_type_function()\" "
    msg += "must either be a <str>, or None."
    if not isinstance(func, str) and func is not None:
        raise TypeError(msg)

    # Checking if "arg" is None or a string:
    msg = "\n\nArgument \"arg\" in function \"check_type_function()\" "
    msg += "must either be a <str>, or None."
    if not isinstance(arg, str) and arg is not None:
        raise TypeError(msg)

    # Checking if the types match
    if isinstance(type_exp, (list, tuple)):
        for t in type_exp:
            if type(obj) == t:
                return True
    elif isinstance(type_exp, type):
        if type(obj) == type_exp:
            return True

    # Generating an error message based on the given arguments
    if func is not None and arg is not None:
        msg = "\n\nArgument \"{}\" in function \"{}\" should belong to:\n\n\t"\
        .format(arg, func)
    elif func is not None:
        msg = "\n\nAn argument in function \"{}\" should belong to:\n\n\t"\
        .format(func)
    elif arg is not None:
        msg = "\n\nArgument \"{}\" should belong to:\n\n\t".format(arg)
    else:
        msg = "\n\nExpected a:\n\n\t"

    if isinstance(type_exp, (list, tuple)):
        if len(type_exp) == 1:
            msg += "{}".format(type_exp[0])
        elif len(type_exp) == 2:
            msg += "{} or {}".format(type_exp[0], type_exp[1])
        else:
            for n,t in enumerate(type_exp):
                msg += str(t)
                if n < len(type_exp)-2:
                    msg += ", "
                elif n == len(type_exp)-2:
                    msg += ", or "
    else:
        msg += "{}".format(type_exp)

    msg += "\n\nGot a {} instead.".format(type(obj))

    raise TypeError(msg)

def check_char_args_method(t_color, b_color, style, clss = None, mthd = None):
    """
        Checks that "t_color", "b_color", and "style" follow the standard
        allowed colors and styles.
    """
    check_type_method(str, t_color, clss, mthd, "t_color")
    check_type_method(str, b_color, clss, mthd, "b_color")
    check_type_method(str, style, clss, mthd, "style")

    def check(argval, allowed_vals, allowed_names, clss, mthd):
        if argval not in allowed_vals.keys():
            msg = "\n\nArgument \"{}\"".format(argname)
            if clss is not None and mthd is not None:
                msg += " of method \"{}\" in class \"{}\""\
                .format(mthd, clss)
            elif clss is not None:
                msg += " of method in class \"{}\""\
                .format(clss)
            elif mthd is not None:
                msg += " of method \"{}\""\
                .format(mthd)
            msg += " is invalid.\n\n\tAvailable selection:"
            for k,v in allowed_names.items():
                msg += "\n\t[{}] – {}".format(v, k)
            raise ValueError(msg)

    check(t_color, globals()["text_colors"], globals()["aliases_color"], clss,
    mthd)

    check(b_color, globals()["back_colors"], globals()["aliases_color"], clss,
    mthd)

    check(style, globals()["styles"], globals()["aliases_style"], clss, mthd)

def check_char_args_function(t_color, b_color, style, func = None):
    """
        Checks that "t_color", "b_color", and "style" follow the standard
        allowed colors and styles.
    """

    check_type_function(str, t_color, func, "t_color")
    check_type_function(str, b_color, func, "b_color")
    check_type_function(str, style, func, "style")

    def check(argval, allowed_vals, allowed_names, func):
        if argval not in allowed_vals.keys():
            msg = "\n\nArgument \"{}\"".format(argname)
            if func is not None:
                msg += " in function \"{}\""\
                .format(func)
            msg += " is invalid.\n\n\tAvailable selection:"
            for k,v in allowed_names.items():
                msg += "\n\t[{}] – {}".format(v, k)
            raise ValueError(msg)

    check(t_color, globals()["text_colors"], globals()["aliases_color"], func)

    check(b_color, globals()["back_colors"], globals()["aliases_color"], func)

    check(style, globals()["styles"], globals()["aliases_style"], func)
