import sys
import subprocess

def main():
    print("=== Current Python Path ===")
    print(sys.executable)
    print("\n=== Installed Packages ===")
    try:
        packages = subprocess.check_output([sys.executable, "-m", "pip", "list"], text=True)
        print(packages)
    except subprocess.CalledProcessError as e:
        print(f"Failed to get packages: {e}")

if __name__ == "__main__":
    main()
