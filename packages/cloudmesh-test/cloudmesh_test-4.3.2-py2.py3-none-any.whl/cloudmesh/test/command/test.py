from __future__ import print_function

import platform

from cloudmesh.common.console import  Console

from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command
from cloudmesh.test.CloudmeshTest import CloudmeshTest
import shutil

class TestCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_test(self, args, arguments):
        """
        ::

          Usage:
                test

          This command is intended to check if your windows set up is
          correctly done.

          Bugs:
              This program is supposed to be implemented. It is at this
              time just a template

          Description:

          Checks we do

             1. are you running python 3.8.1
             2. are you having the newest version of pip
             3. is cl installed
             4. is nmake installed
             5. is the username without spaces
             6. are you running in a vnenv
             7. is the default mongo port used
             8. do you have docker installed
             9. do you have vbox installed
            10. how much memory do you have
            11. do you have free diskspace

          Checks that are missing or need implemented

            12. is hyperv switched on or off
            13. are containers running
            14. .... other tyings that can help us debug your environment

        """

        tester = CloudmeshTest()

        #
        # Python setup
        #
        tester.check_venv()
        tester.check_python()
        tester.check_command("pip --version", test="20.0.2")

        #
        # command tool setup
        #

        if platform.system() == "Windows":

            if not tester.check_windows():
                Console.error(" THIS VERSION OF WINDOWS IS NOT SUPPORTED.")
                return ""


            tester.which("cl")
            tester.which("nmake")
            tester.which("git")
            tester.which("ssh")
            tester.which("ssh-keygen")
            tester.which("docker")
            tester.which("yamllint")


        else:

            tester.check_command("git --version", test="git version")
            tester.check_command("ssh", test="usage", show=False)
            tester.check_command("ssh-keygen --help", test="usage", show=False)
            tester.check_command("docker --version", test="Docker version")
            tester.check_command("VirtualBox --help",
                                 test="Oracle VM VirtualBox VM Selector",
                                 show=False)
            tester.check_command("yamllint", test="usage: yamllint", show=False)

        tester.is_user_name_valid()
        tester.check_mongo()

        tester.usage()
        tester.check_yaml()
        return ""
