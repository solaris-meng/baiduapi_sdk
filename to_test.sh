#!/bin/bash
for file in ./*_test.py
do
    python $file
done
