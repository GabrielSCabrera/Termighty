from distutils.core import setup
setup(
  name = 'Termighty',
  packages = ['Termighty', 'Termighty.obj', 'Termighty.utils'],
  version = '0.0.14',      # Start with a small number and increase it with every change you make
  description = 'A Python-based GUI development package for Ubuntu\'s Gnome terminal',
  author = 'Gabriel S. Cabrera',
  author_email = 'gabric@uio.no',      # Type in your E-Mail
  url = 'https://github.com/GabrielSCabrera/Termighty',
  download_url = 'https://github.com/GabrielSCabrera/Termighty/archive/v0.0.14.tar.gz',    # I explain this later on
  keywords = ['terminal', 'gui', 'interactive'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',   # Again, pick a license
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
