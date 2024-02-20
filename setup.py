import shutil
import subprocess
from setuptools import Command, setup
from setuptools.command.sdist import sdist

def build_js_bundle():
    subprocess.check_call([shutil.which("deno"), "bundle", "deno_vm/vm-server/index.js", "deno_vm/vm-server/bundle.js"])

class BuildJSBundle(Command):
    def initialize_options(self): pass
    def finalize_options(self): pass
    def run(self): build_js_bundle()

class Build(sdist):
    sub_commands = [("build_js_bundle", None), *sdist.sub_commands]

setup(cmdclass={"sdist": Build, "build_js_bundle": BuildJSBundle})
