#!/usr/bin/env python
#
# Copyright 2015 Elliot Jordan
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

import gzip
import json
import re
import StringIO
import urllib2

from autopkglib import Processor, ProcessorError


__all__ = ["GoToMeetingURLProvider"]


BASE_URL = "https://p5.osdimg.com/g2mupdater/live/config.json"


class GoToMeetingURLProvider(Processor):

    """Provides a download URL for the latest GoToMeeting release."""
    input_variables = {
        "base_url": {
            "required": False,
            "description": "Default is %s" % BASE_URL
        }
    }
    output_variables = {
        "url": {
            "description": "URL to the latest GoToMeeting release."
        },
        "build": {
            "description": "Build number of the latest GoToMeeting release."
        }
    }
    description = __doc__

    def get_g2m_json(self, base_url):
        request = urllib2.Request(base_url)
        request.add_header("Accept-Encoding", "gzip")
        opener = urllib2.build_opener()
        response = opener.open(request)

        # Sometimes the base URL is compressed as gzip, sometimes it's not.
        if response.info().get("Content-Encoding") == "gzip":
            self.output("Encoding: gzip")
            gzipData = StringIO.StringIO(response.read())
            jsonData = json.loads(gzip.GzipFile(fileobj=gzipData).read())
        else:
            self.output("Encoding: plaintext")
            jsonData = json.loads(response.read())

        return jsonData

    def get_g2m_url(self, jsonData):
        return jsonData["activeBuilds"][
            len(jsonData["activeBuilds"]) - 1]["macDownloadUrl"]

    def get_g2m_build(self, jsonData):
        return str(jsonData["activeBuilds"][
            len(jsonData["activeBuilds"]) - 1]["buildNumber"])

    def main(self):
        """Find and return a download URL"""
        base_url = self.env.get("base_url", BASE_URL)
        jsonData = self.get_g2m_json(base_url)
        self.env["url"] = self.get_g2m_url(jsonData)
        self.output("Found URL: %s" % self.env["url"])
        self.env["build"] = self.get_g2m_build(jsonData)
        self.output("Build number: %s" % self.env["build"])

if __name__ == "__main__":
    processor = GoToMeetingURLProvider()
    processor.execute_shell()
