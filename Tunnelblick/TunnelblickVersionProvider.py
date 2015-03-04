#!/usr/bin/env/python
#
# Copyright 2015 Nick McSpadden
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from autopkglib import Processor, ProcessorError
import re

__all__ = ["TunnelblickVersionProvider"]


SANITIZE_PATTERN = "^\d+.\d+.\d+"

class TunnelblickVersionProvider(Processor):
    description = "Provides the version of the latest Chef client download."
    input_variables = {
        "input_version": {
            "required": True,
            "description": "Version string to parse for sanitizing."
        }
    }
    output_variables = {
        "version": {
            "description": "Sanitized version.",
        }
    }

    __doc__ = description

    def main(self):
        # Determine type, hashed, username and password.
        input_version = self.env.get("input_version")

        results = re.match(SANITIZE_PATTERN, input_version)

        self.env["version"] = results.group()

        self.output("Found version %s" % self.env["version"])


if __name__ == "__main__":
    processor = TunnelblickVersionProvider()
    processor.execute_shell()