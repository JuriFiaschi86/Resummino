#!/usr/bin/env bash
#VER="latest"
VER="3.1.0"

# Preinstalled pdfs are listed here https://github.com/APN-Pucky/Dockerfiles/tree/master/debian/lhapdf
# Create a pull request/issue for different pdfs 
# or make your own Dockerfile with FROM apnpucky/resummino which has your pdfs installed
# Resummino alias tools
alias resummino='docker run -i  --rm  -u `id -u $USER`:`id -g`  -v $PWD:$PWD -w $PWD  apnpucky/resummino:'$VER' resummino'