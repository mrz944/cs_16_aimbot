# offsets.py - Dynamic memory offsets for Counter-Strike 1.6
import random
import time
import struct
import binascii

class PatternScanner:
    """Pattern scanner to find memory signatures dynamically"""
    
    @staticmethod
    def find_pattern(memory_manager, module_base, pattern, mask, offset=0):
        """
        Scan for a byte pattern in memory
        
        Args:
            memory_manager: MemoryManager instance
            module_base: Base address of module to scan
            pattern: Byte pattern to search for
            mask: Mask string where 'x' means check byte, '?' means ignore
            offset: Offset from found pattern to return
            
        Returns:
            Address of found pattern + offset, or 0 if not found
        """
        try:
            # Get module size (approximate)
            module_size = 0x2000000  # 32MB max scan size
            
            # Read module memory in chunks to avoid large reads
            chunk_size = 0x10000  # 64KB chunks
            
            # Add some randomization to scanning to avoid detection
            start_offset = random.randint(0, 0x1000)  # Random start within first 4KB
            
            # Scan memory in chunks
            for chunk_start in range(start_offset, module_size, chunk_size):
                # Add small random delay occasionally
                if random.random() < 0.05:  # 5% chance
                    time.sleep(random.uniform(0.001, 0.005))
                
                # Read chunk
                chunk_data = memory_manager.read_bytes(module_base + chunk_start, min(chunk_size, module_size - chunk_start))
                if not chunk_data or len(chunk_data) < len(pattern):
                    continue
                
                # Scan chunk for pattern
                for i in range(len(chunk_data) - len(pattern) + 1):
                    found = True
                    for j in range(len(pattern)):
                        if mask[j] == 'x' and pattern[j] != chunk_data[i + j]:
                            found = False
                            break
                    
                    if found:
                        return module_base + chunk_start + i + offset
            
            return 0
        except Exception:
            return 0

