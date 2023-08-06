from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'TextTools4',
  packages = ['TextTools4'],
  version = '0.1.2',
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A package to provide data and use tools on a text.',   # Give a short description about your library
  author = 'Siddharth Rout',                   # Type in your name
  author_email = 'routsiddharth2911@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/routsiddharth/TextTools4',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/routsiddharth/TextTools4/archive/v0.1.2.tar.gz',
  keywords = ['DATA', 'ANALYSIS', 'TEXT', 'WORDS', 'CHART', 'GRAPH', 'TOOLS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'docx',
          'matplotlib',
          'PyPDF4',
          'random',
          're'
      ],
  long_description=long_description,
  long_description_content_type="text/markdown",
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Other Audience',      # Define that your audience are developers
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
