"""
Common Request payloads are listed here with defaults if necessary.
"""

class CreateStoragePoolRequest:

    def __init__(self, disk_drive_ids=str,
                 raid_level='raid0',
                 name='presentation_pool_1',
                 erase_secured_drives=True):
        self.raidLevel = raid_level
        self.eraseSecuredDrives = erase_secured_drives
        self.diskDriveIds = disk_drive_ids
        self.name = name


class CreateVolumeRequest:

    def __init__(self, pool_id=str,
                 name=str,
                 size=20,
                 seg_size=0):
        self.poolId = pool_id
        self.name = name
        self.size = size
        self.segSize = seg_size
