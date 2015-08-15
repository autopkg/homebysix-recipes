#!/usr/bin/python
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

import urllib2
import re
from autopkglib import Processor, ProcessorError

__all__ = ["TorBrowserBundleInfoProvider"]

class TorBrowserBundleInfoProvider(Processor):
    #pylint: disable=missing-docstring
    description = ("Get version and download URL for latest Tor Browser.")
    input_variables = {
        "language": {
            "required": False,
            "description": ("The part of the download filename which "
                            "represents the language (e.g. en-US).")
        },
        "include_prereleases": {
            "required": False,
            "description": ("If set to True or a non-empty value, include "
                            "prereleases.")
        }
    }
    output_variables = {
        "url": {
            "description": ("Download URL for the project's latest release.")
        },
        "version": {
            "description": ("The version number of the latest release. If "
                            "include_prereleases is true, this may be similar "
                            "to 5.5a1 or 5.0a4. Otherwise, similar to 5.0 or "
                            "4.5.3.")
        }
    }

    __doc__ = description


    def get_torbrowser_release(self, language, include_prereleases):
        """Return the URL and version of the latest Tor Broswer release."""

        # URL of directory index that lists Tor browser versions.
        # Include trailing slash.
        releases_url = "https://dist.torproject.org/torbrowser/"

        # The string that indicates a release listing in the HTML.
        marker = '<img src="/icons/folder.gif" alt="[DIR]">'

        # Prepare lists for storage of the parsed versions.
        all_versions = []
        stable_versions = []

        # Download the HTML of the releases page.
        try:
            html_string = urllib2.urlopen(releases_url).read()
        except Exception as err:
            raise ProcessorError("Couldn't load %s (%s)" % (releases_url, err))

        html_string = html_string.split("\n")

        # Look for lines containing a directory listing.
        for line in html_string:
            if marker in line:

                # Strip the version number out of the HTML.
                line = line.lstrip(marker)
                start = line.find('/">') + 3
                stop = line.find('/</a>')
                this_version = line[start:stop]

                # Stable versions go in stable_versions and all_versions.
                if re.match(r"^(?:(\d+\.(?:\d+\.)*\d+))$", this_version):
                    stable_versions.append(this_version)
                    all_versions.append(this_version)
                # Non-stable versions go in all_versions only.
                elif re.match(r"^(?:(\d+\.(?:\d+\.)*.+))$", this_version):
                    all_versions.append(this_version)

        # If we didn't find any versions at all, bail out.
        if not all_versions:
            raise ProcessorError("No Tor Browser versions of any kind were found at %s." % releases_url)

        # If we didn't find any stable versions (and stable versions were
        # requested), bail out.
        if include_prereleases and not stable_versions:
            raise ProcessorError("No stable Tor Browser versions were found at %s." % releases_url)

        # Calculate the latest version number using a simple sort.
        if include_prereleases:
            all_versions.sort()
            latest_version = all_versions[-1]
        else:
            stable_versions.sort()
            latest_version = stable_versions[-1]

        # Construct the URL using the version and language information.
        latest_url = "%s%s/TorBrowser-%s-osx64_%s.dmg" % (releases_url, latest_version, latest_version, language)

        # Put a stamp on it and drop it in the mailbox.
        return latest_version, latest_url


    def main(self):

        # Use input variables to get the latest Tor version and download URL.
        language = self.env.get("language")
        include_prereleases = self.env.get("include_prereleases")
        latest_version, latest_url = self.get_torbrowser_release(language, include_prereleases)

        # Store output variables.
        self.env["version"] = latest_version
        self.env["url"] = latest_url


if __name__ == '__main__':
    PROCESSOR = TorBrowserBundleInfoProvider()
    PROCESSOR.execute_shell()
