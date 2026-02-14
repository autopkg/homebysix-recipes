#
# Copyright 2015-2020 Elliot Jordan
# Based on original processor by Nick Gamewell
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

# pylint: disable=unused-import
from autopkglib import ProcessorError, URLGetter  # noqa: F401

__all__ = ["AnytypeURLProvider"]

BASE_URL = "https://publish-releases.anytype.io/api/v1/latestRelease"


class AnytypeURLProvider(URLGetter):
    """Provides a download URL and build number for the latest Anytype
    release."""

    input_variables = {
        "base_url": {
            "required": False,
            "description": "URL for the Anytype releases JSON feed. "
            f"Default is {BASE_URL}.",
        },
        "ARCH": {
            "required": False,
            "description": "Architecture to look for in the JSON feed. "
            "Supported values include 'arm64' (Apple Silicon) and 'x64' (Intel). "
            "Default is 'arm64'.",
        },
    }
    output_variables = {
        "url": {"description": "URL to the latest Anytype release."},
        "version": {"description": "Version of the latest Anytype release."},
    }
    description = __doc__

    def get_release_info(self, base_url):
        """Process the JSON data from the latest release."""

        # Download JSON feed (or gzipped JSON feed) to a file.
        json_feed = self.download(base_url)
        feed_data = json.loads(json_feed)

        # Get version
        version = feed_data.get("DesktopLatestVersion")

        # Get URL for latest release for given architecture
        releases = feed_data.get("LatestReleasesLinks")
        arch = self.env.get("ARCH", "arm64")
        if arch == "x64":
            url = releases.get(f"MACOS_INTEL_{arch.upper()}", {}).get("url")
        else:
            url = releases.get(f"MACOS_{arch.upper()}", {}).get("url")
        if not url:
            raise ProcessorError(
                "No download URL for the latest release "
                f"found in the base_url JSON feed for {arch} architecture."
            )

        return url, version

    def main(self):
        """Main process."""

        base_url = self.env.get("base_url", BASE_URL)
        url, version = self.get_release_info(base_url)
        self.env["url"] = url
        self.output(f"Found URL: {self.env['url']}")
        self.env["version"] = version
        self.output(f"Version: {self.env['version']}")


if __name__ == "__main__":
    PROCESSOR = AnytypeURLProvider()
    PROCESSOR.execute_shell()
