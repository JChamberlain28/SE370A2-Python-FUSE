
#!/usr/bin/env python

# Name: Jack Chamberlain
# UPI (Login): jcha928

from __future__ import print_function, absolute_import, division

import logging

import os
import sys
import errno
from errno import ENOENT
import re

from collections import defaultdict
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit
from time import time


from fuse import FUSE, FuseOSError, Operations, LoggingMixIn, ENOTSUP
from passthrough import Passthrough
from memory import Memory

class A2Fuse2(LoggingMixIn, Operations):
    def __init__(self, root1, root2):
        self.files = {}
        self.data = defaultdict(bytes)
        self.fd = 0
        now = time()
        self.files['/'] = dict(st_mode=(S_IFDIR | 0o755), st_ctime=now,
                               st_mtime=now, st_atime=now, st_nlink=2)

        self.passthrough1 = Passthrough(root1)
        self.passthrough2 = Passthrough(root2)



    def dirCheck(self, path):
        return os.access(path, os.F_OK)

    def getattr(self, path, fh=None):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)


        if self.dirCheck(fullPathRoot1):
            return self.passthrough1.getattr(path)
        elif self.dirCheck(fullPathRoot2):
            return self.passthrough2.getattr(path)
        else:
            if path not in self.files:
                raise FuseOSError(ENOENT)

            return self.files[path]
        




    def readdir(self, path, fh):


        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)

        pathMemExists = path in self.files

        
        
        dirContent = list()
        if self.dirCheck(fullPathRoot1):
            for x in self.passthrough1.readdir(path, fh):
                dirContent.append(x)
            
        if self.dirCheck(fullPathRoot2):
            for y in self.passthrough2.readdir(path, fh):
                dirContent.append(y)


        if pathMemExists:
            for z in (['.', '..'] + [x[1:] for x in self.files if x != '/']):
                dirContent.append(z)

        return dirContent



    def open(self, path, flags):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        

        if self.dirCheck(fullPathRoot1):
            return self.passthrough1.open(path, flags)
        elif self.dirCheck(fullPathRoot2):
            return self.passthrough2.open(path, flags)
        else:
            self.fd += 1
            return self.fd


    def create(self, path, flags):
        # modified existing memory implementation to include UID and GID
        self.files[path] = dict(st_mode=(S_IFREG | flags), 
            st_nlink=1, st_uid=os.getuid(), st_gid=os.getgid(), st_size=0, st_ctime=time(), 
            st_mtime=time(), st_atime=time())

        self.fd += 1
        return self.fd


    def unlink(self, path):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        
        if self.dirCheck(fullPathRoot1):
            return self.passthrough1.unlink(path)
        elif self.dirCheck(fullPathRoot2):
            return self.passthrough2.unlink(path)
        else:
            self.files.pop(path)
    

    def write(self, path, data, offset, fh):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)


        if self.dirCheck(fullPathRoot1):
            return self.passthrough1.write(path, data, offset, fh)
        elif self.dirCheck(fullPathRoot2):
            return self.passthrough2.write(path, data, offset, fh)
        else:
            self.data[path] = self.data[path][:offset] + data
            self.files[path]['st_size'] = len(self.data[path])
            return len(data)

    def read(self, path, size, offset, fh):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)


        if self.dirCheck(fullPathRoot1):
            return self.passthrough1.read(path, size, offset, fh)
        elif self.dirCheck(fullPathRoot2):
            return self.passthrough2.read(path, size, offset, fh)
        else:
            return self.data[path][offset:offset + size]



    def chmod(self, path, mode):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)


        if self.dirCheck(fullPathRoot1):
            return self.passthrough1.chmod(path, mode)
        elif self.dirCheck(fullPathRoot2):
            return self.passthrough2.chmod(path, mode)
        else:
            self.files[path]['st_mode'] &= 0o770000
            self.files[path]['st_mode'] |= mode
            return 0




    def chown(self, path, uid, gid):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)


        if self.dirCheck(fullPathRoot1):
            return self.passthrough1.chown(path, uid, gid)
        elif self.dirCheck(fullPathRoot2):
            return self.passthrough2.chown(path, uid, gid)
        else:
            self.files[path]['st_uid'] = uid
            self.files[path]['st_gid'] = gid


    def getxattr(self, path, name, position=0):
        raise FuseOSError(ENOTSUP)



    def truncate(self, path, length, fh=None):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)

        if self.dirCheck(fullPathRoot1):
            return self.passthrough1.truncate(path, length)
        elif self.dirCheck(fullPathRoot2):
            return self.passthrough2.truncate(path, length)
        else:
            self.data[path] = self.data[path][:length]
            self.files[path]['st_size'] = length



    def utimens(self, path, times=None):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        
        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)

        if pathRoot1Exists:
            return self.passthrough1.utimens(path)
        elif pathRoot2Exists:
            return self.passthrough2.utimens(path)
        else:
            now = time()
            atime, mtime = times if times else (now, now)
            self.files[path]['st_atime'] = atime
            self.files[path]['st_mtime'] = mtime


    def release(self, path, fh):
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)


        if self.dirCheck(fullPathRoot1):
            return self.passthrough1.release(path, fh)
        elif self.dirCheck(fullPathRoot2):
            return self.passthrough2.release(path, fh)
        else:
            pass



def main(mountpoint, root1, root2):
    FUSE(A2Fuse2(root1, root2), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # passes command line arguments into main (mount point is 3rd arg)
    main(sys.argv[3], sys.argv[1], sys.argv[2])


