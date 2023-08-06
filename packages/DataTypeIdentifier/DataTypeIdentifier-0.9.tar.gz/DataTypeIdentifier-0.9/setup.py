# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from distutils.core import setup
setup(
  name = 'DataTypeIdentifier',         # How you named your package folder (MyLib)
  packages = ['DataTypeIdentifier'],   # Chose the same as "name"
  version = '0.9',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Automatic detection of distribution data type',   # Give a short description about your library
  author = 'AVOKANDOTO',                   # Type in your name
  author_email = 'yannavok2@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/YA26/Data_type_identifier',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/YA26/Data_type_identifier/archive/0.9.tar.gz',    # I explain this later on
  keywords = ['distribution', 'data type identifier', 'data type detector'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'scikit-learn',
          'tensorflow',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
  include_package_data=True,
  package_data={
      'DataTypeIdentifier': ['model_and_checkpoint/*', 'saved_variables/mappings.pickle'],
   },
)
