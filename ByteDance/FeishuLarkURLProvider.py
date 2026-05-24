#!/usr/local/autopkg/python
#
# Copyright 2026 Elliot Jordan
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

"""Provides download URL and version for the latest Feishu (Lark) release."""

import json
import re
import ssl
from urllib.request import urlopen

import certifi
from autopkglib import Processor, ProcessorError

__all__ = ["FeishuLarkURLProvider"]

DOWNLOAD_API_URL = "https://www.feishu.cn/api/downloads"

ARCH_MAP = {
    "arm64": "MacOS_m1",
    "x86_64": "MacOS",
}


class FeishuLarkURLProvider(Processor):
    """Determines the latest version of Feishu (Lark) available for download.

    Returns the URL and version of the software.
    """

    description = __doc__
    input_variables = {
        "ARCH": {
            "required": False,
            "default": "arm64",
            "description": (
                "Architecture to download. "
                "Supported values: arm64 (default), x86_64."
            ),
        },
    }
    output_variables = {
        "url": {"description": "Download URL for the latest Feishu (Lark) release."},
        "version": {"description": "Version of the latest Feishu (Lark) release."},
    }

    def main(self):
        """Main process."""
        arch = self.env.get("ARCH") or self.input_variables["ARCH"]["default"]
        api_key = ARCH_MAP.get(arch)
        if not api_key:
            raise ProcessorError(
                f"Unsupported ARCH value: {arch}. Use arm64 or x86_64."
            )

        self.output(f"Query URL: {DOWNLOAD_API_URL}", 3)
        self.output(f"Architecture: {arch} -> API key: {api_key}", 3)

        try:
            with urlopen(
                DOWNLOAD_API_URL,
                context=ssl.create_default_context(cafile=certifi.where()),
            ) as response:
                data = json.loads(response.read())
        except Exception as e:
            raise ProcessorError(f"Failed to fetch {DOWNLOAD_API_URL}: {e}") from e

        try:
            release = data["versions"][api_key]
            self.env["url"] = release["download_link"]
            version_str = release["version_number"]
        except KeyError as e:
            raise ProcessorError(
                f"Unexpected API response structure (missing key {e}). "
                f"Top-level keys: {list(data.keys())}"
            ) from e

        # version_number format: "MacOS-Apple@V7.68.6" or "MacOS-Intel@V7.68.6"
        match = re.search(r"@[Vv]?(\d+[\d.]*\d+)$", version_str)
        if not match:
            raise ProcessorError(f"Could not extract version from: {version_str}")
        self.env["version"] = match.group(1)

        self.output(f"Found URL: {self.env['url']}")
        self.output(f"Found version: {self.env['version']}")


if __name__ == "__main__":
    PROCESSOR = FeishuLarkURLProvider()
    PROCESSOR.execute_shell()
