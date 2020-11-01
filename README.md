# SE370A2
This assignment uses FUSE for python to create a file system in the userspace of linux. A custom file system was implemented that allowed 2 folders to be mounted. Any modifications to files in these folders are persisted.    
If a new file is created, it is lost upon closure of the custom file system as it is in memory only.

The custom file system is contained in ``a2fuse2.py``
