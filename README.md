# CS 1.6 Aimbot

A simple aimbot for Counter-Strike 1.6 created for educational purposes.

## Disclaimer

This project is for **educational purposes only**. Using aimbots or any other cheating software in online games:
- Violates the game's terms of service
- Can result in permanent bans
- Ruins the gaming experience for other players

The author does not condone or encourage cheating in online games. This project is meant to demonstrate concepts related to game memory manipulation and should only be used in controlled environments for learning.

## Features

- Player detection and targeting
- FOV-based target selection
- Configurable aim smoothing
- Head/body targeting options
- Recoil control
- Toggle functionality with hotkeys
- Status display with FPS counter

## Requirements

- Python 3.6+
- Counter-Strike 1.6
- Windows operating system

## Installation

1. Clone or download this repository
2. Run the setup script to install required packages:
   ```
   python setup.py
   ```

## Usage

1. Start Counter-Strike 1.6
2. Run the aimbot:
   ```
   python main.py
   ```
3. Use the ALT key to toggle the aimbot on/off
4. Press END key to exit the program

## Configuration

The aimbot can be configured by editing the `aimbot_config.json` file that will be created after the first run. Available settings include:

- `fov_limit`: Maximum field of view for target acquisition (degrees)
- `smoothing`: Aim smoothing factor (higher = smoother)
- `use_mouse_movement`: Whether to use mouse movement or memory writing
- `mouse_sensitivity`: Sensitivity for mouse movement
- `target_bone`: Target bone ("head" or "body")
- `check_visibility`: Whether to check if targets are visible
- `recoil_control`: Whether to compensate for recoil
- `recoil_scale`: Recoil compensation scale
- `toggle_key`: Key to toggle aimbot on/off
- `exit_key`: Key to exit the program

## Technical Details

The aimbot works by:
1. Reading the game's memory to find player positions
2. Calculating angles to enemy players
3. Selecting the best target based on FOV
4. Smoothly adjusting aim to the target

Memory offsets are specific to CS 1.6 and may need to be updated for different game versions.

## Files

- `main.py`: Main entry point
- `memory.py`: Memory reading/writing functionality
- `offsets.py`: Game memory offsets
- `entity.py`: Player entity management
- `aimbot.py`: Core aimbot logic
- `vector.py`: Vector calculations
- `config.py`: Configuration management
- `setup.py`: Installation script

## Limitations

- Memory offsets may vary by game version
- Visibility checks are simplified
- Recoil control requires specific offsets
- May not work with all anti-cheat systems

## Educational Value

This project demonstrates:
- Game memory manipulation
- Process memory reading/writing
- Vector mathematics for 3D games
- Player entity management
- Configuration systems
