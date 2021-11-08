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

import json
from urllib.parse import urlparse

# pylint: disable=unused-import
from autopkglib import ProcessorError, URLGetter

__all__ = ["CorelURLProvider"]

# API gateway Corel uses to provide tokenized URLs to download packages
TOKEN_API = "https://i.installportal.com/v1/token"


class CorelURLProvider(URLGetter):
    """Provides a download URL for the latest Corel product release."""

    input_variables = {
        "url": {
            "required": True,
            "description": "Non-tokenized URL for the Corel product.",
        }
    }
    output_variables = {
        "url": {"description": "Tokenized URL to the latest Corel product release."},
        "filename": {"description": "Filename of the downloaded installer."},
    }
    description = __doc__

    def main(self):
        """Main process."""

        # Verify we have an input URL
        if not self.env.get("url").startswith("http"):
            raise ProcessorError("Non-tokenized URL for Corel product is required.")

        # Prepare curl command
        curl_cmd = (
            self.curl_binary(),
            "--url",
            TOKEN_API,
            "--location",
            "-X",
            "POST",
            "--data-binary",
            self.env["url"],
        )

        # Call API to retrieve tokenized product URL
        response = self.download_with_curl(curl_cmd)
        url = json.loads(response).get("tokenizedUrl")
        if not url:
            raise ProcessorError("Unable to get tokenized URL for provided product.")

        # Set URL in environment
        self.env["url"] = url
        self.env["filename"] = urlparse(url).path.split("/")[-1]


if __name__ == "__main__":
    PROCESSOR = CorelURLProvider()
    PROCESSOR.execute_shell()
