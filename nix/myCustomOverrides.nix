# myCustomOverrides.nix
{ pkgs, python }:

final: prev: {
#     pyside6 = pkgs.python312Packages.pyside6;
#     shiboken6 = pkgs.python312Packages.shiboken6;
#     torch = pkgs.python313Packages.torch;

  # Force Torch to use a specific version from nixpkgs
#   torch = pkgs.python312Packages.torch;

#   torch = pkgs.python312Packages.torchWithRocm;
  # Add Vulkan Python bindings (if available in nixpkgs)
#   vulkan = pkgs.python312Packages.vulkan;
#           shiboken2 = python.pkgs.buildPythonPackage rec {
#             pname = "shiboken2";
#             version = "5.15.2.1";
#             format = "other";
#             src = pkgs.fetchurl {
#               url = "https://download.qt.io/official_releases/QtForPython/shiboken2/PySide2-${version}-src/pyside-setup-opensource-src-${version}.tar.gz";
#               hash = "sha256-14dk2gblh8h70gfw0l2ld4aqcmryf0li0krf7h2v1sri7d78xrwi";
#             };
#             nativeBuildInputs = [
#               pkgs.cmake
#               pkgs.llvmPackages.clang
#             ];
#             buildInputs = [
#               pkgs.qt5.full
#               pkgs.wayland
#               pkgs.libxkbcommon
#               pkgs.libxcomposite
#               pkgs.pulseaudio
#               pkgs.libx11
#               pkgs.libxcb
#               pkgs.libdrm
#               pkgs.vulkan-loader
#               pkgs.gst_all_1.gstreamer
#               pkgs.gst_all_1.gst-plugins-base
#               pkgs.alsa-lib
#               pkgs.gtk3
#               pkgs.atk
#               pkgs.pango
#               pkgs.cairo
#               pkgs.gdk-pixbuf
#               pkgs.speechd
#               pkgs.xorg.libXtst
#               pkgs.xorg.xcbutil
#               pkgs.xorg.xcbutilwm
#               pkgs.xorg.xcbutilimage
#               pkgs.xorg.xcbutilkeysyms
#               pkgs.xorg.xcbutilrenderutil
#               pkgs.unixODBC
#               pkgs.postgresql
#               pkgs.nss
#               pkgs.nspr
#             ];
#             doCheck = false; # Disable tests to avoid common failures
#             meta = with pkgs.lib; {
#               description = "Generator runner for Shiboken2";
#               license = licenses.lgpl3;
#               homepage = "https://wiki.qt.io/Qt_for_Python";
#               maintainers = with maintainers; [ gebner ];
#             };
#           };
#           pyside2 = python.pkgs.buildPythonPackage rec {
#             pname = "pyside2";
#             version = "5.15.2.1";
#             format = "other";
#             src = pkgs.fetchurl {
#               url = "https://download.qt.io/official_releases/QtForPython/pyside2/PySide2-${version}-src/pyside-setup-opensource-src-${version}.tar.gz";
#               hash = "sha256-14dk2gblh8h70gfw0l2ld4aqcmryf0li0krf7h2v1sri7d78xrwi";
#             };
#             nativeBuildInputs = [
#               pkgs.cmake
#               pkgs.llvmPackages.clang
#               final.shiboken2
#             ];
#             buildInputs = [
#               pkgs.wayland
#               pkgs.libxkbcommon
#               pkgs.libxcomposite
#               pkgs.pulseaudio
#               pkgs.libx11
#               pkgs.libxcb
#               pkgs.libdrm
#               pkgs.vulkan-loader
#               pkgs.gst_all_1.gstreamer
#               pkgs.gst_all_1.gst-plugins-base
#               pkgs.alsa-lib
#               pkgs.gtk3
#               pkgs.atk
#               pkgs.pango
#               pkgs.cairo
#               pkgs.gdk-pixbuf
#               pkgs.speechd
#               pkgs.xorg.libXtst
#               pkgs.xorg.xcbutil
#               pkgs.xorg.xcbutilwm
#               pkgs.xorg.xcbutilimage
#               pkgs.xorg.xcbutilkeysyms
#               pkgs.xorg.xcbutilrenderutil
#               pkgs.unixODBC
#               pkgs.postgresql
#               pkgs.nss
#               pkgs.nspr
#             ];
#             propagatedBuildInputs = [ pkgs.qt5.full ];
#             doCheck = false; # Disable tests to avoid common failures
#             meta = with pkgs.lib; {
#               description = "Python bindings for Qt5";
#               license = licenses.lgpl3;
#               homepage = "https://wiki.qt.io/Qt_for_Python";
#               maintainers = with maintainers; [ gebner ];
#             };
#           };

}
