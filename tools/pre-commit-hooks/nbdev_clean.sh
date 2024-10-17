#!/bin/sh

set -eu

# Check if at least one file is provided
if [ $# -eq 0 ]; then
	echo "Usage: $0 <file1> [<file2> ...]" >&2
	exit 1
fi

for file in "$@"; do
	uvx --with setuptools --from nbdev nbdev_clean --fname "$file"
done
