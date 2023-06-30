{ lib, buildPythonPackage, pytestCheckHook, doit, poetry-core
, pytest-regressions, poetry2nix }:

buildPythonPackage {
  pname = "doit-ext";
  version = "0.1";
  format = "pyproject";

  # src = ./.;
  src = let
    # Filter from src paths with given suffixes (full name can be given as suffix)
    excludeSuffixes = [ ".flake8" ".nix" "docs_src" "flake.lock" ];
    # anyMatches returns true if any suffix matches
    anyMatches = path:
      (builtins.any (value: lib.hasSuffix value (baseNameOf path))
        excludeSuffixes);

  in builtins.filterSource (path: _:
    # Apply the anyMatches filter and reverse the result with !
    # as we want to EXCLUDE rather than INCLUDE
    !(anyMatches path)) (poetry2nix.cleanPythonSources { src = ./.; });

  nativeBuildInputs = [ poetry-core ];
  propagatedBuildInputs = [ doit ];

  checkInputs = [ pytestCheckHook pytest-regressions ];

  pythonImportsCheck = [ "doit_ext" ];

  meta = with lib; {
    description = "doit-ext";
    homepage = "https://github.com/nialov/doit-ext";
    license = licenses.mit;
    maintainers = with maintainers; [ nialov ];
  };
}
