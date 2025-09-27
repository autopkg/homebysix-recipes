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


from autopkglib import APLooseVersion, URLGetter  # noqa: F401

__all__ = ["CocktailReleasesInfoProvider"]

# Information about available Cocktail releases
ID_BASE = "com.maintain.cocktail"
RELEASES = {
    "10.10": {"filename": "Cocktail8YE.dmg", "bundle_id": f"{ID_BASE}.yosemite"},
    "10.11": {"filename": "Cocktail9ECE.dmg", "bundle_id": f"{ID_BASE}.elcapitan"},
    "10.12": {"filename": "Cocktail10SE.dmg", "bundle_id": f"{ID_BASE}.sierra"},
    "10.13": {"filename": "Cocktail11HSE.dmg", "bundle_id": f"{ID_BASE}.highsierra"},
    "10.14": {"filename": "Cocktail12ME.dmg", "bundle_id": f"{ID_BASE}.mojave12"},
    "10.15": {"filename": "Cocktail13CE.dmg", "bundle_id": f"{ID_BASE}.catalina13"},
    "11": {"filename": "Cocktail14BSE.dmg", "bundle_id": f"{ID_BASE}.bigsur14"},
    "12": {"filename": "Cocktail15ME.dmg", "bundle_id": f"{ID_BASE}.monterey15"},
    "13": {"filename": "Cocktail16VE.dmg", "bundle_id": f"{ID_BASE}.ventura165"},
    # Bundle ID says Ventura but it's the correct one for the Sonoma edition
    "14": {"filename": "Cocktail17SE.dmg", "bundle_id": f"{ID_BASE}.ventura165"},
    "15": {"filename": "Cocktail18SE.dmg", "bundle_id": f"{ID_BASE}.sequoia"},
    "26": {"filename": "Cocktail19TE.dmg", "bundle_id": f"{ID_BASE}.tahoe"},
}

# Base URL for downloading releases
BASE_URL = "https://www.maintain.se/downloads/"

# Default major version if none is provided
DEFAULT_MAJOR_VERSION = "26"


class CocktailReleasesInfoProvider(URLGetter):
    """Provides a download URL and build number for the latest Cocktail
    release."""

    input_variables = {
        "major_version": {
            "required": False,
            "description": "Major version of macOS for which to download a "
            f"compatible Cocktail release. Default is {DEFAULT_MAJOR_VERSION}.",
        }
    }
    output_variables = {
        "url": {
            "description": "URL to the download the latest specified Cocktail release."
        },
        "bundle_id": {
            "description": "Bundle identifier of the specified Cocktail release."
        },
        "cert_leaf_ou": {
            "description": "Certificate leaf identifier used for code signature verification."
        },
    }
    description = __doc__

    def main(self):
        """Main process."""

        # Set input variable
        major_version = self.env.get("major_version", DEFAULT_MAJOR_VERSION)

        # Determine and set output variables
        self.env["url"] = BASE_URL + RELEASES[major_version]["filename"]
        self.output(f"Found URL: {self.env['url']}")
        self.env["bundle_id"] = RELEASES[major_version]["bundle_id"]

        # Determine and set code signature verification cert leaf
        if APLooseVersion(major_version) < APLooseVersion("10.14"):
            self.env["cert_leaf_ou"] = "49Q84U5WS2"
        else:
            self.env["cert_leaf_ou"] = "HC63V5YZGB"


if __name__ == "__main__":
    PROCESSOR = CocktailReleasesInfoProvider()
    PROCESSOR.execute_shell()
