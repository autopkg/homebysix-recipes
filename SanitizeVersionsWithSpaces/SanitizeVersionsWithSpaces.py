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

from autopkglib import Processor, ProcessorError


__all__ = ["SanitizeVersionsWithSpaces"]


class SanitizeVersionsWithSpaces(Processor):

    """For version numbers with spaces, this processor returns everything up
    to but not including the first space.

    Examples:
    - "3.0.8 :074a131:" --> "3.0.8"
    - "8.3.1.1 (154179)" --> "8.3.1.1"

    """

    input_variables = {
        "version": {
            "required": True,
            "description": "The version with spaces."
        }
    }
    output_variables = {
        "version": {
            "description": "The cleaned version."
        }
    }
    description = __doc__

    def main(self):
        """TBD"""

        self.env["version"] = self.env["version"].split(" ")[0]


if __name__ == "__main__":
    processor = SanitizeVersionsWithSpaces()
    processor.execute_shell()
