#!/bin/bash

# Install pyenv
brew install pyenv
brew install pyenv-virtualenv
brew install pyenv-virtualenvwrapper

# Install python
pyenv install -s 2.7.13
pyenv install -s 3.4.6
pyenv install -s 3.5.3
pyenv install -s 3.6.2
pyenv rehash
pyenv global 2.7.13 3.4.6 3.5.3 3.6.2