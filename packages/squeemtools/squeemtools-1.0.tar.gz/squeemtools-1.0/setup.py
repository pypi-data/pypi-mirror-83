from setuptools import setup, find_packages
setup(
  name = 'squeemtools',         # How you named your package folder (MyLib)
  packages = find_packages(),   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Packages for running some lightning graphing code',   # Give a short description about your library
  author = 'Ben van Oostendorp',                   # Type in your name
  author_email = 'ben.vano@digipen.edu',      # Type in your E-Mail
  url = 'https://github.com/Squeemos/SqueemTools',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Squeemos/SqueemTools/archive/SqueemTools_1.0.tar.gz',    # I explain this later on
  keywords = ['GRAPHING', 'FUZZY C MEANS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'mpl_toolkits.basemap',
          'matplotlib',
          'numpy',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.8',      #Specify which pyhton versions that you want to support
  ],
)