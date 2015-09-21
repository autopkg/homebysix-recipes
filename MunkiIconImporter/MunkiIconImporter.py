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
            "required": True,
            "description": "Path to the icon to be copied into the Munki "
                           "repository. Default is %NAME%.png."
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
        source_icon = self.env["source_icon"]
        munki_repo = self.env["munki_repo"]

        shutil.copy(source_icon, os.path.join(munki_repo, "icons"))


if __name__ == "__main__":
    processor = MunkiIconImporter()
    processor.execute_shell()
