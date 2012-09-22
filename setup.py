from setuptools import setup, find_packages


setup(name='ezsocksproxy',
      version="0.1",
      author="Mike Spindel",
      author_email="mike@spindel.is",
      license="MIT",
      keywords="ezproxy socks proxy",
      url="http://github.com/deactivated/ezsocksproxy",
      description='Tunnel EZProxy requests via a SOCKS proxy.',
      install_requires=['PySocks', 'gevent'],
      scripts=["bin/ezsocksproxy"],
      packages=find_packages(),
      zip_safe=False,
      classifiers=[
          "Development Status :: 4 - Beta",
          "License :: OSI Approved :: MIT License",
          "Intended Audience :: Developers",
          "Natural Language :: English",
          "Programming Language :: Python"])
