def remove_extra_spaces(*args):
    """
    Substitutes multiple whitespace with one space and strips the strings.
    """

    if len(args) == 1:
        return " ".join(args[0].split())
    return [" ".join(arg.split()) for arg in args]
