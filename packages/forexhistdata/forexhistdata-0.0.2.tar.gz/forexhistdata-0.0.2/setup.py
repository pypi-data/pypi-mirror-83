from distutils.core import setup

setup(
  name = 'forexhistdata',
  packages = ['.'],
  version = '0.0.2',
  license='MIT',
  description = 'This repo is to download historic data from free source.',
  author = 'John Doe',
  author_email = 'kakashisensei@mailinator.com',
  url = 'https://gitlab.com/franky_armengol/histdata',
  download_url = 'https://gitlab.com/franky_armengol/histdata/-/archive/0.0.2/histdata-0.0.2.tar.gz',
  keywords = ['Forex', 'History data'],
  install_requires=[
          'requests',
          'beautifulsoup4'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
  ],
)
