#!/bin/bash
mkdir exports
find . -name "*.drawio" -exec rm -f {}.pdf \; -exec drawio --crop -x -o exports/{}.pdf {} \;
