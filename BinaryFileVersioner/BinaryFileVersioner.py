#!/usr/bin/env python
#
# Copyright 2018 Elliot Jordan
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

import shlex
import os
from autopkglib import Processor, ProcessorError
from subprocess import PIPE, Popen


__all__ = ['BinaryFileVersioner']


class BinaryFileVersioner(Processor):

    '''This processor returns the version number of a binary file that has an embedded info plist,
    using the /usr/bin/otool command.
    '''

    input_variables = {
        'input_file_path': {
            'required': True,
            'description': 'File path to a binary file (not app bundle).'
        },
        'plist_version_key': {
            'required': False,
            'description': 'Which plist key to use. Defaults to CFBundleShortVersionString.'
        }
    }
    output_variables = {
        'version': {
            'description': 'Version of the file.'
        }
    }
    description = __doc__


    def main(self):
        '''Main function.'''

        if not os.path.isfile('/usr/bin/otool'):
            raise ProcessorError('/usr/bin/otool is not present on this Mac.')

        cmd = '/usr/bin/otool -P \'{}\''.format(self.env['input_file_path'])
        proc = Popen(shlex.split(cmd.strip()), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        exitcode = proc.returncode

        if exitcode != 0:
            raise ProcessorError('/usr/bin/otool failed with error: {}'.format(err))

        plist_lines = out.split('\n')
        for index, line in enumerate(plist_lines):
            if self.env.get('plist_version_key', 'CFBundleShortVersionString') in line:
                version = plist_lines[index + 1]
                version = version.strip().strip('<string>').strip('</string>')
                self.env['version'] = version
                self.output('Found version: {}'.format(self.env['version']))
                break

        if not self.env['version']:
            raise ProcessorError('Unable to find a {} key in {}.'.format(
                self.env.get('plist_version_key', 'CFBundleShortVersionString'),
                self.env['input_file_path']))


if __name__ == '__main__':
    processor = BinaryFileVersioner()
    processor.execute_shell()
