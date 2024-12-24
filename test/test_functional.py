# -*- coding: utf-8 -*-

"""test_functional.py.

Functional tests for homebysix-recipes.
"""


import os
import plistlib
import shutil
import subprocess

from nose.tools import (
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

# Skip run if the recipe contains these processors.
PROCESSOR_EXCEPTIONS = ("PackageRequired", "DeprecationWarning")

# Path to the AutoPkg binary.
AUTOPKG = "/usr/local/bin/autopkg"

# Path to the AutoPkg cache.
AUTOPKG_CACHE = os.path.expanduser("~/Library/AutoPkg/Cache")


def check_recipe(relpath, recipe):
    """Parse the recipe and make sure it's valid."""
    assert_is_instance(recipe, dict, f"{relpath}: recipe is not a dict")
    assert_in("Identifier", recipe, f"{relpath}: no Identifier key")
    assert_true(
        recipe["Identifier"].startswith(IDENTIFIER_PREFIX)
        or recipe["Identifier"] in IDENTIFIER_EXEMPTIONS,
        f"{relpath}: does not start with {IDENTIFIER_PREFIX}",
    )
    assert_in("Input", recipe, f"{relpath}: no Input key")
    assert_in("Process", recipe, f"{relpath}: no Process key")
    assert_not_in(
        "ParentRecipeTrustInfo",
        recipe,
        f"{relpath}: has ParentRecipeTrustInfo key",
    )


def clear_cache(identifier):
    """Clear AutoPkg cache for a specific recipe."""
    recipe_cache = os.path.join(AUTOPKG_CACHE, identifier)
    if os.path.isdir(recipe_cache):
        shutil.rmtree(recipe_cache, ignore_errors=True)


def run_recipe(relpath, recipe):
    """Run the recipe and check the exit code."""

    # Skip any recipe that contains certain processors
    for proc_exc in PROCESSOR_EXCEPTIONS:
        if proc_exc in [x["Processor"] for x in recipe.get("Process", [{}])]:
            print(f"Skipping due to {proc_exc}.")
            return

    proc = subprocess.run(
        [
            AUTOPKG,
            "info",
            relpath,
            "--pull",
            "--quiet",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert_equal(
        proc.returncode,
        0,
        f"{relpath}: autopkg info exited with code {proc.returncode}",
    )
    proc = subprocess.run(
        [
            AUTOPKG,
            "run",
            relpath,
            "--report-plist=test/report.plist",
            "--quiet",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert_equal(
        proc.returncode,
        0,
        f"{relpath}: autopkg run exited with code {proc.returncode}",
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
            elif filename.endswith(
                tuple("." + x + ".recipe.yaml" for x in recipe_types)
            ):
                recipe_paths.append(os.path.join(root, filename))
            elif filename.endswith(
                tuple("." + x + ".recipe.plist" for x in recipe_types)
            ):
                recipe_paths.append(os.path.join(root, filename))

    # Check and run each recipe we found.
    for index, recipe_path in enumerate(recipe_paths):
        print(f"Testing {recipe_path} ({index + 1} of {len(recipe_paths)})...")
        with open(recipe_path, "rb") as infile:
            recipe = plistlib.load(infile)
        yield check_recipe, recipe_path, recipe
        clear_cache(recipe["Identifier"])
        yield run_recipe, recipe_path, recipe
        clear_cache(recipe["Identifier"])
