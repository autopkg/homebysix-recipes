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

import re

# pylint: disable=unused-import
from autopkglib import APLooseVersion, ProcessorError, URLGetter

__all__ = ["PerforceURLProvider"]

# Base URL for the Perforce downloads host.
BASE_URL = "https://cdist2.perforce.com"

# Information about the directory listing URL, subdirectory hierarchy,
# and desired filename of each product.
PRODUCT_DETAILS = {
    "P4V": {
        "start": "perforce",
        "path": [
            r"r[\d\.]+/",  # Version number prefixed with "r"
            r"bin\.macosx[\w]+/",  # For example: "bin.macosx1015x86_64/"
            r"P4V\.dmg",  # Literal filename "P4V.dmg"
        ],
    },
    "HelixALM": {
        "start": "alm/helixalm",
        "path": [
            r"r[\d\.]+/",  # Version number prefixed with "r"
            r"ttmacclientinstall\.zip",  # Literal filename "ttmacclientinstall.zip"
        ],
    },
}


class PerforceURLProvider(URLGetter):
    """Provides a download URL for Perforce products. Currently only supports
    recent versions of P4V and HelixALM.
    """

    input_variables = {
        "product": {
            "required": False,
            "default": "P4V",
            "description": "Perforce product to provide a download URL for. "
            "'P4V' is the only supported value at this time.",
        }
    }
    output_variables = {
        "url": {"description": "URL to the latest P4V download."},
        "version": {"description": "Latest version of the product."},
    }
    description = __doc__

    def recurse_subdirs(self, path, url):
        """Recursively process web directory listings looking for matching
        paths, and when we have a match, return the URL."""

        # Add trailing slash to prevent constant 301 redirects.
        if not url.endswith("/"):
            url = url + "/"
        self.output(f"Searching {url} for {path[0]}")

        # Get content of directory listing and parse for links matching path regex.
        html = self.download(url, text=True)
        link_pattern = re.compile(f'<a href="({path[0]})">')
        links = re.findall(link_pattern, html)
        if len(links) == 0:
            # No match, toss back to parent caller and continue recursing.
            return None
        if len(links) == 1 and len(path) == 1:
            # We found a match, return the URL.
            return url + links[0]

        # Sort "r"-prefixed versions in reverse LooseVersion order before continuing.
        if path[0] == r"r[\d\.]+/":
            links = sorted(
                links, key=lambda x: APLooseVersion(x.lstrip("r")), reverse=True
            )

        # Recursively search each link in the directory listing.
        for link in links:
            result = self.recurse_subdirs(path[1:], url + link)
            if result:
                return result

        return None

    def main(self):
        """Main process."""

        info = PRODUCT_DETAILS[self.env["product"]]
        url = self.recurse_subdirs(info["path"], BASE_URL + "/" + info["start"])
        if not url:
            raise ProcessorError(
                f"Did not find a matching download URL for {self.env['product']}."
            )
        self.env["url"] = url
        self.output(f"Found url: {self.env['url']}")


if __name__ == "__main__":
    PROCESSOR = PerforceURLProvider()
    PROCESSOR.execute_shell()
