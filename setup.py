from distutils.core import setup
setup(
  name = 'Termighty',
  packages = ['Termighty', 'Termighty.obj', 'Termighty.utils'],
  version = '0.0.1',
  description = 'A Python-based GUI development package for the Gnome terminal',
  author = 'Gabriel S. Cabrera',
  author_email = 'gabric@uio.no',
  url = 'https://github.com/GabrielSCabrera/Termighty',
  download_url = 'https://github.com/GabrielSCabrera/Termighty/archive/v0.0.1.tar.gz',
  keywords = ['terminal', 'gui', 'interactive'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',   
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
)
