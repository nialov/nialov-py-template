{
  description = "nix declared development environment";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    let
      mkshell = pkgs:
        let
          poetry-wrapped = pkgs.callPackage ({ writeScriptBin, poetry, stdenv
            , zlib, cacert, python38, python39, lib, execline }:
            let
              pythons = [ python38 python39 ];

              site-packages = lib.concatStringsSep ":" (lib.forEach pythons
                (python: "${python}/${python.sitePackages}"));
              interpreters = lib.concatStringsSep ":"
                (lib.forEach pythons (python: "${python}/bin"));
            in writeScriptBin "poetry" ''
              CLIB="${stdenv.cc.cc.lib}/lib"
              ZLIB="${zlib}/lib"
              CERT="${cacert}/etc/ssl/certs/ca-bundle.crt"

              export GIT_SSL_CAINFO=$CERT
              export SSL_CERT_FILE=$CERT
              export CURL_CA_BUNDLE=$CERT
              export LD_LIBRARY_PATH=$CLIB:$ZLIB

              export PYTHONPATH=${site-packages}
              export PATH=${interpreters}:$PATH
              ${execline}/bin/exec -a "$0" "${poetry}/bin/poetry" "$@"
            '') { };
        in pkgs.mkShell rec {
          packages = with pkgs; [
            pre-commit
            pandoc
            git
            pastel
            nixFlakes
            poetry-wrapped
          ];

          # Required for building C extensions
          # _LD_LIBRARY_PATH = "${stdenv.cc.cc.lib}/lib:${zlib}/lib";
          # Certificates for secure connections for e.g. pip downloads
          # _GIT_SSL_CAINFO = "${cacert}/etc/ssl/certs/ca-bundle.crt";
          # _SSL_CERT_FILE = "${cacert}/etc/ssl/certs/ca-bundle.crt";
          # _CURL_CA_BUNDLE = "${cacert}/etc/ssl/certs/ca-bundle.crt";
          # Required to fully use the python environments
          # PYTHON37PATH = "${python38}/lib/python3.7/site-packages";
          # PYTHON38PATH = "${python38}/lib/python3.8/site-packages";
          # PYTHONPATH is overridden with contents from e.g. poetry */site-package.
          # We do not want them to be in PYTHONPATH.
          # Therefore, in ./.envrc PYTHONPATH is set to the _PYTHONPATH defined below
          # and also in shellHooks (direnv does not load shellHook exports, always).
          # _PYTHONPATH =
          # "${PYTHON37PATH}:${PYTHON38PATH}:${python39}/lib/python3.9/site-packages";

          envrc_contents = ''
            use flake
          '';

          shellHook = ''
            [[ -a .pre-commit-config.yaml ]] && \
              echo "Installing pre-commit hooks"; pre-commit install
            pastel paint -n green "
            Run poetry install to install environment from poetry.lock
            "
            [[ ! -a .envrc ]] && echo -n "$envrc_contents" > .envrc
          '';
        };
    in flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages."${system}";
      in { devShell = mkshell pkgs; });
}
