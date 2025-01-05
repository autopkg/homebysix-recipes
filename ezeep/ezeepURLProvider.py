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

import json

# pylint: disable=unused-import
from autopkglib import ProcessorError, URLGetter

__all__ = ["ezeepURLProvider"]

# API gateway ezeep uses to provide download URLs for updates
UPDATE_API = "https://sidetrack.ezeep.com/updater/check"


class ezeepURLProvider(URLGetter):
    """Provides a download URL for the latest ezeep product release."""

    input_variables = {
        "application": {
            "required": False,
            "description": "Bundle identifier of ezeep app to provide URL for. "
            "Defaults to 'com.ezeep.clients.mac'.",
        },
        "os_version": {
            "required": False,
            "description": "OS version to provide to ezeep updates API. "
            "Defaults to '10.15.7'.",
        },
        "channel": {
            "required": False,
            "description": "Update channel to provide to ezeep updates API. "
            "Defaults to 'live'.",
        },
        "platform": {
            "required": False,
            "description": "Platform to provide to ezeep updates API. "
            "Defaults to 'mac'.",
        },
    }
    output_variables = {
        "url": {"description": "URL to the latest ezeep release."},
        "version": {"description": "Version of the latest ezeep release."},
    }
    description = __doc__

    def main(self):
        """Main process."""

        # Read input variables
        data = {
            "application": self.env.get("application", "com.ezeep.clients.mac"),
            "os_version": self.env.get("os_version", "10.15.7"),
            "channel": self.env.get("channel", "live"),
            "platform": self.env.get("platform", "mac"),
        }

        # Prepare curl command
        curl_cmd = (
            self.curl_binary(),
            "--url",
            UPDATE_API,
            "--location",
            "-H",
            "Content-Type: application/json",
            "-X",
            "POST",
            "--data-binary",
            json.dumps(data),
        )

        # Call API to retrieve update info
        response = self.download_with_curl(curl_cmd)
        if not response:
            raise ProcessorError("No response from ezeep API.")

        # Set URL and version in environment
        self.env["url"] = json.loads(response).get("url")
        self.output(f"Found url: {self.env['url']}")
        self.env["version"] = json.loads(response).get("version")
        self.output(f"Found version: {self.env['version']}")


if __name__ == "__main__":
    PROCESSOR = ezeepURLProvider()
    PROCESSOR.execute_shell()
