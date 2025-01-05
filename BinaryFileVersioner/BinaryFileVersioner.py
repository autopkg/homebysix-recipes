#
# Copyright 2018-2020 Elliot Jordan
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import subprocess

from autopkglib import Processor, ProcessorError  # noqa: F401

__all__ = ["BinaryFileVersioner"]


class BinaryFileVersioner(Processor):  # pylint: disable=invalid-name
    """This processor returns the version number of a binary file that has an
    embedded info plist."""

    input_variables = {
        "input_file_path": {
            "required": True,
            "description": "File path to a binary file (not app bundle).",
        },
        "plist_version_key": {
            "required": False,
            "description": "Which plist key to use. Defaults to CFBundleShortVersionString.",
        },
    }
    output_variables = {"version": {"description": "Version of the file."}}
    description = __doc__

    def main(self):
        """Main process."""

        if not os.path.isfile("/bin/launchctl"):
            raise ProcessorError("/bin/launchctl is not present on this Mac.")

        cmd = [
            "/bin/launchctl",
            "plist",
            "__TEXT,__info_plist",
            self.env["input_file_path"],
        ]
        proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
        if proc.returncode != 0:
            raise ProcessorError(f"/bin/launchctl failed with error: {proc.stderr}")

        version_key = self.env.get("plist_version_key", "CFBundleShortVersionString")
        pattern = f'"{version_key}" = "(.*)";'
        match = re.search(pattern, proc.stdout)

        if match:
            self.env["version"] = match.group(1)
            self.output(f"Found version: {self.env['version']}")
        else:
            raise ProcessorError(
                f"Unable to find a {self.env.get('plist_version_key', 'CFBundleShortVersionString')} "
                f"key in {self.env['input_file_path']}."
            )


if __name__ == "__main__":
    PROCESSOR = BinaryFileVersioner()
    PROCESSOR.execute_shell()
