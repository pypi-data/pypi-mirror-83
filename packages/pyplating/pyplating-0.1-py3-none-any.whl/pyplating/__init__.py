#!/usr/bin/env python3

import logging, json, enum

class Collection(object):
    def __init__(self, level=None, handler=None):
        self._replacements = {}

        if not handler:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(levelname)s - %(name)s - %(message)s"))

        self._logger = logging.getLogger(__name__)

        if level:
            handler.setLevel(level)
            self._logger.setLevel(level)

        self._logger.addHandler(handler)

    def add(self, key, value):
        """Create a new substitution that replaces instances of the specified key with a given value."""

        if key in self._replacements:
            self._logger.info(f"Substitution with key '{key}' will been redefined")

        self._replacements[key] = value
        self._logger.info(f"Created new substitution with key '{key}'")

    def addByFile(self, key, path):
        """Read the file at the specified path and use the data read as the value for a new substitution with the specified key."""

        with open(path) as f:
            data = f.read()
            self._logger.info(f"Loaded value for substitution with key '{key}' from file at path '{path}'")
            self.add(key, data)

    def addMultiple(self, dictionary):
        """Create multiple substitutions using a given dictionary."""

        self._logger.info(f"Adding multiple substitutions via dictionary: {dictionary}")

        for key, value in dictionary.items():
            self.add(key, value)

    def evaluate(self, data, params={}):
        """Return the given input data after any and all substitutions have been applied."""

        # TODO: Implement this method in C for performance boost?

        state = _State.INITIAL
        output = ""
        name = ""
        argKey = ""
        args = {}
        nestingLevel = 0

        for index, char in enumerate(data):
            self._logger.debug(f"Char: '{char}' State: {state}")

            if state == _State.INITIAL:
                if char == "{":
                    state = _State.OPEN_BRACKET
                else:
                    output += char

            elif state == _State.OPEN_BRACKET:
                if char == "{":
                    self._logger.debug(f"Identified command at input position {index}")
                    state = _State.NAME
                else:
                    output += "{" + char
                    state = _State.INITIAL

            elif state == _State.NAME:
                if char == ":":
                    name = name.strip()
                    self._logger.debug(f"Substitution for '{name}' command has arguments")
                    state = _State.ARG_KEY
                elif char == "}":
                    state = _State.NAME_CLOSE_BRACKET
                else:
                    name += char

            elif state == _State.NAME_CLOSE_BRACKET:
                if char == "}":
                    name = name.strip()

                    output += self._lookup(name, params)

                    self._logger.debug(f"Reached end of subtitution call '{name}' without arguments")

                    state = _State.INITIAL
                    name = ""
                else:
                    name += "}" + char

            elif state == _State.ARG_KEY:
                if char == "=":
                    argKey = argKey.strip()
                    args[argKey] = ""

                    self._logger.debug(f"Argument with key '{argKey}' encountered")

                    state = _State.ARG_VALUE
                else:
                    argKey += char

            elif state == _State.ARG_VALUE:
                if char == "&":
                    if nestingLevel == 0:
                        self._logger.debug(f"Value of argument '{argKey}' set to '{args[argKey]}' - moving onto the next argument")

                        argKey = ""
                        state = _State.ARG_KEY
                    else:
                        self._logger.debug("Moving onto next argument in nested substitution command")
                        args[argKey] += char

                elif char == "}":
                    state = _State.ARG_VALUE_CLOSE_BRACKET
                elif char == "{":
                    state = _State.ARG_VALUE_OPEN_BRACKET
                else:
                    args[argKey] += char


            elif state == _State.ARG_VALUE_OPEN_BRACKET:
                if char == "{":
                    args[argKey] += "{"

                    nestingLevel += 1
                    state = _State.ARG_VALUE

                    self._logger.debug(f"Level of nesting (command contained within argument value to another command) increased to {nestingLevel}")

                args[argKey] += char

            elif state == _State.ARG_VALUE_CLOSE_BRACKET:
                if char == "}":
                    if nestingLevel == 0:
                        self._logger.debug(f"Value of final argument '{argKey}' set to '{args[argKey]}'")

                        output += self._lookup(name, params, args)

                        self._logger.debug(f"Reached end of substitution call '{name}' with arguments {args}")

                        state = _State.INITIAL
                        name = ""
                        argKey = ""
                        args = {}

                    else:
                        nestingLevel -= 1
                        self._logger.debug("End of command nested within argument value")

                        state = _State.ARG_VALUE

                        args[argKey] += "}" + char

        return output

    def evaluateByFile(self, path):
        """Open and the file at the given path and evaluate any substitutions contained within."""

        with open(path) as f:
            data = f.read()
            self._logger.info(f"Loaded data to be evaluated from file at path '{path}'")
            return self.evaluate(data)

        return ""

    def _lookup(self, name, params, args={}):
        if name in self._replacements:
            value = self._replacements[name]
            self._logger.info(f"Substitution for '{name}' found: {value}")

        elif name in params:
            value = params[name]
            self._logger.info(f"Substitution for '{name}' found in local parameters: {value}")

        else:
            self._logger.warn(f"Substition for '{name}' does not exist!")
            return ""

        return self.evaluate(value, args)

class _State(enum.Enum):
    INITIAL = enum.auto()
    OPEN_BRACKET = enum.auto()
    NAME = enum.auto()
    NAME_CLOSE_BRACKET = enum.auto()
    ARG_KEY = enum.auto()
    ARG_VALUE = enum.auto()
    ARG_VALUE_OPEN_BRACKET = enum.auto()
    ARG_VALUE_CLOSE_BRACKET = enum.auto()
