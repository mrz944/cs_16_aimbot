# setup.py - Installation script for CS 1.6 aimbot
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    
    requirements = [
        "pymem",
        "pywin32",
        "keyboard",
        "mouse",
        "numpy",
        "psutil"
    ]
    
    for req in requirements:
        print(f"Installing {req}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
            print(f"Successfully installed {req}")
        except Exception as e:
            print(f"Error installing {req}: {e}")
            print("You may need to install this package manually.")
    
    print("\nAll requirements processed.")

def print_instructions():
    """Print usage instructions"""
    print("\n=== CS 1.6 Aimbot Setup Complete ===")
    print("\nUsage Instructions:")
    print("1. Start Counter-Strike 1.6")
    print("2. Run the aimbot with: python main.py")
    print("3. Use ALT key to toggle the aimbot on/off")
    print("4. Press END key to exit the program")
    print("\nConfiguration:")
    print("- Edit aimbot_config.json to customize settings")
    print("- Adjust FOV, smoothing, and other parameters as needed")
    print("\nNote: This aimbot is for educational purposes only.")
    print("Using it in online games may violate terms of service and result in bans.")

if __name__ == "__main__":
    try:
        print("=== CS 1.6 Aimbot Setup ===")
        install_requirements()
        print_instructions()
        input("\nPress Enter to exit setup...")
    except Exception as e:
        print(f"\nError during setup: {e}")
        input("Press Enter to exit...")
