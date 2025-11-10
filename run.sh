#!/usr/bin/env bash
set -e
python3 parser.py test_cases/test1.rat output/output_test1.txt
echo "Wrote output to output/output_test1.txt"
