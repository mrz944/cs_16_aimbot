# memory.py - Memory reading/writing functionality
from pymem import Pymem
from pymem.process import module_from_name
import time
import psutil
import sys

class MemoryManager:
    def __init__(self):
        self.process = None
        self.client_module = None
        self.engine_module = None
        self.connect_to_game()
        
    def connect_to_game(self):
        """Find and connect to CS 1.6 process"""
        print("Looking for CS 1.6 process...")
        
        # Common process names for CS 1.6
        process_names = ["hl.exe", "cstrike.exe", "cs.exe"]
        
        # Try to find the process
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] in process_names:
                try:
                    self.process = Pymem(proc.info['name'])
                    print(f"Connected to {proc.info['name']}")
                    break
                except Exception as e:
                    print(f"Failed to connect: {e}")
        
        # If process not found
        if not self.process:
            print("CS 1.6 not found. Make sure the game is running.")
            print("The aimbot will continue to search for the process.")
            print("Start CS 1.6 and the aimbot will connect automatically.")
            
            # Keep trying to connect
            retry_count = 0
            while not self.process and retry_count < 30:  # Try for about 30 seconds
                time.sleep(1)
                retry_count += 1
                
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'] in process_names:
                        try:
                            self.process = Pymem(proc.info['name'])
                            print(f"Connected to {proc.info['name']}")
                            break
                        except Exception:
                            pass
            
            if not self.process:
                print("Could not find CS 1.6 process after multiple attempts.")
                print("Please start CS 1.6 and run this program again.")
                sys.exit(1)
        
        # Get modules
        try:
            self.client_module = module_from_name(self.process.process_handle, "client.dll").lpBaseOfDll
            self.engine_module = module_from_name(self.process.process_handle, "hw.dll").lpBaseOfDll
            print("Modules loaded successfully")
        except Exception as e:
            print(f"Failed to load modules: {e}")
            print("This could be due to an unsupported game version.")
            sys.exit(1)
    
    def read_int(self, address):
        """Read 4-byte integer from memory"""
        try:
            return self.process.read_int(address)
        except Exception:
            return 0
    
    def read_float(self, address):
        """Read 4-byte float from memory"""
        try:
            return self.process.read_float(address)
        except Exception:
            return 0.0
    
    def read_bytes(self, address, size):
        """Read bytes from memory"""
        try:
            return self.process.read_bytes(address, size)
        except Exception:
            return b'\x00' * size
    
    def write_int(self, address, value):
        """Write 4-byte integer to memory"""
        try:
            self.process.write_int(address, value)
            return True
        except Exception:
            return False
    
    def write_float(self, address, value):
        """Write 4-byte float to memory"""
        try:
            self.process.write_float(address, value)
            return True
        except Exception:
            return False
    
    def write_bytes(self, address, value):
        """Write bytes to memory"""
        try:
            self.process.write_bytes(address, value, len(value))
            return True
        except Exception:
            return False
