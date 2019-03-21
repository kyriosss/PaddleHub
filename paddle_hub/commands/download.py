# Copyright (c) 2019  PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from paddle_hub.tools.logger import logger
from paddle_hub.commands.base_command import BaseCommand, ENTRY
from paddle_hub.tools import utils
from paddle_hub.tools.downloader import default_downloader
from paddle_hub.hub_server import default_hub_server
import argparse


class DownloadCommand(BaseCommand):
    name = "download"

    def __init__(self, name):
        super(DownloadCommand, self).__init__(name)
        self.show_in_help = True
        self.description = "Download a paddle hub module."
        self.parser = self.parser = argparse.ArgumentParser(
            description=self.__class__.__doc__,
            prog='%s %s <module_name>' % (ENTRY, name),
            usage='%(prog)s [options]',
            add_help=False)
        # yapf: disable
        self.add_arg('--output_path',  str,  ".",   "path to save the module" )
        self.add_arg('--uncompress',   bool, False,  "uncompress the download package or not" )
        # yapf: enable

    def exec(self, argv):
        if not argv:
            print("ERROR: Please specify a module\n")
            self.help()
            return False
        module_name = argv[0]
        module_version = None if "==" not in module_name else module_name.split(
            "==")[1]
        module_name = module_name if "==" not in module_name else module_name.split(
            "==")[0]
        self.args = self.parser.parse_args(argv[1:])
        if not self.args.output_path:
            self.args.output_path = "."
        utils.check_path(self.args.output_path)

        url = default_hub_server.get_module_url(
            module_name, version=module_version)
        if not url:
            tips = "can't found module %s" % module_name
            if module_version:
                tips += " with version %s" % module_version
            print(tips)
            return True

        if self.args.uncompress:
            result, tips, file = default_downloader.download_file_and_uncompress(
                url=url, save_path=self.args.output_path, print_progress=True)
        else:
            result, tips, file = default_downloader.download_file(
                url=url, save_path=self.args.output_path, print_progress=True)
        print(tips)
        return True


command = DownloadCommand.instance()
