#!/usr/bin/env python
#
# Copyright 2015-2020 Elliot Jordan
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

from autopkglib import Processor, ProcessorError  # noqa: F401

__all__ = ["VersionSplitter"]


class VersionSplitter(Processor):
    """This processor splits version numbers and returns the specified index.
    By default, it splits using a space, and returns the first item. Default
    behavior example: "3.0.8 :074a131:" --> "3.0.8".

    More examples (with "split_on" in parentheses and "index" in brackets):
    - "8.3.1.1 (154179)" --> (" ")[0] -->"8.3.1.1"
    - "1.3.1-stable" --> ("-")[0] -->"1.3.1"
    - "macosx_64bit_3.0" --> ("_")[2] -->"3.0"
    """

    input_variables = {
        "version": {
            "required": True,
            "description": "The version string that needs splitting.",
        },
        "split_on": {
            "required": False,
            "description": "The character(s) to use for splitting the "
            "version. (Defaults to a space.)",
        },
        "index": {
            "required": False,
            "description": "The index of the version string to be "
            "returned. (Defaults to 0.)",
        },
    }
    output_variables = {"version": {"description": "The cleaned up version string."}}
    description = __doc__

    def main(self):
        """Main process."""

        split_on = self.env.get("split_on", " ")
        index = self.env.get("index", 0)
        self.env["version"] = self.env["version"].split(split_on)[index]
        self.output("Split version: {}".format(self.env["version"]))


if __name__ == "__main__":
    PROCESSOR = VersionSplitter()
    PROCESSOR.execute_shell()
