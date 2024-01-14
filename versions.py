import pkg_resources
import os
import shutil
import flask
import pydub
import openai
import tqdm

def print_version(package_name):
    try:
        version = pkg_resources.get_distribution(package_name).version
        print(f"{package_name}=={version}")
    except pkg_resources.DistributionNotFound:
        print(f"{package_name} is not installed")

print_version("flask")
print_version("shutil")  # This is a standard library, it won't have a version
print_version("pathlib")  # This is a standard library, it won't have a version
print_version("pydub")
print_version("openai")
print_version("tqdm")
print_version("os")  # This is a standard library, it won't have a version
print_version("datetime")  # This is a standard library, it won't have a version