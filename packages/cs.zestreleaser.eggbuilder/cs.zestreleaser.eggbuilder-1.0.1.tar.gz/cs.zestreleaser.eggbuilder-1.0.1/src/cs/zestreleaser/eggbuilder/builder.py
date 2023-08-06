# -*- coding: utf-8 -*-
from zest.releaser import utils

import os
import shutil


def build(context):
    if utils.ask("Do you want to create an *.egg file?", False):
        result = utils.execute_command(utils.setup_py("bdist_egg"))
        utils.show_interesting_lines(result)
        result = utils.execute_command(["python2", "setup.py", "bdist_egg"])
        utils.show_interesting_lines(result)

        dist_folder = os.path.join(context.get("tagworkingdir"), "dist")
        for filename in os.listdir(dist_folder):
            if filename.endswith("egg"):
                egg_files = os.path.join(dist_folder, filename)
                shutil.copy(egg_files, context.get("workingdir"))


def show_contents(context):
    for filename in os.listdir(context.get("workingdir")):
        if filename.endswith("egg"):
            print("Created file: {0}".format(filename))
