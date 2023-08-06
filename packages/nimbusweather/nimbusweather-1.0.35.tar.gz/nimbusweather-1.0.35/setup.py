#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'nimbusweather',
        version = '1.0.35',
        description = 'weather software',
        long_description = 'nimbus weather talks to a variety of weather stations and publishes the data to (currently) weather underground. Nimbus is a fork of the very popular weewx weather software.',
        long_description_content_type = None,
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        keywords = '',

        author = 'Garret Hayes',
        author_email = 'glhayes81@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'GPLv3',

        url = '',
        project_urls = {},

        scripts = [
            'scripts/nimbus',
            'scripts/nimbus_config'
        ],
        packages = [
            'nimbuscfg',
            'nimbusdrivers',
            'nimbusmain'
        ],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {
            'nimbuscfg': ['nimbus.conf', 'init.d/*']
        },
        install_requires = [
            'configobj',
            'pyserial',
            'pyusb',
            'requests',
            'sentry_sdk',
            'setuptools',
            'urllib3==1.22'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
