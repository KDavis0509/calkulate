# Calkulate: seawater total alkalinity from titration data
# Copyright (C) 2019-2020  Matthew P. Humphreys  (GNU GPLv3)
"""Classes for the different components of a titration."""

import numpy as np
from .. import density, io


class Analyte:
    """Properties of the analyte being titrated."""

    def __init__(self, ttr, fdata):
        self.salinity = ttr.salinity
        self.temperature = fdata["mixture_temperature"][0]
        self.density = density.seawater_atm_MP81(self.temperature, self.salinity)
        self.volume = ttr.analyte_volume
        self.mass = self.volume * self.density
        # User provides or assumed zero:
        self.ammonia = io.check_set(ttr, "ammonia", 0)
        self.phosphate = io.check_set(ttr, "phosphate", 0)
        self.silicate = io.check_set(ttr, "silicate", 0)
        self.sulfide = io.check_set(ttr, "sulfide", 0)
        # User provides or estimated later from salinity:
        self.borate = io.check_set(ttr, "borate", None)
        self.fluoride = io.check_set(ttr, "fluoride", None)
        self.sulfate = io.check_set(ttr, "sulfate", None)


class Titrant:
    """Properties of the titrant added to the analyte."""

    def __init__(self, ttr, fdata):
        self.volume = fdata["titrant_volume"]
        self.density = density.HCl_NaCl_25C_DSC07()
        self.mass = self.volume * self.density


class Mixture:
    """Properties of the titrant-analyte mixture."""

    def __init__(self, ttr, fdata):
        self.emf = fdata["mixture_emf"]
        self.temperature = fdata["mixture_temperature"]


class Settings:
    """Settings for solving the titration."""

    def __init__(self, ttr, fdata):
        self.carbonic_constants = io.check_set(ttr, "carbonic_constants", 10)
        self.borate_ratio = io.check_set(ttr, "borate_ratio", 2)