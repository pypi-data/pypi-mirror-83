import getpass
import os
import platform
import socket
import sys
from subprocess import CalledProcessError

import psutil
from pathlib import Path
from cloudmesh.common.Shell import Shell
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from cloudmesh.configuration.Config import Config
from cloudmesh.configuration.__version__ import version as latest
import shutil

"""
are you running in a vnenv
are you running python 3.8.1
are you running the 64 bit version of python
are you having the newest version of pip
is the default mongo port used
is cl installed
how much memory do you have
do you have free diskspace
do you have docker installed
do you have vbox installed

TODO
is hyperv switched on or off
are containers running
.... other tyings that can help us debug your environment 

https://stackoverflow.com/questions/30496116/how-to-disable-hyper-v-in-command-line

In an elevated Command Prompt write this :

To disable:

bcdedit /set hypervisorlaunchtype off

To enable:

bcdedit /set hypervisorlaunchtype auto 


"""

class CloudmeshTest:

    def __init__(self):
        pass

    def check_windows(self):
        osv, n, version = platform.platform().split(".")

        if "18362" in version:
            kind = "1903"
        elif "18363" in version:
            kind = "1909"
        else:
            kind = "unsupported"

        if kind == "unsuported":
            Console.error(f"Windows {osv} {version}: {kind}")
            return False
        else:
            Console.ok(f"OK. Windows {osv} {version}: {kind}")
        return True


    def check_yaml(self):
        config = Config()
        errors = False
        if "chameleon" in config["cloudmesh.cloud"]:
            credentials = config["cloudmesh.cloud.chameleon.credentials"]
            if "OS_PASSWORD" in credentials:
                Console.error("You are using an old version of the cloudmesh.yaml file")
            else:
                Console.ok("your yaml file seems ok")
        location = config.location
        print(f"Location of cloudmesh.yaml: {location}")
        print("we run a simple yamllint test. Not all issues reported need to be corrected.")

        current = config["cloudmesh.version"]
        if latest == current:
            Console.ok(f"OK. you have cloudmesh.yaml version {current}")
        else:
            Console.warning(f"Your cloudmesh.yaml file version is not up to date.")
            Console.warning(f"Production version: {latest}")
            Console.warning(f"Your version:       {current}")
            Console.warning(f"Please carefully check your cloudmesh.yaml")

        yamlfile = Path(f"{location}/cloudmesh.yaml")
        if sys.platform in ["win32"]:
            r = os.system((f"yamllint {yamlfile}"))
        else:
            result = Shell.run(f"yamllint {yamlfile}")
            for line in result.splitlines():
                line = line.strip()
                if "missing document start" in line:
                    continue
                if "line too long" in line:
                    continue
                if "error" in line:
                    errors = True
                    Console.error (line)
                else:
                    print(line)
            if errors:
                Console.error("We found issues in your yaml file")
            else:
                Console.ok(f"OK. Your yaml file {yamlfile} seems valid")

    def usage(self):
        hdd = psutil.disk_usage('/')
        Console.info("Disk Space")
        print("      Total: {total:.0f} GiB".format(total=hdd.total / (2 ** 30)))
        print("      Used: {used:.0f} GiB".format(used=hdd.used / (2 ** 30)))
        print("      Free: {free:.0f} GiB".format(free=hdd.free / (2 ** 30)))

        mem = psutil.virtual_memory()
        total = mem.total >> 30
        available = mem.available >> 30
        print(f"      Memory: {available}GB free from {total}GB")

    def is_port_used(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    def is_venv(self):
        return (hasattr(sys, 'real_prefix') or
                (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

    # noinspection PyPep8
    def check_mongo(self):
        if platform.system() == "Windows":
            result = os.system("sc.exe query MongoDB")
            if result == 1060:
                Console.ok("The MongoDB service is not running")
            else:
                Console.error("The MOngo DB service is running")
                Console.error(result)

            self.which("mongod")
            self.which("mongo")

        if self.is_port_used(27017):
            Console.error("The mongo port 27017 is already used")
        else:
            Console.ok("OK. The mongo port 27017 is free")

    def check_python(self):
        self.check_python_command()
        length = platform.architecture()[0]
        if length == "32bit":
            Console.error("You run Python 32 bit")
        elif length == "64bit":
            Console.ok("OK. You run Python 64 bit")
        else:
            Console.error(f"Pythin is not 32 or 64 bit: {length}")


    def check_path(self, command):
        path = os.environ["PATH"]
        print(path)

    def which(self, command):
        result = shutil.which(command)
        if result is not None:
            Console.ok(f"OK. {command} found: {result}")
        else:
            Console.error(f"Command {command} not found")


    def check_python_command(self,
                     command="python --version",
                     tests=["3.8.1", "3.8.2"],
                     show=True):

        # banner(f"testing command: {command}")
        try:
            if sys.platform in ["win32"]:
                result = Shell.run2(command).strip()
            else:
                result = Shell.run(command).strip()

            for test in tests:
                print (test)
                if test in result:
                    if show:
                        Console.ok(f"OK. {test} found in {result}")
                    else:
                        Console.ok(f"OK. {command} found")
                    return

            if show:
                Console.error(f"python not found in {result}")
            else:
                Console.error(f"{command} not found")
        except:
            Console.error(f"command '{command}' not successfull")

    def check_command(self, command, test=None, show=True):

        # banner(f"testing command: {command}")

        try:
            if sys.platform in ["win32"]:
                result = Shell.run2(command).strip()
            else:
                result = Shell.run(command).strip()

            if test not in result:
                if show:
                    Console.error(f"{test} not found in {result}")
                else:
                    Console.error(f"{command} not found")
            else:
                if show:
                    Console.ok(f"OK. {test} found in {result}")
                else:
                    Console.ok(f"OK. {command} found")

        except:
            Console.error(f"command '{command}' not successful")

    #
    # TODO:  this should also work if you do return not name is ENV3
    #        use where python to find where ot is
    #        the username shoudl be in the path of the first python that shows
    #
    def check_venv(self):

        # banner(f"checking python venv")

        if self.is_venv():
            Console.ok("OK. you are running in a venv")
            print("    VIRTUAL_ENV=", os.environ.get("VIRTUAL_ENV"), sep="")

        else:
            Console.error("You are not running in a venv")
        if "ENV3" not in os.environ.get("VIRTUAL_ENV"):
            Console.warning("your venv is not called ENV3. That may be ok")

        if platform.system() == "Windows":
            venv = os.environ.get("VIRTUAL_ENV")
            where = path_expand(venv)
            activate_path = f"{where}\\Scripts\\activate.bat"
            # check if the dir exists at where
            if os.path.isdir(where):
                Console.ok("OK. ENV3 directory exists")
            else:
                Console.error("ENV3 directory does not exists")

            # check if activate exists in ~\ENV3\Scripts\activate.bat
            if os.path.isfile(activate_path):
                Console.ok(f"OK. Activate exists in {activate_path}")
            else:
                Console.error(f"Could not find {activate_path}")


    def is_user_name_valid(self):
        # banner("Check For User Name")
        username = getpass.getuser()

        if " " in username:
            Console.error("User name has spaces")
        else:
            Console.ok("OK. No spaces in user name")


if __name__ == "__main__":
    _test = CloudmeshTest()
    # _test.check_command("python --version", test="3.8.1")
    # _test.check_command("cl")
    # _test.check_venv()
    # _test.is_venv_exists()
    _test.is_user_name_valid()
