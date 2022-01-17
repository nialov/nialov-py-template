{ pkgs }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    poetry 
    python37
    python38
    python39
    pre-commit
    git
    cacert
  ];

  shellHook = with pkgs; ''
    echo Welcome to nix shell.
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${stdenv.cc.cc.lib}/lib
    export GIT_SSL_CAINFO=${cacert}/etc/ssl/certs/ca-bundle.crt
    export SSL_CERT_FILE=${cacert}/etc/ssl/certs/ca-bundle.crt
    export CURL_CA_BUNDLE=${cacert}/etc/ssl/certs/ca-bundle.crt
  '';
}
