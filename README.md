# flat_globe

Testbed for building a Python env from `requirements.bak.txt` with Nix +
uv2nix.

`globe_vs_flat.py` (single source of truth) is converted to a notebook with
`p2j`, executed with `jupyter nbconvert --execute` and shipped as an HTML
report. `nix build` produces the `flat_globe` binary, which opens the report
in your default browser.

## Commands

`nix run github:Viruliant/flat_globe` will "just work"

but if you run the following commands it will "just work" faster
because `Lock2LocalPkgs.sh` will set the flake.lock to your
system packages, and cause less downloading and building.

```bash
# checkout and run with
git clone https://github.com/Viruliant/flat_globe.git ~/flat_globe
cd ~/flat_globe
# requirements.bak.txt (repo root) is the only editable source
# regenerates nix/requirements.txt, nix/pyproject.toml, nix/uv.lock from it
./nix/update-lock.sh
# sets flake.lock to match system nixpkgs
./nix/Lock2LocalPkgs.sh
# run with # opens the report in the default browser (via `meta.mainProgram`)
nix run
```

you can also use this as a playground

```bash
# needs network on first run (fetches pinned git deps + PyPI wheels)
nix build && nix develop
# builds and enters development environment matching whatever you have set in requirements.bak.txt
# do an exmaple run on
./result/bin/flat_globe-env/python3 ./numtest.py
```

- `nix build` - build; needs network on first run (fetches pinned git deps + PyPI wheels)
- `nix run` - build and open the report (via `bin/flat_globe`, `meta.mainProgram`)
- `nix develop` - shell where `python3` is the uv.lock venv python
- `result/bin/flat_globe-env/` - the full locked venv, namespaced
  (`flat_globe-env/python3`, `flat_globe-env/jupyter`, ...), so nothing
  shadows the system `python3`. On NixOS,
  `environment.systemPackages = [ pkg ]` exposes it at
  `/run/current-system/sw/bin/flat_globe-env/python3`.
- `result/share/flat_globe/globe_vs_flat.html` - the executed report

## Build artifacts

`globe_vs_flat.ipynb` and `globe_vs_flat.html` are generated during the build
from `globe_vs_flat.py` (`p2j` + `jupyter nbconvert --to html --execute`) and
are gitignored. To reproduce locally:

```bash
p2j -o -t globe_vs_flat.ipynb globe_vs_flat.py
jupyter nbconvert --to html --execute globe_vs_flat.ipynb
```

## Gotchas

- `package.nix` pins the pyproject-nix / uv2nix / build-system-pkgs git revs:
  un-pinned `fetchGit` is an "unlocked" input and fails in pure evaluation
  mode (`nix build`, `nix develop`). Bump revs deliberately.
- Python is 3.12: `numpy==1.26.4` (pinned in `uv.lock`) only ships wheels up
  to cp312, so on 3.13 the wheel is missing and the sdist build fails
  (numpy 1.26.4 does not support 3.13 at all).
- `package.nix` `projectName = "flat_globe"` must match `pyproject.toml`
  `[project] name`, which `update-lock.sh` hardcodes.
- The namespaced venv lives at `bin/flat_globe-env/` (not `bin/flat_globe/`)
  so it can't collide with the `flat_globe` launcher.
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
