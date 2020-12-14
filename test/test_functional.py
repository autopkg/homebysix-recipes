#!/usr/bin/python
"""test_functional.py.

Functional tests for homebysix-recipes.
"""


import os
import plistlib
import shutil
import subprocess

from nose.tools import (  # assert_false,
    assert_equal,
    assert_in,
    assert_is_instance,
    assert_not_in,
    assert_true,
)

# Desired identifier prefix, with few exceptions.
IDENTIFIER_PREFIX = "com.github.homebysix."
IDENTIFIER_EXEMPTIONS = (
    "com.github.jps3.download.Kitematic",
    "com.github.jps3.pkg.Kitematic",
)

# Path to the AutoPkg cache.
AUTOPKG_CACHE = os.path.expanduser("~/Library/AutoPkg/Cache")


def check_recipe(relpath, recipe):
    """Parse the recipe and make sure it's valid."""
    assert_is_instance(recipe, dict, "{}: recipe is not a dict".format(relpath))
    assert_in("Identifier", recipe, "{}: no Identifier key".format(relpath))
    assert_true(
        recipe["Identifier"].startswith(IDENTIFIER_PREFIX)
        or recipe["Identifier"] in IDENTIFIER_EXEMPTIONS,
        "{}: does not start with {}".format(relpath, IDENTIFIER_PREFIX),
    )
    assert_in("Input", recipe, "{}: no Input key".format(relpath))
    assert_in("Process", recipe, "{}: no Process key".format(relpath))
    assert_not_in(
        "ParentRecipeTrustInfo",
        recipe,
        "{}: has ParentRecipeTrustInfo key".format(relpath),
    )


def clear_cache(identifier):
    """Clear AutoPkg cache for a specific recipe."""
    recipe_cache = os.path.join(AUTOPKG_CACHE, identifier)
    if os.path.isdir(recipe_cache):
        shutil.rmtree(recipe_cache, ignore_errors=True)


def run_recipe(relpath):
    """Run the recipe and check the exit code."""
    retcode = subprocess.call(
        ["/usr/local/bin/autopkg", "info", relpath, "--pull", "--quiet",]
    )
    assert_equal(
        retcode, 0, "{}: autopkg info exited with code {}".format(relpath, retcode)
    )
    retcode = subprocess.call(
        [
            "/usr/local/bin/autopkg",
            "run",
            relpath,
            "--report-plist=test/report.plist",
            "--quiet",
        ]
    )
    assert_equal(
        retcode, 0, "{}: autopkg run exited with code {}".format(relpath, retcode)
    )


def test_functional():
    """Functional tests."""

    # Types of recipes we are targeting for testing. (Recommend "download" and "pkg" only.)
    recipe_types = ("download", "pkg")

    # Walk our repo and collect each recipe matching the above types.
    recipe_paths = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for filename in files:
            if filename.endswith(tuple("." + x + ".recipe" for x in recipe_types)):
                recipe_paths.append(os.path.join(root, filename))

    # Check and run each recipe we found.
    for index, recipe_path in enumerate(recipe_paths):
        print(
            "Testing {} ({} of {})...".format(recipe_path, index + 1, len(recipe_paths))
        )
        recipe = plistlib.readPlist(recipe_path)
        yield check_recipe, recipe_path, recipe
        clear_cache(recipe["Identifier"])
        yield run_recipe, recipe_path
        clear_cache(recipe["Identifier"])
