# main.py - Main entry point for CS 1.6 aimbot
import time
import keyboard
import os
import sys
from memory import MemoryManager
from offsets import Offsets
from entity import Player
from aimbot import Aimbot
from config import Config
from vector import Vector3

def clear_console():
    """Clear console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_status(aimbot, fps=0):
    """Print current status"""
    clear_console()
    print("=== CS 1.6 Aimbot ===")
    print(f"Status: {'ACTIVE' if aimbot.is_active else 'INACTIVE'}")
    print(f"FPS: {fps:.1f}")
    print(f"FOV: {aimbot.config.fov_limit}°")
    print(f"Smoothing: {aimbot.config.smoothing}x")
    print(f"Target: {aimbot.config.target_bone}")
    print("\nControls:")
    print(f"  {aimbot.config.toggle_key.upper()}: Toggle aimbot")
    print(f"  {aimbot.config.exit_key.upper()}: Exit program")
    print("\nTarget: " + ("LOCKED" if aimbot.target_lock else "None"))

def main():
    try:
        print("Starting CS 1.6 Aimbot...")
        
        # Initialize components
        config = Config()
        memory = None
        
        # Try to connect to game
        try:
            memory = MemoryManager()
        except Exception as e:
            print(f"Failed to initialize memory: {e}")
            print("Make sure Counter-Strike 1.6 is running")
            input("Press Enter to exit...")
            return
        
        aimbot = Aimbot(memory, config)
        aimbot.initialize()
        
        print("Aimbot initialized.")
        print(f"Press {config.toggle_key.upper()} to toggle aimbot.")
        print(f"Press {config.exit_key.upper()} to exit.")
        
        # Register hotkeys
        keyboard.add_hotkey(config.toggle_key, lambda: toggle_aimbot(aimbot))
        
        # Main loop variables
        running = True
        frame_count = 0
        last_time = time.time()
        fps = 0
        
        while running:
            # Check exit key
            if keyboard.is_pressed(config.exit_key):
                print("Exiting...")
                break
                
            current_time = time.time()
            frame_count += 1
            
            # Calculate FPS every second
            if current_time - last_time >= 1.0:
                fps = frame_count / (current_time - last_time)
                frame_count = 0
                last_time = current_time
                
                # Update status display
                print_status(aimbot, fps)
            
            if aimbot.is_active:
                try:
                    # Get local player
                    local_player_addr = memory.read_int(memory.client_module + Offsets.dwLocalPlayer)
                    if local_player_addr:
                        local_player = Player(memory, local_player_addr)
                        
                        if not local_player.is_valid():
                            time.sleep(0.01)
                            continue
                        
                        # Get all players
                        players = []
                        for i in range(1, Offsets.MAX_PLAYERS):
                            entity_addr = memory.read_int(memory.client_module + Offsets.dwEntityList + i * 4)
                            if entity_addr and entity_addr != local_player_addr:
                                players.append(Player(memory, entity_addr))
                        
                        # Find and aim at best target
                        target = aimbot.get_best_target(local_player, players)
                        if target:
                            aimbot.aim_at_target(target, local_player)
                
                except Exception as e:
                    print(f"Error in main loop: {e}")
                    time.sleep(1)  # Pause on error
            
            # Small sleep to reduce CPU usage
            time.sleep(0.001)
        
        # Save config on exit
        config.save_config()
        
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"Unhandled error: {e}")
        input("Press Enter to exit...")

def toggle_aimbot(aimbot):
    status = "ON" if aimbot.toggle() else "OFF"
    print(f"Aimbot: {status}")

if __name__ == "__main__":
    main()
