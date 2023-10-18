{
  description = "nix declared development environment";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    # nix-extra = {
    #   url = "github:nialov/nix-extra";
    #   inputs.nixpkgs.follows = "nixpkgs";
    # };
    flake-utils.url = "github:numtide/flake-utils";
    pre-commit-hooks = { url = "github:cachix/pre-commit-hooks.nix"; };
  };

  outputs = { self, nixpkgs, flake-utils, ... }@inputs:
    flake-utils.lib.eachSystem [ flake-utils.lib.system.x86_64-linux ] (system:
      let
        # Initialize nixpkgs for system
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ ];
        };

        devShellPackages = with pkgs; [ pre-commit pandoc copier ];

      in {
        checks = {
          preCommitCheck = inputs.pre-commit-hooks.lib.${system}.run
            (import ././pre-commit.nix { inherit pkgs; });
        };
        packages = {
          # TODO: Use from template/flake.nix
          update-changelog = pkgs.writeShellApplication {
            name = "update-changelog";
            runtimeInputs = with pkgs; [
              clog-cli
              ripgrep
              git
              gnused
              coreutils
              pandoc
            ];
            text = ''
              homepage="https://github.com/nialov/nialov-py-template"
              version="$(git tag --sort=-creatordate | head -n 1 | sed 's/v\(.*\)/\1/')"
              clog --repository "$homepage" --subtitle "Release Changelog $version" "$@"
            '';
          };
          template-test = pkgs.writeShellApplication {
            name = "template-test";
            runtimeInputs =
              self.devShells."${system}".default.nativeBuildInputs;
            text =
              let renderedTemplate = self.packages."${system}".render-template;

              in ''
                set -x
                tmpdir="$(mktemp -d -u)"
                cp -r ${renderedTemplate} "$tmpdir"

                cd "$tmpdir"
                nix build .#devShells.x86_64-linux.default --no-link --no-write-lock-file
              '';
          };
          render-template = let
            copierAnswers = builtins.concatStringsSep " "
              (builtins.map (data: "--data ${data}") [
                "year=2023"
                "package=testpackage"
                "full_name='First Last'"
                "description='Test rendering of template'"
                "github_account=tester"
                "email=tester@example.com"
              ]);

          in pkgs.runCommand "render-template" {
            nativeBuildInputs = with pkgs; [ copier git ];
          }

          ''
            export HOME=$(mktemp -d)
            source=${pkgs.lib.cleanSource ./.}
            tmpdir="$(mktemp -d -u)"
            cp -r $source $tmpdir
            chmod -R 777 $tmpdir

            cd $tmpdir
            git init
            git add -A .
            git config --global user.email "nixpkgs"
            git config --global user.name "nixpkgs"
            git commit -m "copier requires git"

            copier ${copierAnswers} --vcs-ref HEAD --force . $out
          '';
        };
        devShells = {
          default = pkgs.mkShell {
            packages = devShellPackages;
            inherit (self.checks.${system}.preCommitCheck) shellHook;
          };
        };
      });

}
