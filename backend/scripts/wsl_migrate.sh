#!/usr/bin/env bash

# script to quickly move stuff to wsl because performance
from=$PWD
target=~/backend_tmp

rm -rf $target || true
mkdir $target
cd $target
git clone https://github.com/szczursonn/pp5-property-olx
mv ./pp5-property-olx/backend/* .
rm -rf ./pp5-property-olx
cp -r $from/.env $from/db.sqlite3 $from/media $target
poetry install || true