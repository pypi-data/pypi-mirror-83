# -*- coding: utf-8 -*-
"""
File that contains the pyls plugin esc-ls.

Created on Fri Jul 10 09:53:57 2020

@author: Richard Kellnberger
"""
import re
import os
import os.path
import logging
from pyls import hookimpl
from pyls.workspace import Document, Workspace
from pyls.config.config import Config
from typing import Optional, Dict, Any, List

linePattern: str = (r'([^r]"{3}.*"{3})|([^r]"(?:(?:\\")|[^"])*")|'
                    r"([^r]'{3}.*'{3})|([^r]'(?:(?:\\')|[^'])*')")
secondaryLinePattern: str = r"""[^\\](?:\\{2})*(\\[^"'\\nrtbf])"""

regex = re.compile(linePattern)
secondaryRegex = re.compile(secondaryLinePattern)

log = logging.getLogger(__name__)

unknownSequences: Dict[str, str] = {r"\a": r"\x07", r"\e": r"\x1B", r"\v": r"\x0B"}


def parse_line(line: str, lineNumber: int) -> List[Dict[str, Any]]:
    """
    Return a language-server diagnostic from a line of file.

    Parameters
    ----------
    line : str
        Line of the document to be analysed.

    Returns
    -------
    Optional[List[Dict[str, Any]]]
        The list of dicts with the lint data.

    """
    diags = []
    for found in regex.finditer(line):
        group = found.group()
        span = found.span()
        for escape in secondaryRegex.finditer(group):
            secondaryGroup = escape.group(1)
            if secondaryGroup == r"\\x" or secondaryGroup[-1].isdigit():
                # Probably valid hex or oct
                continue
            severity = 2
            message = f"The escape sequence '{secondaryGroup}' is unknown. It may or may not exist."
            secondarySpan = escape.span()
            if secondaryGroup in unknownSequences:
                severity = 1
                message = (f"The escape sequence '{secondaryGroup}' does not exist in python, "
                           f"consider using '{unknownSequences[secondaryGroup]}' instead.")
            diags.append({'source': 'esc',
                          'range': {
                              'start':
                                  {'line': lineNumber, 'character': span[0]+secondarySpan[0]+1},
                              'end':
                                  {'line': lineNumber, 'character': span[0]+secondarySpan[1]}
                              },
                          'message': message,
                          'severity': severity
                          })
    return diags


@hookimpl
def pyls_lint(config: Config, workspace: Workspace, document: Document,
              is_saved: bool) -> List[Dict[str, Any]]:
    """
    Lints.

    Parameters
    ----------
    config : Config
        The pyls config.
    workspace : Workspace
        The pyls workspace.
    document : Document
        The document to be linted.
    is_saved : bool
        Weather the document is saved.

    Returns
    -------
    List[Dict[str, Any]]
        List of the linting data.

    """
    diagnostics = []
    lines: List[str] = document.source.splitlines()
    for i in range(len(lines)):
        diag = parse_line(lines[i], i)
        if diag:
            diagnostics.extend(diag)

    return diagnostics


@hookimpl
def pyls_settings(config: Config) -> Dict[str, Dict[str, Dict[str, str]]]:
    """
    Read the settings.

    Parameters
    ----------
    config : Config
        The pyls config.

    Returns
    -------
    Dict[str, Dict[str, Dict[str, str]]]
        The config dict.

    """
    configuration = init(config._root_path)
    return {"plugins": {"esc-ls": configuration}}


def init(workspace: str) -> Dict[str, str]:
    """
    Find plugin config file.

    Parameters
    ----------
    workspace : str
        The path to the current workspace.

    Returns
    -------
    Dict[str, str]
        The plugin config dict.

    """
    # On windows the path contains \\ on linux it contains / all the code works with /
    workspace = workspace.replace("\\", "/")
    configuration = {}
    path = findConfigFile(workspace, "esc-ls.cfg")
    if path:
        with open(path) as file:
            configuration = eval(file.read())
    return configuration


def findConfigFile(path: str, name: str) -> Optional[str]:
    """
    Search for a config file.

    Search for a file of a given name from the directory specifyed by path through all parent
    directories. The first file found is selected.

    Parameters
    ----------
    path : str
        The path where the search starts.
    name : str
        The file to be found.

    Returns
    -------
    Optional[str]
        The path where the file has been found or None if no matching file has been found.

    """
    while True:
        p = f"{path}/{name}"
        if os.path.isfile(p):
            return p
        else:
            loc = path.rfind("/")
            if loc == -1:
                return None
            path = path[:loc]
