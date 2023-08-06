# Boilee

[![License](https://img.shields.io/github/license/vadolasi/boilee?style=for-the-badge)](https://choosealicense.com/licenses/gpl-3.0/)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/vadolasi/boilee?style=for-the-badge)](https://github.com/vadolasi/boilee/releases)
[![Python version](https://img.shields.io/github/pipenv/locked/python-version/vadolasi/boilee?style=for-the-badge)](https://docs.python.org/3.8/)
[![Last commit](https://img.shields.io/github/last-commit/vadolasi/boilee?style=for-the-badge)](https://github.com/vadolasi/boilee/commits/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![Say Thanks!](https://img.shields.io/badge/say%20thanks-!-blue?style=for-the-badge)](https://saythanks.io/to/vitor036daniel%40gmail.com)

An easy way to create a tool to generate code boilerplates like `npm init` and `vue create` for any programming language.

Main features:

- Read arguments and inputs of the user;
- Manipulate the files using templates;
- Manipulate the file tree using templates;

## Installation

### Obtain the executable

You can get here the executables for [Windows](https://google.com.br) and [Linux](https://google.com.br)

### Installing via pip

You can install boilee via pip on your system (or on a venv) with the following command:

```bash
pip install boilee
```

### Installing from source code

To get the executable from the source see the [build](#build) section

## Usage

```bash
# Create a zip file that contains all the information of the boilerplate:
boilee make <input-directory> <output-file>
# Generate boilerplate
boilee run <input-file> [...boilerplate-options]
```

## Example

Create the following files:

```python
# example_boilerplate/project/scripts/python3.py

def main():
    print("Message from Python 3:")
    print("{{ message }}")

if __name__ == "__main__":
    main()
```

```python
# example_boilerplate/project/scripts/python2.py

def main():
    print "Message from Python 2:"
    print "{{ message }}"

if __name__ == "__main__":
    main()
```

```yaml
# example_boilerplate/.boilee/structure.yml

{{ project_name }} @content=project: # Creates a directory with a name provided by the user with the content of the "project" directory
    scripts: # "scripts" directory
        python{{ python-version }}.py
```

```yaml
# example_boilerplate/.boilee/parameters.yml

project_name:
    input-type: input
    parameter_type: argument
    message: Enter the project name
python-version:
    input-type: list
    message: Select a Python version
    choices:
        - choice:
            message: "Python 3"
            value: 3
        - choice:
            message: "Python 2"
            value: 2
message:
    input-type: input
    message: Enter a message
```

Create a zip file that contains all the information of the boilerplate:

```bash
boilee make example_boilerplate example.zip
```

Generate boilerplate and test:

```bash
boilee run example.zip example_python3 --python-version=3 --message=Hi!
python3 example_python3/scripts/python3.py

# Result
Message from Python 3:
Hi!
```

```bash
boilee run example.boilerplate example_python2 --python-version=2 --message=Hi!
python2 example_python2/scripts/python2.py

# Result
Message from Python 2:
Hi!
```

If a parameter is not provided it will be requested later.

![boilee run example](https://i.ibb.co/289HVb1/boilee.png)

## Contributing

See [Contributor Guidelines](CONTRIBUTING.md)

## Build

By default boilee uses [pyoxidizer](https://pyoxidizer.readthedocs.io/en/stable/) to generate an executable.

To generate an executable with pyoxidizer (if pyoxidizer is already installed) run the command:

```bash
pyoxidizer run
```

## License

[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)
