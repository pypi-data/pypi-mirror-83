# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
from pkg_resources import get_distribution, DistributionNotFound
import sys


def get_dist(pkgname):
    try:
        return get_distribution(pkgname)
    except DistributionNotFound:
        return None


setup_kwargs = dict(
    name='wbia-lightnet',
    author='EAVISE, WildMe Developers',
    author_email='dev@wildme.org',
    description='Building blocks for recreating darknet networks in pytorch',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # The following settings retreive the version from git.
    # See https://github.com/pypa/setuptools_scm/ for more information
    setup_requires=['setuptools_scm'],
    use_scm_version={
        'write_to': 'lightnet/_version.py',
        'write_to_template': '__version__ = "{version}"',
        'tag_regex': '^(?P<prefix>v)?(?P<version>[^\\+]+)(?P<suffix>.*)?$',
        'local_scheme': 'dirty-tag',
    },
    packages=find_packages(exclude=('test',))
    + find_packages(where='wbia-tpl-brambox', exclude=('tests', 'tests.*')),
    package_dir={'lightnet': 'lightnet', 'brambox': 'wbia-tpl-brambox/brambox'},
    test_suite='test',
)


def parse_requirements(fname='requirements.txt', with_version=False):
    """
    Parse the package dependencies listed in a requirements file but strips
    specific versioning information.

    Args:
        fname (str): path to requirements file
        with_version (bool, default=False): if true include version specs

    Returns:
        List[str]: list of requirements items

    CommandLine:
        python -c "import setup; print(setup.parse_requirements())"
        python -c "import setup; print(chr(10).join(setup.parse_requirements(with_version=True)))"
    """
    from os.path import exists
    import re

    require_fpath = fname

    def parse_line(line):
        """
        Parse information from a line in a requirements text file
        """
        if line.startswith('-r '):
            # Allow specifying requirements in other files
            target = line.split(' ')[1]
            for info in parse_require_file(target):
                yield info
        else:
            info = {'line': line}
            if line.startswith('-e '):
                info['package'] = line.split('#egg=')[1]
            else:
                # Remove versioning from the package
                pat = '(' + '|'.join(['>=', '==', '>']) + ')'
                parts = re.split(pat, line, maxsplit=1)
                parts = [p.strip() for p in parts]

                info['package'] = parts[0]
                if len(parts) > 1:
                    op, rest = parts[1:]
                    if ';' in rest:
                        # Handle platform specific dependencies
                        # http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-platform-specific-dependencies
                        version, platform_deps = map(str.strip, rest.split(';'))
                        info['platform_deps'] = platform_deps
                    else:
                        version = rest  # NOQA
                    info['version'] = (op, version)
            yield info

    def parse_require_file(fpath):
        with open(fpath, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    for info in parse_line(line):
                        yield info

    def gen_packages_items():
        if exists(require_fpath):
            for info in parse_require_file(require_fpath):
                parts = [info['package']]
                if with_version and 'version' in info:
                    parts.extend(info['version'])
                if not sys.version.startswith('3.4'):
                    # apparently package_deps are broken in 3.4
                    platform_deps = info.get('platform_deps')
                    if platform_deps is not None:
                        parts.append(';' + platform_deps)
                item = ''.join(parts)
                yield item

    packages = list(gen_packages_items())
    return packages


if __name__ == '__main__':
    install_requires = parse_requirements('requirements/runtime.txt')
    extras_require = {
        'all': parse_requirements('requirements.txt'),
        'runtime': parse_requirements('requirements/runtime.txt'),
        'build': parse_requirements('requirements/build.txt'),
        'visual': parse_requirements('requirements/visual.txt'),
    }
    setup(**setup_kwargs)
