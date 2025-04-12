# offsets.py - Memory offsets for Counter-Strike 1.6
# Note: These offsets may vary by game version and would need to be updated

class Offsets:
    # Client module
    dwLocalPlayer = 0x00F0F6BC      # Local player pointer
    dwEntityList = 0x00FBEEF4       # Entity list base
    
    # Player offsets
    m_iTeam = 0x9C                  # Team ID
    m_iHealth = 0xA0                # Health
    m_vecOrigin = 0x88              # Position (feet)
    m_vecViewOffset = 0x7C          # Eye position offset from origin
    
    # Engine offsets
    dwViewAngles = 0x00ABCF74       # View angles
    dwClientState = 0x00ABCF60      # Client state
    
    # Bone matrix
    m_dwBoneMatrix = 0x2698         # Bone matrix
    
    # Constants
    BONE_HEAD = 10                  # Head bone index
    MAX_PLAYERS = 32                # Maximum players
