from distutils.core import setup, Extension
from distutils.cmd import Command
from distutils.command.install import install
from distutils.command.build import build
import subprocess
import os


class BuildLibsumoCommand(Command):
    """Build libsumo module."""

    description = 'Build libsumo shared library'
    user_options = [
        # The format is (long option, short option, description).
        ('no-build-libsumo', None, 'skip building libsumo'),
    ]

    def initialize_options(self):
        # """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.no_build_libsumo = False

    def finalize_options(self):
        #  """Post-process options."""
        if not self.no_build_libsumo:
            assert os.path.exists('sumo/sumo/src/libsumo'), 'sumo/sumo/src/libsumo does not exist. Did you git submodule init and git submodule update?'

    def run(self):
        """Run command."""
        if self.no_build_libsumo:
            self.announce("Skipping libsumo shared library build")
        else:
            self.announce("Building libsumo shared library")
            srcdir = './sumo/sumo'
            assert (subprocess.Popen(['aclocal'], cwd=srcdir).wait() == 0)
            assert (subprocess.Popen(['automake'], cwd=srcdir).wait() == 0)
            assert (subprocess.Popen(['autoconf'], cwd=srcdir).wait() == 0)
            assert (subprocess.Popen(['./configure', '--enable-libsumo=yes'], cwd=srcdir).wait() == 0)
            assert (subprocess.Popen(['make'], cwd=srcdir).wait() == 0)
            libsumodir = './sumo/sumo/src/libsumo'
            assert (subprocess.Popen(['make', 'install'], cwd=libsumodir).wait() == 0)
            assert (subprocess.Popen(['ldconfig']).wait() == 0)
            self.announce('Successfully built libsumo')


class PysumoBuildCommand(build):
    def run(self):
        self.run_command("build_libsumo")
        build.run(self)

cmdclass = {
	"build": PysumoBuildCommand,
	"build_libsumo": BuildLibsumoCommand
}

ext_args = {
    'include_dirs': ['src', 'sumo/sumo/src', '/usr/include/fox-1.6'],
    'libraries': ['sumo']
}

src = [
	'src/inductionloop.cpp',
	'src/meme.cpp',
	'src/simulation.cpp',
	'src/tls.cpp',
	'src/vehicle.cpp',
	'src/pysumo.cpp'
]
	
ext_modules = [
    Extension('pysumo', src, **ext_args)
]

setup(name='pysumo',
      version='0.0.1',
      description='Pysumo',
      author='Ben Striner',
      author_email='bstriner@gmail.com',
      url='https://github.com/bstriner/pysumo',
      cmdclass=cmdclass,
      ext_modules=ext_modules)