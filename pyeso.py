#!/usr/bin/python
# -*- coding: utf-8 -*-


class EsoVariable(object):
    """ Output EnergyPlus variable data.
    
    Attributes:
        name (str): The report variable name.
        units (str): The report variable units.
        key (str): The identifying "key name" for the line.
        freq (str): How frequently this data will appear.
        data (List[float]): The actual data associated with the variable.
    """

    def __init__(self, name, units, key, freq):
        self.name = name
        self.units = units
        self.key = key
        self.freq = freq
        self.data = []

    def __repr__(self):
        return "{}(name={}, units={}, key={}, freq={}, len(data)={})".format(
            self.__class__.__name__, self.name, self.units,
            self.key, self.freq, len(self.data))

    def __str__(self):
        return "ESO variable:\n" + \
            " - name:  {}\n".format(self.name) + \
            " - units: {}\n".format(self.units) + \
            " - key:   {}\n".format(self.key) + \
            " - freq:  {}\n".format(self.freq) + \
            " - data:  list of {} elements\n".format(len(self.data))


def read_metadata(fileobj):
    """ Reads the variables' metadata from an EnergyPlus output file (.eso).

    Args:
        fileobj (TextIO): The file object to read from.

    Returns:
        Dict[int, EsoVariable]: The dictionary with all the metadata.
    """
    vardict = {}
    for _ in range(6):
        next(fileobj)
    for line in fileobj:
        if line.startswith("End of Data Dictionary"):
            break
        rest, freq = [f.strip() for f in line.split("!")]
        fields = [f.strip() for f in rest.split(",")]
        id = fields[0]
        key = fields[-2]
        nameunits = fields[-1]
        name, units = [f[:-1] for f in nameunits.split("[")]
        vardict[id] = EsoVariable(name, units, key, freq)
    return vardict


def read_data(fileobj, vardict):
    """ Fills the data of the variables from an EnergyPlus output file (.eso).

    Args:
        fileobj (TextIO): The file object to read from.
    """
    for line in fileobj:
        if line.startswith("End of Data"):
            break
        id, value = [f.strip() for f in line.split(",")[:2]]
        if id in vardict:
            vardict[id].data.append(value)


def read(filename):
    """ Reads all the data from an EnergyPlus output file (.eso).

    Args:
        filename (str): The name of the file to read from.

    Returns:
        Dict[int, EsoVariable]: The dictionary with all the data.
    """
    with open(filename, "r") as fileobj:
        vardict = read_metadata(fileobj)
        read_data(fileobj, vardict)
        return vardict
