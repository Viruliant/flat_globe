#!/usr/bin/env bash
owd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" #Path to THIS script.

updatelockmain(){
  cleanup_proj_py
  compile_requirements
  gen_toml requirements.txt pyproject.toml
  uv lock --upgrade
}

cleanup_proj_py(){
  cd "$owd"
  rm ./requirements.txt
  rm ./pyproject.toml
  rm ./uv.lock
}

compile_requirements(){
  uv pip compile \
    requirements.bak.txt \
    -o requirements.txt \
    --upgrade \
    --prerelease=allow
}

gen_toml() {
    local in_file="$1"
    local out_file="$2"
    if [[ -z "$in_file" || -z "$out_file" ]]; then
        echo "Usage: gen_toml <input_requirements_file> <output_pyproject.toml>"
        return 1
    fi
    if [[ ! -f "$in_file" ]]; then
        echo "$in_file not found in $(pwd)"
        return 1
    fi
    set -euo pipefail
    # Format dependencies for TOML array
    deps=$(
        awk '
            /^[[:space:]]*#/ { next }
            /^[[:space:]]*$/ { next }
            { print "\"" $0 "\"," }
        ' "$in_file"
    )
    # deps=$(sed 's/^/"/; s/$/",/' "$in_file")
    cat > "$out_file" <<EOF
[project]
name = "ex-reqs-shell"
version = "0.1.0"
description = "Add your description here"
requires-python = ">=3.12"
dependencies = [
$deps
]
[tool.uv.sources]
torch = { index = "pytorch-cpu" }
[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true
EOF
    echo ">>> generated $out_file"
    # If output is pyproject.toml, generate lock file
    if [[ "$(basename "$out_file")" == "pyproject.toml" ]]; then
        echo ">>> generating uv.lock with CPU-only Torch"
        uv lock --upgrade
    fi
}

updatelockmain
