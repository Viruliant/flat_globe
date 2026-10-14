# numtest

Testbed for building a Python app from `requirements.bak.txt` with Nix +
uv2nix. `nix build` produces `ex-reqs-shell`, a binary that runs `numtest.py`.

## Commands

```bash
# checkout with
git clone 

# requirements.bak.txt is the only editable source
# regenerates requirements.txt, pyproject.toml, uv.lock from requirements.bak.txt
./update-lock.sh
# sets flake.lock to match system nixpkgs
./Lock2LocalPkgs.sh

# build with
nix build
# needs network on first run (fetches pinned git deps + PyPI wheels)

# enter development environment with
nix develop
./result/bin/ex-reqs-shell/python3 ./numtest.py

# run with # build and run numtest.py (via `meta.mainProgram`)
nix run
```

- `nix build` - build; needs network on first run (fetches pinned git deps + PyPI wheels)
- `nix run` - build and run numtest.py (via `bin/numtest`, `meta.mainProgram`)
- `nix develop` - shell where `python3` is the uv.lock venv python
- `result/bin/ex-reqs-shell/` - the full locked venv, namespaced
  (`ex-reqs-shell/python3`, `ex-reqs-shell/jupyter`, ...), so nothing
  shadows the system `python3`. On NixOS,
  `environment.systemPackages = [ pkg ]` exposes it at
  `/run/current-system/sw/bin/ex-reqs-shell/python3`.


 (requires `uv` on PATH; **deletes and rewrites**
  those three files, so hand-edits to them are lost - 

## Trying both bin layouts

`nix run` works on both branches (each sets `meta.mainProgram`):

    git checkout master && nix run
    # option A (master): venv at bin/ex-reqs-shell/, wrapper is bin/numtest

## Gotchas

- `package.nix` pins the pyproject-nix / uv2nix / build-system-pkgs git revs:
  un-pinned `fetchGit` is an "unlocked" input and fails in pure evaluation
  mode (`nix build`, `nix develop`). Bump revs deliberately.
- Python is 3.12: `numpy==1.26.4` (pinned in `uv.lock`) only ships wheels up
  to cp312, so on 3.13 the wheel is missing and the sdist build fails
  (numpy 1.26.4 does not support 3.13 at all).
- `package.nix` `projectName = "ex-reqs-shell"` must match
  `pyproject.toml` `[project] name`, which `update-lock.sh` hardcodes.
- `myCustomOverrides.nix` is the hook for forcing nixpkgs-built packages
  (torch, pyside6, shiboken6, ...) on top of the uv.lock overlay.

## Dependency/build options considered

For later, if the wheel path stops working:

1. **PyPI wheels on Python 3.12** (current). Stays faithful to `uv.lock`;
   needs network for first-time wheel fetches.
2. **nixpkgs override in `myCustomOverrides.nix`** (e.g.
   `numpy = pkgs.python313Packages.numpy;`). nixpkgs builds from source, no
   wheel needed, works on 3.13; version drifts from `uv.lock`.
3. **Fix sdist source builds** (provide meson-python et al. via
   `build-system-pkgs`). Only viable for packages that actually support the
   chosen Python; useless for numpy 1.26.4 on 3.13.
4. **Drop uv2nix, plain nixpkgs env**
   (`python312.withPackages (ps: [ ps.numpy ])` wrapped around `numtest.py`).
   Fastest and most robust, but abandons the lockfile pipeline this repo
   exists to test.
