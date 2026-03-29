{
  description = "Nix environment for survivalvolume using uv2nix";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

    # Core pyproject-nix ecosystem tools
    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
    };
    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
    };
  };

  outputs = { self, nixpkgs, pyproject-nix, uv2nix, pyproject-build-systems }:
    let
      inherit (nixpkgs) lib;

      # Expose this on major systems (both Linux and macOS)
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = lib.genAttrs systems;
    in
    {
      packages = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python311; # Matches your project target

          # 1. Load the uv workspace
          workspace = uv2nix.lib.workspace.loadWorkspace {
            workspaceRoot = ./.;
          };

          # 2. Create overlay from uv.lock
          uvOverlay = workspace.mkPyprojectOverlay {
            sourcePreference = "wheel"; # Prioritize binary wheels
          };

          # 3. Construct the Python package set
          pythonSet = (pkgs.callPackage pyproject-nix.build.packages {
            inherit python;
          }).overrideScope (lib.composeManyExtensions [
            pyproject-build-systems.overlays.default
            uvOverlay
          ]);

          # 4. Create the final virtual environment linking your dependencies
          env = pythonSet.mkVirtualEnv "survivalvolume-env" workspace.deps.default;
        in
        {
          # This determines what `nix shell .#` runs
          default = env;
        }
      );

      # Fallback devShell in case you want to just run `nix develop`
      devShells = forAllSystems (system: {
        default = nixpkgs.legacyPackages.${system}.mkShell {
          packages = [ self.packages.${system}.default ];
        };
      });
    };
}