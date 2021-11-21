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
from distutils.version import LooseVersion

# pylint: disable=unused-import
from autopkglib import ProcessorError, URLGetter

__all__ = ["PerforceURLProvider"]

# Base URL for the Perforce downloads host.
BASE_URL = "https://cdist2.perforce.com"

# Information about the directory listing URL, subdirectory hierarchy,
# and desired filename of each product.
PRODUCT_DETAILS = {
    "P4V": {
        "start": "perforce",
        "path": [
            r"r[\d\.]+/",
            r"bin\.macosx[\w]+/",
            r"P4V\.dmg",
        ],
    },
    "HelixALM": {
        "start": "alm/helixalm",
        "path": [
            r"r[\d\.]+/",
            r"ttmacclientinstall\.zip",
        ],
    },
}


class PerforceURLProvider(URLGetter):
    """Provides a download URL for Perforce products. Currently only supports
    recent versions of P4V, but could be extended for HelixALM and others in
    the future.
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
        self.output("Searching %s for %s" % (url, path[0]))

        # Get content of directory listing and parse for links.
        html = self.download(url, text=True)
        link_pattern = re.compile('<a href="(%s)">' % path[0])
        links = re.findall(link_pattern, html)
        if len(links) == 0:
            # No match, toss back to parent caller and continue recursing.
            return None
        elif len(links) == 1 and len(path) == 1:
            # We found a match, return the URL.
            return url + links[0]

        # Sort versions in reverse LooseVersion order before continuing.
        if path[0] == r"r[\d\.]+/":
            links = sorted(
                links, key=lambda x: LooseVersion(x.lstrip("r")), reverse=True
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
                "Did not find a matching download URL for %s." % self.env["product"]
            )
        self.env["url"] = url
        self.output("Found url: %s" % self.env["url"])


if __name__ == "__main__":
    PROCESSOR = PerforceURLProvider()
    PROCESSOR.execute_shell()
