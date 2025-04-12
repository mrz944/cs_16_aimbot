# config.py - Configuration settings for aimbot
import json
import os

class Config:
    def __init__(self):
        # Aimbot settings
        self.fov_limit = 5.0        # Maximum FOV to acquire targets
        self.smoothing = 2.0        # Higher = smoother aim (less snappy)
        self.use_mouse_movement = True  # Use mouse movement vs memory writing
        self.mouse_sensitivity = 1.0    # Mouse movement sensitivity
        self.target_bone = "head"   # Target bone (head, body)
        self.check_visibility = True # Check if target is visible
        self.recoil_control = True  # Control for recoil
        self.recoil_scale = 2.0     # Recoil compensation scale
        
        # Key bindings
        self.toggle_key = "alt"     # Key to toggle aimbot
        self.exit_key = "end"       # Key to exit program
        
        # Try to load from file
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists("aimbot_config.json"):
                with open("aimbot_config.json", "r") as f:
                    data = json.load(f)
                    
                    # Update config with loaded values
                    for key, value in data.items():
                        if hasattr(self, key):
                            setattr(self, key, value)
                            
                print("Configuration loaded from file")
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            # Convert config to dict
            config_dict = {key: value for key, value in self.__dict__.items()}
            
            with open("aimbot_config.json", "w") as f:
                json.dump(config_dict, f, indent=4)
                
            print("Configuration saved to file")
        except Exception as e:
            print(f"Error saving config: {e}")
