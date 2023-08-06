def shorten(package_name: str, max_length: int, level: int = 1) -> str:
    """
    Shorten package name like Convention Word in logback - but in a simpler
    version.
    Eg: package.name.class.Function will be shorten to p.n.c.Function

    @param package_name: name of package to shorten
    @param max_length: max length of shortened name - shortened name will be
    smaller or equal this value. If smaller - add space.
    @param level: to use this function recursive, add level to travel over dots

    >>> assert shorten("thit.cho.mam.tom", 9) == "t.c.m.tom"
    >>> assert shorten("thit.cho.mam.tom", 11) == "t.c.mam.tom"
    >>> assert shorten("thit.cho.mam.tom", 10) == "t.c.m.tom "
    """
    package_len = len(package_name)
    if package_len < max_length:
        return package_name.ljust(max_length, " ")
    elif package_len == max_length:
        return package_name
    dots = package_name.count(".")

    if dots < level:
        return package_name

    names = package_name.split(".")
    names[level-1] = names[level-1][0]
    new_package_name = ".".join(names)
    return shorten(new_package_name, max_length, level+1)
