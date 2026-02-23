{
  description = "ROS2 development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" "x86_64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in
    {
      devShells = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              # Python with packages
              (python311.withPackages (ps: with ps; [
                setuptools
                wheel
                pytest
                flake8
              ]))

              # Colcon build tool
              colcon

              # Build essentials
              cmake
              git
              devcontainer
            ];

            shellHook = ''
              echo "ROS2 development environment (Python + colcon)"
              echo "Python: $(python3 --version)"
              echo ""
              echo "Note: ROS2 core must be installed separately (e.g., via rosdep or system package manager)"
              echo "This shell provides: colcon, python, cmake"
            '';
          };
        }
      );
    };
}
