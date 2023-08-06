import sys
import platform
import os
import subprocess


basepath_for_binaries = os.path.join(sys.prefix, "epew_binaries")


def execute(os_specific_path: str, file: str, encoding: str, argument: str):
    epew_executable_file = os.path.join(basepath_for_binaries, os_specific_path, file)
    process = subprocess.Popen(f'"{epew_executable_file}" {argument}')
    process.communicate()
    return process.returncode


def epew_cli():
    epew_cli_with_custom_argument(' '.join(sys.argv[1:]))


def epew_cli_with_custom_argument(argument: str):
    try:
        os = platform.system()
        if(os == "Windows"):
            exit_code = execute("win-x64", "epew.exe", "cp850", argument)
        elif(os == "Linux"):
            exit_code = execute("linux-64", "epew", "UTF-8", argument)
        elif(os == "Darwin"):
            print(f"OS '{os}' is not supported yet")
            exit_code = 2147393881
        else:
            print(f"Unexpected OS: '{os}'")
            exit_code = 2147393882
    except Exception as exception:
        sys.stdout.write(str(exception))
        sys.stderr.flush()
        exit_code = 2147393883
    sys.exit(exit_code)


if __name__ == '__main__':
    epew_cli()
