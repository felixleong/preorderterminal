import configparser


class ConfigParser(configparser.ConfigParser):
    """
    ConfigParser implementation that can output as dict.

    Credit: Alex Martelli, http://stackoverflow.com/a/3220891
    """

    def as_dict(self):
        """
        Return a dictionary of the parsed config.

        :returns: The dictionary of the parsed config.
        :rtype: dict
        """
        d = dict(self._sections)

        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d
