from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

with open(path.join(here, ".gitignore"), encoding="utf-8") as file:
    ignore = [
        line.split("#")[0].rstrip()
        for line in file.readlines()
        if line.split("#")[0].rstrip()
    ]

setup(
    name="boilee",
    version="0.1.0",
    description="""An easy way to create a tool to generate code boilerplates like "npm init" and "vue create" for any programming language.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vadolasi/easy-boilerplate",
    author="Vitor Daniel",
    author_email="vitor036daniel@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="boilerplate cli generator templating",
    packages=find_packages(exclude=ignore),
    python_requires=">=3.5",
    install_requires=[
        "click==7.1.2",
        "docopt==0.6.2",
        "jinja2==2.11.2",
        "markupsafe==1.1.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "prompt-toolkit==1.0.14",
        "pyfiglet==0.8.post1",
        "pygments==2.7.1; python_version >= '3.5'",
        "pyinquirer==1.0.3",
        "pyyaml==5.3.1",
        "regex==2020.10.15",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "sqlalchemy==1.3.20",
        "wcwidth==0.2.5",
    ],
    extras_require={
        "dev": [
            "appdirs==1.4.4",
            "attrs==20.2.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "black==19.10b0",
            "bleach==3.2.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "cached-property==1.5.2",
            "cerberus==1.3.2",
            "certifi==2020.6.20",
            "cffi==1.14.3",
            "chardet==3.0.4",
            "click==7.1.2",
            "colorama==0.4.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "cryptography==3.1.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "distlib==0.3.1",
            "docutils==0.16; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "idna==2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "jeepney==0.4.3; sys_platform == 'linux'",
            "keyring==21.4.0; python_version >= '3.6'",
            "orderedmultidict==1.0.1",
            "packaging==20.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pathspec==0.8.0",
            "pep517==0.9.1",
            "pip-shims==0.5.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "pipenv-setup==3.1.1",
            "pipfile==0.0.2",
            "pkginfo==1.6.0",
            "plette[validation]==0.2.3; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pycparser==2.20; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pygments==2.7.1; python_version >= '3.5'",
            "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "readme-renderer==28.0",
            "regex==2020.10.15",
            "requests==2.24.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "requests-toolbelt==0.9.1",
            "requirementslib==1.5.13; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "rfc3986==1.4.0",
            "secretstorage==3.1.2; sys_platform == 'linux'",
            "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "toml==0.10.1",
            "tomlkit==0.7.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "tqdm==4.50.2; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "twine==3.2.0",
            "typed-ast==1.4.1",
            "urllib3==1.25.11; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
            "vistir==0.5.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "webencodings==0.5.1",
            "wheel==0.35.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        ]
    },
    dependency_links=[],
    project_urls={
        "Bug Reports": "https://github.com/vadolasi/easy-boilerplate/issues",
        "Funding": "https://donate.pypi.org",
        "Say Thanks!": "https://saythanks.io/to/vitor036daniel%40gmail.com",
        "Source": "https://github.com/vadolasi/easy-boilerplate/",
    },
    entry_points="""
        [console_scripts]
        boilee=boilee.scripts.boilee:cli
    """,
)
