#!/bin/env bash
# ANTAB TARBALL
ANTABTAR=../../../antab/ER1v2.tar.gz

rsync -av $ANTABTAR .
tar xzvf ER1v2.tar.gz
python convert_antab.py

