from pathlib import Path
from string import ascii_lowercase

from rsrc import plugins
from setuptools import (find_packages,
                        setup)

import rsrc_local
from rsrc_local import base

plugins_entry_points = [
    plugins.to_entry_point(id_=plugins.to_id(''),
                           module_name=base.__name__,
                           function_name=base.deserialize_path.__qualname__),
    plugins.to_entry_point(id_=plugins.to_id('file'),
                           module_name=base.__name__,
                           function_name=base.deserialize_url.__qualname__),
]
# workaround for supporting absolute Windows paths with drive letters
# which may be considered as a scheme during URL parsing
for drive_letter in ascii_lowercase:
    plugins_entry_points.append(plugins.to_entry_point(
            id_=plugins.to_id(drive_letter),
            module_name=base.__name__,
            function_name=base.deserialize_path.__qualname__))

project_base_url = 'https://github.com/lycantropos/rsrc_local/'

setup(name=rsrc_local.__name__,
      packages=find_packages(exclude=('tests', 'tests.*')),
      version=rsrc_local.__version__,
      description=rsrc_local.__doc__,
      long_description=Path('README.md').read_text(encoding='utf-8'),
      long_description_content_type='text/markdown',
      author='Azat Ibrakov',
      author_email='azatibrakov@gmail.com',
      url=project_base_url,
      download_url=project_base_url + 'archive/master.zip',
      python_requires='>=3.5.3',
      entry_points={plugins.__name__: plugins_entry_points},
      install_requires=Path('requirements.txt').read_text(encoding='utf-8'))
