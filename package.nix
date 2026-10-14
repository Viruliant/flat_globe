# package.nix
#
# Goal:
#   Keep flake.nix as small as possible and move the uv2nix /
#   pyproject-nix setup into package.nix.
#
# info:
#   - update-lock.sh will regenerate:
#       pyproject.toml
#       uv.lock
#       make sure you manage these files with git in case
#       we need to go back
#   - myCustomOverrides.nix
#       Useful place to force particular nixpkgs versions
#       of packages such as: torch pyside6 shiboken6 etc.
#
# Usage:
#   nix build
#   nix run
#
# so everything must be self-contained.

{ pkgs }:

let
  inherit (pkgs) lib;

  # Pull pyproject-nix ecosystem directly.
  pyproject-nix = import (builtins.fetchGit {
    url = "https://github.com/pyproject-nix/pyproject.nix.git";
  }) {
    inherit lib;
  };

  uv2nix = import (builtins.fetchGit {
    url = "https://github.com/pyproject-nix/uv2nix.git";
  }) {
    inherit pyproject-nix lib;
  };

  pyproject-build-systems = import (builtins.fetchGit {
    url = "https://github.com/pyproject-nix/build-system-pkgs.git";
  }) {
    inherit pyproject-nix uv2nix lib;
  };
  python = pkgs.python313;

  # Load workspace Reads:
  #   pyproject.toml
  #   uv.lock
  workspace = uv2nix.lib.workspace.loadWorkspace {
    workspaceRoot = ./.;
  };

  # Convert uv.lock into an overlay
  # Prefer wheels where available because:
  #   - faster builds
  #   - fewer compilation surprises
  uvLockedOverlay = workspace.mkPyprojectOverlay {
    sourcePreference = "wheel";
  };

  myCustomOverrides =
    import ./myCustomOverrides.nix {
      inherit pkgs python;
    };

  # Construct final python package set Order matters:
  #   1. build-system packages
  #   2. uv lockfile packages
  #   3. custom fixes
  pythonSet =
    (pkgs.callPackage pyproject-nix.build.packages {
      inherit python;
    }).overrideScope (
      lib.composeManyExtensions [
        pyproject-build-systems.overlays.default
        uvLockedOverlay
        myCustomOverrides
      ]
    );

  # in pyproject.toml Must match:
  #   [project]
  #   name = "ex-reqs-shell"
  projectName = "ex-reqs-shell";

  # Build the runtime virtual environment
  # workspace.deps.default comes from pyproject.toml
  appPythonEnv =
    pythonSet.mkVirtualEnv
      "${projectName}-env"
      workspace.deps.default;
  # For now we only need the virtualenv.
  # If the generated package exists, you can expose it:
  #   projectPkg = pythonSet.${projectName};

in

####################################################################

pkgs.stdenv.mkDerivation {
#   pname = "numtest";
  pname = projectName;
  version = "0.1.0";

  src = ./.;

  nativeBuildInputs = [
    appPythonEnv
  ];

  installPhase = ''
    mkdir -p $out/bin
    # Replace numtest.py with your real entrypoint later.
    cat > $out/bin/${projectName} <<EOF
    #!${pkgs.runtimeShell}
    exec ${appPythonEnv}/bin/python $src/numtest.py "\$@"
    EOF
    chmod +x $out/bin/${projectName}
  '';

  meta = with lib; {
    description = "Python environment generated from uv.lock using uv2nix";
    platforms = platforms.all;
  };
}
####################################################################
# Option: Return the virtual environment directly.
# If all you really want is a Python environment generated from
# pyproject.toml + uv.lock, this may be all that's needed.
# this should happen if we do nix develop
####################################################################
# Option: Wrap the environment in a package so nix build / nix run have
# something concrete to produce.
# this should happen if we build
####################################################################
