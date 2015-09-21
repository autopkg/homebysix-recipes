#!/usr/bin/env python
#
# Copyright 2015 Elliot Jordan
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
import shutil

from autopkglib import Processor, ProcessorError


__all__ = ["MunkiIconImporter"]


class MunkiIconImporter(Processor):
    """For a given recipe Foo.munki.recipe, the MunkiIconImporter processor
    copies a file called Foo.png to the "icons" folder in the local Munki
    repository.
    """

    input_variables = {
        "icon_path": {
            "required": False,
            "description": "Path to the icon to be copied into the Munki "
                           "repository. Defaults to "
                           "%RECIPE_DIR%/%NAME%.png."
        },
        "MUNKI_REPO": {
            "description": "Path to a mounted Munki repo.",
            "required": True
        }
    }
    output_variables = {}
    description = __doc__


    def main(self):
        """Copy the icon to the Munki repo."""

        icon_path = self.env.get("icon_path", os.path.join(self.env["RECIPE_DIR"], "%s.png" % self.env["NAME"]))
        munki_repo = self.env["MUNKI_REPO"]

        # Create icons folder in munki_repo, if it doesn't already exist.
        dest_dir = os.path.join(munki_repo, "icons")
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Copy the icon.
        shutil.copy(icon_path, os.path.join(dest_dir, "%s.png" % self.env["NAME"]))


if __name__ == "__main__":
    processor = MunkiIconImporter()
    processor.execute_shell()
