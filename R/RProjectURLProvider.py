# -*- coding: utf-8 -*-
#
# Copyright 2022 Elliot Jordan
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

import re

# pylint: disable=unused-import
from autopkglib import ProcessorError, URLGetter

__all__ = ["RProjectURLProvider"]

# R project Mac downloads page
DL_PAGE = "https://cran.r-project.org/bin/macosx/"


class RProjectURLProvider(URLGetter):
    """Provides a download URL for the latest R Project
    (https://cran.r-project.org/) product release."""

    input_variables = {
        "architecture": {
            "required": False,
            "description": "Architecture of the R package to download. "
            "Possible values are 'x86_64' (Intel) or 'arm64' (Apple Silicon). "
            "Defaults to 'x86_64' (Intel).",
        },
    }
    output_variables = {
        "url": {"description": "URL to the latest R release."},
        "version": {"description": "Version of the latest R release."},
    }
    description = __doc__

    def main(self):
        """Main process."""

        # Read and validate input variables
        arch = self.env.get("architecture", "x86_64")
        if arch not in ("x86_64", "arm64"):
            raise ProcessorError("Architecture must be one of: x86_64, arm64")

        # Prepare regular expression
        if arch == "x86_64":
            pattern = r'base\/(?P<file>R-(?P<vers>[\d.]+)\.pkg)">R-[\d.]+\.pkg</a>'
            url_base = "https://cran.r-project.org/bin/macosx/base/"
        elif arch == "arm64":
            pattern = r'base\/(?P<file>R-(?P<vers>[\d.]+)-arm64\.pkg)">R-[\d.]+-arm64\.pkg</a>'
            url_base = "https://cran.r-project.org/bin/macosx/big-sur-arm64/base/"

        # Get and parse download page contents
        download_page_html = self.download(DL_PAGE, text=True)
        m = re.search(pattern, download_page_html)
        if not m:
            raise ProcessorError(f"No match found on {DL_PAGE}")

        # Set URL and version in environment
        self.env["url"] = url_base + m.groupdict()["file"]
        self.output("Found url: %s" % self.env["url"])
        self.env["version"] = m.groupdict()["vers"]
        self.output("Found version: %s" % self.env["version"])


if __name__ == "__main__":
    PROCESSOR = RProjectURLProvider()
    PROCESSOR.execute_shell()
