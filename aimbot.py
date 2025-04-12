# aimbot.py - Core aimbot logic
from vector import Vector3, calculate_angle, normalize_angles, calc_fov
from offsets import Offsets
import time
import mouse

class Aimbot:
    def __init__(self, memory_manager, config):
        self.memory = memory_manager
        self.config = config
        self.is_active = False
        self.target_lock = None
        self.last_target_check = 0
        self.view_angles_address = 0
        
    def toggle(self):
        """Toggle aimbot on/off"""
        self.is_active = not self.is_active
        self.target_lock = None  # Reset target lock when toggling
        return self.is_active
    
    def initialize(self):
        """Initialize aimbot with necessary addresses"""
        # Set view angles address
        self.view_angles_address = self.memory.engine_module + Offsets.dwViewAngles
        
    def get_best_target(self, local_player, players):
        """Find the best target based on FOV and distance"""
        current_time = time.time()
        
        # Only search for new target if we don't have one or every 0.2 seconds
        if self.target_lock and current_time - self.last_target_check < 0.2:
            # Check if locked target is still valid
            for player in players:
                if player.base_address == self.target_lock.base_address:
                    if player.is_valid() and player.is_enemy(local_player.team):
                        player.update()  # Update position
                        self.target_lock = player
                        return player
            # Target no longer valid
            self.target_lock = None
        
        # Find new target
        self.last_target_check = current_time
        best_target = None
        best_fov = float('inf')
        
        # Get current view angles
        current_angles = Vector3(
            self.memory.read_float(self.view_angles_address),
            self.memory.read_float(self.view_angles_address + 4),
            0
        )
        
        for player in players:
            if not player.is_valid() or not player.is_enemy(local_player.team):
                continue
                
            # Get target position based on config
            if self.config.target_bone == "head":
                target_pos = player.head_position
            else:
                target_pos = player.position
                
            # Calculate angle to this player
            aim_angle = calculate_angle(local_player.eye_position, target_pos)
            
            # Calculate FOV (angular distance from current view)
            fov = calc_fov(current_angles, aim_angle)
            
            # Check if within configured FOV limit
            if fov < self.config.fov_limit:
                # Check visibility if enabled
                if self.config.check_visibility:
                    if not self.is_visible(local_player.eye_position, target_pos):
                        continue
                
                # Prioritize by FOV (closest to crosshair)
                if fov < best_fov:
                    best_fov = fov
                    best_target = player
        
        self.target_lock = best_target
        return best_target
    
    def is_visible(self, from_pos, to_pos):
        """Check if target is visible (not behind walls)"""
        # This is a simplified implementation
        # A real implementation would use ray tracing through the game's BSP tree
        # or use game-specific functions to check visibility
        
        # For CS 1.6, we could check if there's a direct line of sight
        # This would require more complex implementation with game's trace functions
        
        # For now, we'll assume the target is visible if we found them
        # A more accurate implementation would require game-specific memory reading
        return True
        
    def aim_at_target(self, target, local_player):
        """Aim at the specified target"""
        if not target:
            return False
            
        # Get target position based on config
        if self.config.target_bone == "head":
            target_pos = target.head_position
        else:
            target_pos = target.position
            
        # Calculate angle to target
        aim_angle = calculate_angle(local_player.eye_position, target_pos)
        
        # Apply recoil control if enabled
        if self.config.recoil_control:
            # Note: This is a placeholder. Real recoil control would need
            # game-specific offsets for punch angle
            try:
                # Placeholder offsets - these would need to be updated for actual game
                punch_x = self.memory.read_float(local_player.base_address + 0x3020)
                punch_y = self.memory.read_float(local_player.base_address + 0x3024)
                
                # Adjust aim angle for recoil
                aim_angle.x -= punch_x * self.config.recoil_scale
                aim_angle.y -= punch_y * self.config.recoil_scale
            except Exception:
                # Silently fail if recoil control fails
                pass
        
        # Normalize angles to valid ranges
        aim_angle = normalize_angles(aim_angle)
        
        # Get current view angles
        current_angles = Vector3(
            self.memory.read_float(self.view_angles_address),
            self.memory.read_float(self.view_angles_address + 4),
            0
        )
        
        # Apply smoothing
        smoothing = self.config.smoothing
        
        # Calculate new angles with smoothing
        new_angles = Vector3(
            current_angles.x + (aim_angle.x - current_angles.x) / smoothing,
            current_angles.y + (aim_angle.y - current_angles.y) / smoothing,
            0
        )
        
        # Apply the new angles
        if self.config.use_mouse_movement:
            # Convert angle difference to mouse movement
            mouse_x = int((new_angles.y - current_angles.y) * self.config.mouse_sensitivity)
            mouse_y = int((new_angles.x - current_angles.x) * self.config.mouse_sensitivity)
            
            # Move mouse
            mouse.move(mouse_x, mouse_y, absolute=False)
        else:
            # Write directly to memory
            self.memory.write_float(self.view_angles_address, new_angles.x)
            self.memory.write_float(self.view_angles_address + 4, new_angles.y)
        
        return True
