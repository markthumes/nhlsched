#!/bin/bash

python main.py > temp.out
python -m json.tool temp.out > output.json
rm temp.out
