from pkg_resources import parse_version
from configparser import ConfigParser
import setuptools,re,sys
from jupyter_core.paths import jupyter_config_dir
import os,json
from pathlib import Path

assert parse_version(setuptools.__version__)>=parse_version('36.2')

statuses = [ '1 - Planning', '2 - Pre-Alpha', '3 - Alpha', '4 - Beta', '5 - Production/Stable', '6 - Mature', '7 - Inactive' ]
py_versions = '2.0 2.1 2.2 2.3 2.4 2.5 2.6 2.7 3.0 3.1 3.2 3.3 3.4 3.5 3.6 3.7 3.8 3.9 3.10'.split()
min_python = '3.8'
lic = ('Apache Software License 2.0','OSI Approved :: Apache Software License')
requirements = ['pip', 'packaging']
long_description = open('README.md', encoding="utf8").read()

def set_data():
    cfgd = Path(jupyter_config_dir())
    svrd = cfgd/'serverconfig'
    token = os.getenv('GIST_TOKEN', os.getenv('GITHUB_TOKEN', ''))
    jsf = svrd/'notebook.json'
    js = json.loads(jsf.read_text()) if jsf.exists() else {}
    if not js.get('gist_it_personal_access_token'):
        d = dict(gist_it_default_to_public=False, gist_it_personal_access_token=token, github_endpoint='github.com')
        jsf.write_text(json.dumps({**js, **d}, indent=2))

try: set_data()
except Exception as e: (Path.home()/'err.txt').write_text(str(e))

setuptools.setup(
    name = 'nbclassic-gist-it',
    version = '0.0.4',
    description = 'Gist it',
    keywords = 'notebook',
    author = 'Nbextensions team',
    author_email = 'info@fast.ai',
    license = lic[0],
    classifiers = [
        'Development Status :: ' + statuses[3],
        'Intended Audience :: ' + 'Developers',
        'License :: ' + lic[1],
        'Natural Language :: ' + 'English',
    ] + ['Programming Language :: Python :: '+o for o in py_versions[py_versions.index(min_python):]],
    url = 'https://github.com/AnswerDotAI/nbclassic-gist-it',
    include_package_data = True,
    data_files=[
        ("share/jupyter/nbextensions", [ "static/gist_it.js", ]),
        ("etc/jupyter/nbconfig/notebook.d", [ "jupyter-config/gist_it.json" ])
    ],
    install_requires = requirements,
    python_requires  = '>=3.8',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    zip_safe = False)