class OffsetManager:
    """Manager for dynamic offset calculation"""
    
    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.last_update = 0
        self.update_interval = random.uniform(300, 600)  # Update every 5-10 minutes
        self.offsets = {}
        self.fallback_offsets = {
            # Client module
            "dwLocalPlayer": 0x00F0F6BC,      # Local player pointer
            "dwEntityList": 0x00FBEEF4,       # Entity list base
            
            # Player offsets
            "m_iTeam": 0x9C,                  # Team ID
            "m_iHealth": 0xA0,                # Health
            "m_vecOrigin": 0x88,              # Position (feet)
            "m_vecViewOffset": 0x7C,          # Eye position offset from origin
            
            # Engine offsets
            "dwViewAngles": 0x00ABCF74,       # View angles
            "dwClientState": 0x00ABCF60,      # Client state
            
            # Bone matrix
            "m_dwBoneMatrix": 0x2698,         # Bone matrix
        }
        
        # Constants
        self.BONE_HEAD = 10                   # Head bone index
        self.MAX_PLAYERS = 32                 # Maximum players
        
        # Initialize offsets
        self.update_offsets()
    
    def update_offsets(self):
        """Update offsets using pattern scanning"""
        try:
            # Only update if enough time has passed
            current_time = time.time()
            if current_time - self.last_update < self.update_interval:
                return
                
            self.last_update = current_time
            
            # Randomize next update interval (5-10 minutes)
            self.update_interval = random.uniform(300, 600)
            
            print("Updating offsets...")
            
            # Initialize scanner
            scanner = PatternScanner()
            
            # Find LocalPlayer pointer
            # Pattern for CS 1.6 LocalPlayer reference
            local_player_pattern = b"\x8B\x0D\x00\x00\x00\x00\x8B\x01\x8B\x40\x00\xFF\xD0\x85\xC0\x74\x00\x8B"
            local_player_mask = "xx????xxxx?xxxx?x"
            result = scanner.find_pattern(self.memory, self.memory.client_module, local_player_pattern, local_player_mask, 2)
            
            if result:
                # Read the address from the found location
                address_bytes = self.memory.read_bytes(result, 4)
                if address_bytes and len(address_bytes) == 4:
                    self.offsets["dwLocalPlayer"] = struct.unpack("<I", address_bytes)[0] - self.memory.client_module
                    print(f"Found LocalPlayer offset: {hex(self.offsets['dwLocalPlayer'])}")
            else:
                print("LocalPlayer pattern not found, using fallback")
            
            # Find EntityList
            # Pattern for CS 1.6 EntityList reference
            entity_list_pattern = b"\x05\x00\x00\x00\x00\xC1\xE1\x04\x05\x00\x00\x00\x00"
            entity_list_mask = "x????xxxx????"
            result = scanner.find_pattern(self.memory, self.memory.client_module, entity_list_pattern, entity_list_mask, 9)
            
            if result:
                # Read the address from the found location
                address_bytes = self.memory.read_bytes(result, 4)
                if address_bytes and len(address_bytes) == 4:
                    self.offsets["dwEntityList"] = struct.unpack("<I", address_bytes)[0] - self.memory.client_module
                    print(f"Found EntityList offset: {hex(self.offsets['dwEntityList'])}")
            else:
                print("EntityList pattern not found, using fallback")
            
            # Find ViewAngles
            # Pattern for CS 1.6 ViewAngles reference
            view_angles_pattern = b"\xD9\x00\x00\x00\x00\x00\xD8\x0D\x00\x00\x00\x00\xDF\xE0\xF6\xC4\x00\x7A"
            view_angles_mask = "x?????xx????xxx?x"
            result = scanner.find_pattern(self.memory, self.memory.engine_module, view_angles_pattern, view_angles_mask, 1)
            
            if result:
                # Read the address from the found location
                address_bytes = self.memory.read_bytes(result, 4)
                if address_bytes and len(address_bytes) == 4:
                    self.offsets["dwViewAngles"] = struct.unpack("<I", address_bytes)[0] - self.memory.engine_module
                    print(f"Found ViewAngles offset: {hex(self.offsets['dwViewAngles'])}")
            else:
                print("ViewAngles pattern not found, using fallback")
            
            # For player-specific offsets, we can use netvar scanning or hardcoded values
            # For simplicity, we'll use slightly randomized offsets based on the fallbacks
            
            # Add small random variations to player offsets to avoid detection
            # These are structure offsets, so they shouldn't vary much between versions
            variation = random.randint(-2, 2)  # Small variation
            
            self.offsets["m_iTeam"] = self.fallback_offsets["m_iTeam"] + variation
            self.offsets["m_iHealth"] = self.fallback_offsets["m_iHealth"] + variation
            self.offsets["m_vecOrigin"] = self.fallback_offsets["m_vecOrigin"] + variation
            self.offsets["m_vecViewOffset"] = self.fallback_offsets["m_vecViewOffset"] + variation
            self.offsets["m_dwBoneMatrix"] = self.fallback_offsets["m_dwBoneMatrix"] + variation
            
            print(f"Player offsets updated with variation {variation}")
            print(f"m_iTeam: {hex(self.offsets['m_iTeam'])}")
            print(f"m_iHealth: {hex(self.offsets['m_iHealth'])}")
            print(f"m_vecOrigin: {hex(self.offsets['m_vecOrigin'])}")
            print(f"m_vecViewOffset: {hex(self.offsets['m_vecViewOffset'])}")
            print(f"m_dwBoneMatrix: {hex(self.offsets['m_dwBoneMatrix'])}")
            
            # Use fallbacks for any offsets we couldn't find
            for key, value in self.fallback_offsets.items():
                if key not in self.offsets:
                    self.offsets[key] = value
                    print(f"Using fallback for {key}: {hex(value)}")
                    
        except Exception as e:
            # If anything fails, use fallback offsets
            print(f"Error updating offsets: {str(e)}")
            print("Using fallback offsets")
            self.offsets = self.fallback_offsets.copy()

class Offsets:
    """Dynamic offsets for Counter-Strike 1.6"""
    
    # These will be populated at runtime by OffsetManager
    dwLocalPlayer = 0x00F0F6BC      # Local player pointer (fallback)
    dwEntityList = 0x00FBEEF4       # Entity list base (fallback)
    
    # Player offsets
    m_iTeam = 0x9C                  # Team ID (fallback)
    m_iHealth = 0xA0                # Health (fallback)
    m_vecOrigin = 0x88              # Position (feet) (fallback)
    m_vecViewOffset = 0x7C          # Eye position offset from origin (fallback)
    
    # Engine offsets
    dwViewAngles = 0x00ABCF74       # View angles (fallback)
    dwClientState = 0x00ABCF60      # Client state (fallback)
    
    # Bone matrix
    m_dwBoneMatrix = 0x2698         # Bone matrix (fallback)
    
    # Constants
    BONE_HEAD = 10                  # Head bone index
    MAX_PLAYERS = 32                # Maximum players
    
    @classmethod
    def initialize(cls, memory_manager):
        """Initialize offsets with OffsetManager"""
        cls.offset_manager = OffsetManager(memory_manager)
        cls.update_offsets()
    
    @classmethod
    def update_offsets(cls):
        """Update offsets from OffsetManager with better error handling"""
        try:
            if hasattr(cls, 'offset_manager'):
                cls.offset_manager.update_offsets()
                
                # Update class attributes from offset_manager
                for key, value in cls.offset_manager.offsets.items():
                    if hasattr(cls, key):
                        setattr(cls, key, value)
                
                # Print a debug message to confirm offsets were updated
                print("Offsets updated successfully.")
        except Exception as e:
            # Silently continue with fallback offsets
            pass
