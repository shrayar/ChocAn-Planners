#!/usr/bin/env bash

# this should work on ada.cs.pdx.edu to install hatch.
# only needs to be run once per developer.

set -o errexit   # abort on nonzero exitstatus
set -o nounset   # abort on unbound variable
set -o pipefail  # don't hide errors within pipes

python3 -m pip install --user --upgrade pipx
python3 -m pipx ensurepath

virtualenv --clear ~/.local/pipx/shared 

pipx install hatch
