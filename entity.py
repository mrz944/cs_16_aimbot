# entity.py - Player entity management
from offsets import Offsets
from vector import Vector3

class Player:
    def __init__(self, memory, base_address):
        self.memory = memory
        self.base_address = base_address
        self.position = Vector3(0, 0, 0)
        self.eye_position = Vector3(0, 0, 0)
        self.head_position = Vector3(0, 0, 0)
        self.health = 0
        self.team = 0
        self.update()
        
    def update(self):
        """Update player data from memory"""
        try:
            self.health = self.memory.read_int(self.base_address + Offsets.m_iHealth)
            self.team = self.memory.read_int(self.base_address + Offsets.m_iTeam)
            
            # Get position (feet)
            x = self.memory.read_float(self.base_address + Offsets.m_vecOrigin)
            y = self.memory.read_float(self.base_address + Offsets.m_vecOrigin + 4)
            z = self.memory.read_float(self.base_address + Offsets.m_vecOrigin + 8)
            self.position = Vector3(x, y, z)
            
            # Get eye position (feet + view offset)
            view_offset_x = self.memory.read_float(self.base_address + Offsets.m_vecViewOffset)
            view_offset_y = self.memory.read_float(self.base_address + Offsets.m_vecViewOffset + 4)
            view_offset_z = self.memory.read_float(self.base_address + Offsets.m_vecViewOffset + 8)
            self.eye_position = Vector3(
                x + view_offset_x,
                y + view_offset_y,
                z + view_offset_z
            )
            
            # Get head position from bone matrix
            self.head_position = self.get_bone_position(Offsets.BONE_HEAD)
            
        except Exception as e:
            # Silent fail - this is common when players disconnect or memory changes
            pass
    
    def get_bone_position(self, bone_id):
        """Get position of specific bone from bone matrix"""
        try:
            bone_matrix_ptr = self.memory.read_int(self.base_address + Offsets.m_dwBoneMatrix)
            
            if bone_matrix_ptr:
                x = self.memory.read_float(bone_matrix_ptr + 0x30 * bone_id + 0x0C)
                y = self.memory.read_float(bone_matrix_ptr + 0x30 * bone_id + 0x1C)
                z = self.memory.read_float(bone_matrix_ptr + 0x30 * bone_id + 0x2C)
                return Vector3(x, y, z)
            
            return self.position  # Fallback to body position
            
        except Exception:
            return self.position  # Fallback to body position
    
    def is_valid(self):
        """Check if player is valid target"""
        return self.health > 0 and self.base_address != 0
        
    def is_enemy(self, local_team):
        """Check if player is enemy"""
        return self.team != local_team and self.team in [1, 2]  # 1=T, 2=CT
