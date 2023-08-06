# This file is part of rddlgym.

# rddlgym is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# rddlgym is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with rddlgym. If not, see <http://www.gnu.org/licenses/>.


"""Collection of utility functions used in the rddlgym package."""


from enum import Enum, auto
import json
import os

from pyrddl.parser import RDDLParser
from rddl2tf.compilers import DefaultCompiler

import rddlgym
from rddlgym.env import RDDLEnv


class Mode(Enum):
    """rddlgym.Mode controls the type of return in rddlgym.make()."""

    RAW = auto()
    AST = auto()
    SCG = auto()
    GYM = auto()


def read_db():
    """Returns list of available RDDL domains as a JSON object."""
    dirname = os.path.join(os.path.dirname(rddlgym.__file__), "files")
    domains = os.path.join(dirname, "all.json")
    with open(domains, "r") as file:
        domains = json.loads(file.read())
        return domains


def read_model(filename):
    """Returns RDDL string read from `filename`."""
    with open(filename, "r") as file:
        rddl = file.read()
        return rddl


def parse_model(filename, verbose=False):
    """Returns RDDL abstract syntax tree (AST)."""
    rddl = read_model(filename)
    parser = RDDLParser(verbose=verbose)
    parser.build()
    model = parser.parse(rddl)
    model.build()
    return model


def create_env(filename, config=None):
    """Returns a RDDLEnv object for the given RDDL file."""
    return RDDLEnv(filename, config)


def compile_model(filename):
    """Returns the rddl2tf compiler for the given RDDL file."""
    model = parse_model(filename)
    compiler = DefaultCompiler(model)
    return compiler


def load(filename, mode=Mode.AST, config=None, verbose=False):
    """Loads `filename` with given `mode`."""
    # pylint: disable=no-else-return
    if mode == Mode.RAW:
        return read_model(filename)
    elif mode == Mode.AST:
        return parse_model(filename, verbose)
    elif mode == Mode.SCG:
        return compile_model(filename)
    elif mode == Mode.GYM:
        return create_env(filename, config)
    else:
        raise ValueError("Invalid rddlgym mode: {}".format(mode))


def make(rddl, mode=Mode.AST, config=None, verbose=False):
    """Returns `rddl` object for the given `mode`."""
    # pylint: disable=no-else-return
    if os.path.isfile(rddl):
        return load(rddl, mode, config, verbose)
    else:
        dirname = os.path.join(os.path.dirname(rddlgym.__file__), "files")
        filename = os.path.join(dirname, "{}.rddl".format(rddl))
        if not os.path.isfile(filename):
            raise ValueError("Couldn't find RDDL domain: {}".format(rddl))
        return load(filename, mode, config, verbose)
