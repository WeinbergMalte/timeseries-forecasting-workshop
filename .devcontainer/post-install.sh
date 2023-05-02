#!/bin/bash
set -ex

### Aliases #######################################

# listing:
echo 'alias ll="ls -lha"' >> $HOME/.bashrc
echo 'alias la="ls -A"' >> $HOME/.bashrc
echo 'alias l="ls -CF"' >> $HOME/.bashrc

# directories:
alias cdd="cd ../.."
alias cddd="cd ../../.."
alias cd..="cd .."

# typos:
alias sl="ls"
alias c="clear"
alias h="history"

# root:
alias root="sudo -i"
alias su="sudo -i"

# grep:
alias grep="grep --color=auto"
alias fgrep="fgrep --color=auto"
alias egrep="egrep --color=auto"
alias grepi="grep -ri"
alias greph="grep -ri --exclude-dir='.*'"
alias gn="grep -ri --exclude='*.ipynb'"

# git:
alias gdd="git add"
alias glg="git log --oneline --decorate --graph --all"
alias gst="git status"
alias gco="git checkout"
alias gcm="git commit"


#### Poetry #######################################
WORKSPACE_DIR=$(pwd)
pip3 install poetry
poetry config cache-dir ${WORKSPACE_DIR}/.cache
poetry config virtualenvs.in-project true
poetry install

echo "Done!"
