#!/usr/bin/python
"""
test_functional.py

Functional tests for homebysix-recipes.
"""


import os
import plistlib
import subprocess

from nose.tools import *  # pylint: disable=W0401, W0614


def recipe_runner(relpath):
    """Given a relative path, run the recipe and return the exit code."""
    retcode = subprocess.call(
        [
            "/usr/local/bin/autopkg",
            "run",
            relpath,
            "--verbose",
            "--report-plist=test/report.plist",
        ]
    )
    return retcode


def check_recipe(relpath):
    """Verify the recipe run produces expected exitcode and results."""
    retcode = recipe_runner(relpath)
    assert_equal(retcode, 0)
    report = plistlib.readPlist("test/report.plist")
    assert_equal(report["failures"], [])


def test_functional():
    """Iterate through recipes in working directory and run tests on each."""

    # Types of recipes we are targeting for testing. (Recommend "download" and "pkg" only.)
    recipe_types = ("download", "pkg")

    # Walk our repo and check each recipe matching the above types.
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for filename in files:
            if filename.endswith(tuple("." + x + ".recipe" for x in recipe_types)):
                yield check_recipe, os.path.join(root, filename)
