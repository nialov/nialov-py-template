{ pkgs }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    poetry 
    python38
    python39
    python38Packages.pipx
    pre-commit
    git
    cacert
  ];

  shellHook = with pkgs; ''
    echo Setting environment for shared libraries
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${stdenv.cc.cc.lib}/lib
    export GIT_SSL_CAINFO=${cacert}/etc/ssl/certs/ca-bundle.crt
    export SSL_CERT_FILE=${cacert}/etc/ssl/certs/ca-bundle.crt
    export CURL_CA_BUNDLE=${cacert}/etc/ssl/certs/ca-bundle.crt
    [[ -a .pre-commit-config.yaml ]] && \
      echo "Installing pre-commit hooks"; pre-commit install
  '';
}
