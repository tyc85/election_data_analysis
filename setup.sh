#/usr/bin/env bash

# setup local python virtualenv and packages

mkdir -p ./pdfs/openelections
mkdir -p ./pdfs/electioncom
set -ex
python3 -m venv ~/venvs/election_analysis
source ~/venvs/election_analysis/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
