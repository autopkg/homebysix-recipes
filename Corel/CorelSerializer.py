# -*- coding: utf-8 -*-
#
# Copyright 2021 Elliot Jordan
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

import os
import plistlib
import subprocess

# pylint: disable=unused-import
from autopkglib import Processor, ProcessorError

__all__ = ["Processor"]


class CorelSerializer(Processor):
    """Given a Corel product serial number and full installer package, this
    processor uses the installer's create_dta command to create a DTA file.
    The path to the generated DTA file is provided as an output variable."""

    input_variables = {
        "serial_number": {
            "required": True,
            "description": "Serial number for the Corel product.",
        },
        "dta_path": {
            "required": False,
            "description": "Desired path for the generated DTA file. "
            "If not provided, defaults to %RECIPE_CACHE_DIR%/<productid>.dta",
        },
    }
    output_variables = {
        "dta_path": {"description": "Path to the generated DTA file."},
        "dta_installed_path": {
            "description": "Path to the installed destination for the DTA file."
        },
    }
    description = __doc__

    def license_info(self):
        """Return the product code and DTA file installed path for this Corel
        product by parsing the License.plist file in the Registration bundle."""

        license_path = (
            "%s/plugins/Registration.bundle/Contents/Resources/License.plist"
            % self.env["RECIPE_CACHE_DIR"]
        )
        with open(license_path, "rb") as openfile:
            license_info = plistlib.load(openfile)
        return license_info["ProductID"], license_info["DTAFileInstalledPath"]

    def main(self):
        """Main process."""

        if not os.path.isfile(self.env["flat_pkg_path"]):
            raise ProcessorError(
                "Provided flat_pkg_path does not exist: %s" % self.env["flat_pkg_path"]
            )

        create_dta = os.path.join(self.env["RECIPE_CACHE_DIR"], "plugins", "create_dta")
        product_code, dta_installed_path = self.license_info()
        dta_path = self.env.get(
            "dta_path",
            os.path.join(self.env["RECIPE_CACHE_DIR"], product_code + ".dta"),
        )
        subprocess.run([create_dta, self.env["serial_number"], dta_path], check=True)
        self.env["dta_path"] = dta_path
        self.env["dta_installed_path"] = dta_installed_path
        self.env["product_code"] = product_code
        self.output("Serialized DTA file: %s" % dta_path)


if __name__ == "__main__":
    PROCESSOR = CorelSerializer()
    PROCESSOR.execute_shell()
