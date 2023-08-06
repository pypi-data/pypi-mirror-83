# -*- coding: utf-8 -*-
"""
File that contains the tests for the pyls plugin esc-ls.

Created on Fri Jul 10 09:53:57 2020

@author: Richard Kellnberger
"""
from esc_ls import plugin

TEST_LINE_NOTHING = 'Not str literal in this line'
TEST_LINE_R = 'if secondaryGroup == r"\\x" or secondaryGroup[-1].isdigit():'
TEST_LINE_KNOWN = ('print("\\n")')
TEST_LINE_UNKNOWN = ('print("a\\e")')
TEST_LINE_UNUNKNOWN = ('print("\\s")')


class FakeConfig(object):

    def __init__(self):
        self._root_path = "C:"

    def plugin_settings(self, plugin, document_path=None):
        return {}


def test_parse_line_UNKNOWN():
    diags = plugin.parse_line(TEST_LINE_UNKNOWN, 0)
    assert len(diags) == 1
    assert diags[0]["source"] == "esc"
    assert diags[0]["message"] == ("The escape sequence '\\e' does not exist in python, "
                                   "consider using '\\x1B' instead.")
    assert diags[0]["severity"] == 1


def test_parse_line_UNUNKNOWN():
    diags = plugin.parse_line(TEST_LINE_UNUNKNOWN, 0)
    assert len(diags) == 1
    assert diags[0]["source"] == "esc"
    assert diags[0]["message"] == "The escape sequence '\\s' is unknown. It may or may not exist."
    assert diags[0]["severity"] == 2


def test_parse_line_nothing():
    diags = plugin.parse_line(TEST_LINE_NOTHING, 0)
    assert diags == []


def test_parse_line_r():
    diags = plugin.parse_line(TEST_LINE_R, 0)
    assert diags == []


def test_parse_line_known():
    diags = plugin.parse_line(TEST_LINE_KNOWN, 0)
    assert diags == []
