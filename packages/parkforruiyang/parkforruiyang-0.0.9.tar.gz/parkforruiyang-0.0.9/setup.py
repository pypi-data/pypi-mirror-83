from setuptools import setup, find_packages

setup(name='parkforruiyang',
      packages = find_packages(),
      version='0.0.9',
      install_requires=['numpy', 'wget', 'networkx', 'gym', 'dill', 'pandas'],
      author = 'Ruiyang',                   # Type in your name
      author_email = 'ruiyang@ccs.neu.edu',      # Type in your E-Mail
      url = 'https://github.com/xuruiyang/parkforruiyang',   # Provide either the link to your github or to your website
      download_url = 'https://github.com/xuruiyang/parkforruiyang/archive/0.0.9.tar.gz',    # I explain this later on
)
