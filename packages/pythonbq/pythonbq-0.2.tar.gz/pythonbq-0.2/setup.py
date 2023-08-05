from distutils.core import setup
setup(
  name = 'pythonbq',
  packages = ['pythonbq'],
  version = '0.2',
  license='MIT',
  description = 'Python wrapper for easy use of big query',
  author = 'Connor Makowski',
  author_email = 'connor.m.makowski@gmail.com',
  url = 'https://github.com/connor-makowski/pythonbq',
  download_url = 'https://github.com/connor-makowski/pythonbq/dist/pythonbq-0.2.tar.gz',
  keywords = ['bigquery', 'big', 'query', 'pythonbq'],
  install_requires=['pandas-gbq','tqdm'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
