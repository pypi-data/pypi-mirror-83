# pytest-shortcuts

Expand command-line shortcuts listed in pytest configuration

This [pytest](https://github.com/pytest-dev/pytest) plugin was generated with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with @hackebrot's [cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin) template.

## Getting Started

Install using your favourite python package manager:

```no-highlight
$ pip install pytest-shortcuts
```

Add some shortcuts to your pytest configuration:

```no-highlight
[pytest]
shortcuts =
    --live: -m "live and not slow"
    --slow: -m "live and slow"
    --offline: --disable-socket -m "not live"
```

Now when you run your tests with eg `--live`, it will be as if you provided `-m "live and not slow"`.

## Contributing

If you would like to contribute, you may need to install the following development tools:

```
# Useful for installing tools like tox and pre-commit in a separate environment
pip install --user pipx

# We run the test suite with tox
pipx install tox
pipx install flake8

# Install pre-commit hooks to prevent commits that do not pass static checks
pipx install pre-commit
pre-commit install
```

Additionally, you will want to install a number of different Python versions for tox to use.
I would recommend using [pyenv](https://github.com/pyenv/pyenv) to do this.
After you have installed pyenv, run `tox` to see which Python versions you are missing and enable them.
For example:

```
brew install pyenv              # If you have homebrew
tox -l                          # Check which Python versions are currently required
pipx inject tox tox-pyenv       # Make pyenv versions available to tox
pyenv install 3.6.11            # If you need a Python 3.6
pyenv install 3.7.8             # If you need a Python 3.7
pyenv install 3.8.5             # If you need a Python 3.8
pyenv local 3.6.11 3.7.8 3.8.5  # Make these versions locally available
tox                             # Run the test suite via tox (same as "make test")
```

A simple Makefile is included to run development commands, just type `make` to see
a list of available commands.

## License

Distributed under the terms of the [BSD-3 license](http://opensource.org/licenses/BSD-3-Clause), "pytest-shortcuts" is free and open source software


  [Cookiecutter]: https://github.com/audreyr/cookiecutter
  [@hackebrot]: https://github.com/hackebrot
  [MIT]: http://opensource.org/licenses/MIT
  [BSD-3]: http://opensource.org/licenses/BSD-3-Clause
  [GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
  [Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
  [cookiecutter-pytest-plugin]: https://github.com/pytest-dev/cookiecutter-pytest-plugin
  [file an issue]: https://github.com/willhardy/pytest-shortcuts/issues
  [pytest]: https://github.com/pytest-dev/pytest
  [tox]: https://tox.readthedocs.io/en/latest/
  [pip]: https://pypi.org/project/pip/
  [PyPI]: https://pypi.org/project
