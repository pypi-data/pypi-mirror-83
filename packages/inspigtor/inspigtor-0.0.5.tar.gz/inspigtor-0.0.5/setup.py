import glob
import os

from setuptools import find_packages, setup

package_info = {}
exec(open("src/inspigtor/__pkginfo__.py").read(), {}, package_info)

scripts = glob.glob(os.path.join('scripts', '*'))

with open('requirements.txt', 'r') as fin:
    install_requires = fin.readlines()

setup(name="inspigtor",
      version=package_info["__version__"],
      description=package_info["__description__"],
      long_description=package_info["__long_description__"],
      author=package_info["__author__"],
      author_email=package_info["__author_email__"],
      maintainer=package_info["__maintainer__"],
      maintainer_email=package_info["__maintainer_email__"],
      license=package_info["__license__"],
      install_requires=install_requires,
      packages=find_packages('src'),
      include_package_data=True,
      package_dir={'': 'src'},
      platforms=['Unix', 'Windows'],
      entry_points={'gui_scripts': ['inspigtor = inspigtor.scripts.run_inspigtor:main']})
