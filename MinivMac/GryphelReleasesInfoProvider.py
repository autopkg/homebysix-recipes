#
# Copyright 2025 Elliot Jordan
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

from autopkglib import APLooseVersion, ProcessorError, URLGetter  # noqa: F401

__all__ = ["GryphelReleasesInfoProvider"]

# Base URL for page that lists available releases
BASE_URL = {
    "stable": "https://www.gryphel.com/c/minivmac/dnld_%s.html",
    "beta": "https://www.gryphel.com/c/minivmac/b_dl_%s.html",
}


class GryphelReleasesInfoProvider(URLGetter):
    """Provides a download URL and build number for the latest Mini vMac
    releases hosted on the gryphel.com website. Note that some combinations
    of variation and platform may not have releases available. Some releases
    for Mac may not be codesigned."""

    input_variables = {
        "channel": {
            "description": (
                "Release channel to use. Can be 'stable' or 'beta'. "
                "Default is 'stable'."
            ),
            "required": False,
            "default": "stable",
        },
        "variation": {
            "description": (
                "Mini vMac variation to find releases for. "
                "Can be 'std' for standard Macintosh Plus (default), "
                "'mii' for Macintosh II, or "
                "'128' for Macintosh 128K."
            ),
            "required": False,
            "default": "std",
        },
        "platform": {
            "description": (
                "Platform to find releases for. "
                "Use 'mc64' for Apple Silicon Macs (default), "
                "'imch' for Intel Macs. Untested values include "
                "'wx86' for Windows, "
                "'lx86' for Linux, "
                "'fb64' for FreeBSD, "
                "'nb64' for NetBSD, "
                "'oi64' for OpenIndiana, and "
                "'wear' for Windows Mobile 5.0."
            ),
            "required": False,
            "default": "mc64",
        },
        "get_inf_txt": {
            "description": "Whether to attempt to retrieve and parse the .inf.txt file for additional metadata.",
            "required": False,
            "default": False,
        },
    }
    output_variables = {
        "url": {"description": "URL to the download the specified Mini vMac release."},
        "version": {"description": "Version of the specified Mini vMac release."},
        # Provided by .inf.txt files linked from the download page
        "filename": {
            "description": "Filename of the specified Mini vMac release. "
            "Only provided if 'get_inf_txt' is True."
        },
        "size_bytes": {
            "description": "Size of the download in bytes. "
            "Only provided if 'get_inf_txt' is True."
        },
        "md5_checksum": {
            "description": "MD5 checksum of the download. "
            "Only provided if 'get_inf_txt' is True."
        },
    }
    description = __doc__

    def main(self):
        """Main process."""

        # Set release channel, variation, and platform
        # If an invalid value is provided, a 404 error will occur later
        channel = self.env.get("channel", "stable").lower()
        variation = self.env.get("variation", "std").lower()
        platform = self.env.get("platform", "mc64").lower()

        # Get contents of download page
        download_page = self.download(BASE_URL[channel] % variation, text=True)

        # Match pattern for download links
        pattern = re.compile(
            r'/d/minivmac/minivmac-[\d\.]+/minivmac-(?P<version>[\d\.]+)-%s\.bin\.(?P<ext>tgz|zip)"'
            % platform
        )
        matches = pattern.findall(download_page)
        if not matches:
            raise ProcessorError(
                f"Could not find any matching Mini vMac releases for "
                f"variation '{variation}' on platform '{platform}' "
                f"in channel '{channel}'."
            )
        print(
            f"Found {len(matches)} matching releases for "
            f"variation '{variation}' on platform '{platform}' "
            f"in channel '{channel}'."
        )

        # Provide URL and version for latest release
        latest_version = sorted([match[0] for match in matches], key=APLooseVersion)[-1]
        latest_ext = [match[1] for match in matches if match[0] == latest_version][0]
        print(f"Latest version is {latest_version}.")
        self.env["url"] = (
            f"https://www.gryphel.com/d/minivmac/minivmac-{latest_version}/minivmac-{latest_version}-{platform}.bin.{latest_ext}"
        )
        self.env["version"] = latest_version


if __name__ == "__main__":
    PROCESSOR = GryphelReleasesInfoProvider()
    PROCESSOR.execute_shell()
