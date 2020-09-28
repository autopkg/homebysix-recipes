#!/usr/local/autopkg/python
#
# Based on AppDmgVersioner, Copyright 2010 Per Olofsson
# Adapted to use Foundation, 2020 Graham Pugh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""See docstring for FoundationDmgVersioner class"""

import glob
import os.path

from autopkglib import ProcessorError  # pylint: disable=import-error
from autopkglib.DmgMounter import DmgMounter  # pylint: disable=import-error
# PyLint cannot properly find names inside Cocoa libraries, so issues bogus
# No name 'Foo' in module 'Bar' warnings. Disable them.
# pylint: disable=E0611
from Foundation import (
    NSData,
    NSPropertyListMutableContainers,
    NSPropertyListSerialization,
    NSPropertyListXMLFormat_v1_0,
)

# pylint: enable=E0611

# Disable PyLint complaining about 'invalid' camelCase names
# pylint: disable=C0103


__all__ = ["FoundationDmgVersioner"]


class FoundationDmgVersioner(DmgMounter):
    # we dynamically set the docstring from the description (DRY), so:
    description = "Extracts bundle ID and version of app inside dmg."
    input_variables = {
        "dmg_path": {
            "required": True,
            "description": "Path to a dmg containing an app.",
        }
    }
    output_variables = {
        "app_name": {
            "description": (
                "Name of app found at the root of the disk image. This does not search "
                "recursively for a matching app. If you need to specify a path, use "
                "Versioner instead."
            )
        },
        "bundleid": {"description": "Bundle identifier of the app."},
        "version": {"description": "Version of the app."},
    }

    __doc__ = description

    def readPlist(self, filepath):
        """
        Read a .plist file from filepath.  Return the unpacked root object
        (which is usually a dictionary).
        """
        plistData = NSData.dataWithContentsOfFile_(filepath)
        (
            dataObject,
            dummy_plistFormat,
            error,
        ) = NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(
            plistData, NSPropertyListMutableContainers, None, None
        )
        if dataObject is None:
            if error:
                error = error.encode("ascii", "ignore")
            else:
                error = "Unknown error"
            errmsg = "%s in file %s" % (error, filepath)
            raise ProcessorError(errmsg)
        else:
            return dataObject

    def readPlistFromString(self, data):
        """Read a plist data from a string. Return the root object."""
        try:
            plistData = memoryview(data)
        except TypeError as err:
            raise ProcessorError(err)
        (
            dataObject,
            dummy_plistFormat,
            error,
        ) = NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(
            plistData, NSPropertyListMutableContainers, None, None
        )
        if dataObject is None:
            if error:
                error = error.encode("ascii", "ignore")
            else:
                error = "Unknown error"
            raise ProcessorError(error)
        else:
            return dataObject

    def find_app(self, path):
        """Find app bundle at path."""
        apps = glob.glob(os.path.join(path, "*.app"))
        if len(apps) == 0:
            raise ProcessorError("No app found in dmg")
        return apps[0]

    def read_bundle_info(self, path):
        """Read Contents/Info.plist inside a bundle."""

        plistpath = os.path.join(path, "Contents", "Info.plist")
        try:
            info = self.readPlist(plistpath)
        except Exception as error:
            raise ProcessorError(f"Can't read {plistpath}: {error}")
        return info

    def main(self):
        # Mount the image.
        mount_point = self.mount(self.env["dmg_path"])
        # Wrap all other actions in a try/finally so the image is always
        # unmounted.
        try:
            app_path = self.find_app(mount_point)
            info = self.read_bundle_info(app_path)
            self.env["app_name"] = os.path.basename(app_path)
            try:
                self.env["bundleid"] = info["CFBundleIdentifier"]
                self.env["version"] = info["CFBundleShortVersionString"]
                self.output(f"BundleID: {self.env['bundleid']}")
                self.output(f"Version: {self.env['version']}")
            except BaseException as err:
                raise ProcessorError(err)
        finally:
            self.unmount(self.env["dmg_path"])


if __name__ == "__main__":
    PROCESSOR = FoundationDmgVersioner()
    PROCESSOR.execute_shell()
