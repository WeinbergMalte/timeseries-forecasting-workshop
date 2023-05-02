#!/bin/bash
set -ex

### Aliases #######################################

# listing:
echo 'alias ll="ls -lha"' >> $HOME/.bashrc
echo 'alias la="ls -A"' >> $HOME/.bashrc
echo 'alias l="ls -CF"' >> $HOME/.bashrc

# directories:
echo 'alias cdd="cd ../.."' >> $HOME/.bashrc
echo 'alias cddd="cd ../../.."' >> $HOME/.bashrc
echo 'alias cd..="cd .."' >> $HOME/.bashrc

# typos:
echo 'alias sl="ls"' >> $HOME/.bashrc
echo 'alias c="clear"' >> $HOME/.bashrc
echo 'alias h="history"' >> $HOME/.bashrc

# root:
echo 'alias root="sudo -i"' >> $HOME/.bashrc
echo 'alias su="sudo -i"' >> $HOME/.bashrc

# git:
echo 'alias glg="git log --oneline --decorate --graph --all"' >> $HOME/.bashrc
echo 'alias gst="git status"' >> $HOME/.bashrc
echo 'alias gco="git checkout"' >> $HOME/.bashrc
echo 'alias gcm="git commit"' >> $HOME/.bashrc


#### Poetry #######################################
WORKSPACE_DIR=$(pwd)
poetry config cache-dir ${WORKSPACE_DIR}/.cache
poetry config virtualenvs.in-project true
poetry install

echo "Done!"
