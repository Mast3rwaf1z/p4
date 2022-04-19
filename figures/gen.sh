#!/bin/bash
mkdir exports
find . -name "*.drawio" -exec rm -f {}.pdf \; -exec sh -c 'drawio --crop -x -o "exports/${0%.drawio}.pdf" {}' {} \;
