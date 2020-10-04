
#!/usr/bin/env python

from __future__ import print_function, absolute_import, division

import logging

import os
import sys
import errno

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
from passthrough import Passthrough
from memory import Memory

class A2Fuse2(Memory):
    def __init__(self, root1, root2):
        # Initialise the Memory class that is inherited in this class
        super().__init__()
        self.passthrough1 = Passthrough(root1)
        self.passthrough2 = Passthrough(root2)

    def getattr(self, path, fh=None):
        try:
            # try in first source folder
            return self.passthrough1.getattr(path)
        except FileNotFoundError:
            try:
                # not found error in first, so try in second
                return self.passthrough2.getattr(path)
            except FileNotFoundError:
                # not found in second so try in 3rd
                return super().getattr(path)


    # def getattr(self, path, fh=None):


    #     # get hypothetical path for both source folders
    #     fullPathRoot1 = self.passthrough1._full_path(path)
    #     fullPathRoot2 = self.passthrough2._full_path(path)

    #     pathRoot1Exists = os.path.isdir(fullPathRoot1)
    #     pathRoot2Exists = os.path.isdir(fullPathRoot2)

    #     #if  pathRoot1Exists & pathRoot2Exists:
    #         # directory / file exists in both source folders so both are read
    #        # return self.passthrough1.readdir(path) + self.passthrough2.readdir(path)
    #     if pathRoot1Exists:
    #         return self.passthrough1.getattr(path)
    #     elif pathRoot2Exists:
    #         return self.passthrough2.getattr(path)
    #     else:
    #         return super().getattr(path)




    def readdir(self, path, fh):

        # if path for root 1 and root 2 exists, assume operation performed on both??? NOT DONE

        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)

        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)
        pathMemExists = path in self.files

        
        # directory / file exists in both source folders so both are read
        dirList = list()
        if pathRoot2Exists:
            for x in self.passthrough2.readdir(path, fh):
                dirList.append(x)
            
        if pathRoot1Exists:
            for y in self.passthrough1.readdir(path, fh):
                dirList.append(y)


        if pathMemExists:
            for z in super().readdir(path, fh):
                dirList.append(z)

        return dirList

        # elif pathRoot2Exists:
        #     return self.passthrough2.readdir(path, fh)
        # elif pathRoot1Exists:
        #     return self.passthrough1.readdir(path, fh)
        # else:
        #     return super().getattr(path)


    def open(self, path, flags):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        
        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)

        if pathRoot1Exists:
            return self.passthrough1.open(path, flags)
        elif pathRoot2Exists:
            return self.passthrough2.open(path, flags)
        else:
            return super().open(path, flags)


    def create(self, path, flags): ## should we check if exists in source folders first??? HELP ##################
        # Only allows creation of new files in memory file system
        return super().create(path, flags) ################################ is mode flags???


    def unlink(self, path):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        
        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)

        if pathRoot1Exists:
            return self.passthrough1.unlink(path)
        elif pathRoot2Exists:
            return self.passthrough2.unlink(path)
        else:
            return super().unlink(path)
    

    def write(self, path, data, offset, fh):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        
        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)

        if pathRoot1Exists:
            return self.passthrough1.write(path, data, offset, fh)
        elif pathRoot2Exists:
            return self.passthrough2.write(path, data, offset, fh)
        else:
            return super().write(path, data, offset, fh)

    def read(self, path, size, offset, fh):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        
        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)

        if pathRoot1Exists:
            return self.passthrough1.read(path, size, offset, fh)
        elif pathRoot2Exists:
            return self.passthrough2.read(path, size, offset, fh)
        else:
            return super().read(path, size, offset, fh)



    def chmod(self, path, mode):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        
        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)

        if pathRoot1Exists:
            return self.passthrough1.chmod(path, mode)
        elif pathRoot2Exists:
            return self.passthrough2.chmod(path, mode)
        else:
            return super().chmod(path, mode)




    def chown(self, path, uid, gid):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        
        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)

        if pathRoot1Exists:
            return self.passthrough1.chown(path, uid, gid)
        elif pathRoot2Exists:
            return self.passthrough2.chown(path, uid, gid)
        else:
            return super().chown(path, uid, gid)


    def getxattr(self, path, name, position=0):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        
        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)

        if pathRoot1Exists:
            return self.passthrough1.getxattr(path, name, position=0)
        elif pathRoot2Exists:
            return self.passthrough2.getxattr(path, name, position=0)
        else:
            return super().getxattr(path, name, position=0)


    def listxattr(self, path):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        
        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)

        if pathRoot1Exists:
            return self.passthrough1.listxattr(path)
        elif pathRoot2Exists:
            return self.passthrough2.listxattr(path)
        else:
            return super().listxattr(path)

    # def mkdir(self, path, mode):
    #     return super().mkdir(path, mode)





    def readlink(self, path):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        
        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)

        if pathRoot1Exists:
            return self.passthrough1.readlink(path)
        elif pathRoot2Exists:
            return self.passthrough2.readlink(path)
        else:
            return super().readlink(path)

    def removexattr(self, path, name):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        
        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)

        if pathRoot1Exists:
            return self.passthrough1.removexattr(path, name)
        elif pathRoot2Exists:
            return self.passthrough2.removexattr(path, name)
        else:
            return super().removexattr(path, name)

    def rename(self, old, new):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(old)
        fullPathRoot2 = self.passthrough2._full_path(old)
        
        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)

        if pathRoot1Exists:
            return self.passthrough1.rename(old, new)
        elif pathRoot2Exists:
            return self.passthrough2.rename(old, new)
        else:
            return super().rename(old, new)


    def rmdir(self, path):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        
        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)

        if pathRoot1Exists:
            return self.passthrough1.rmdir(path)
        elif pathRoot2Exists:
            return self.passthrough2.rmdir(path)
        else:
            return super().rmdir(path)

    def setxattr(self, path, name, value, options, position=0):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        
        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)

        if pathRoot1Exists:
            return self.passthrough1.setxattr(path, name, value, options, position=0)
        elif pathRoot2Exists:
            return self.passthrough2.setxattr(path, name, value, options, position=0)
        else:
            return super().setxattr(path, name, value, options, position=0)


    def statfs(self, path):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        
        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)

        if pathRoot1Exists:
            return self.passthrough1.statfs(path)
        elif pathRoot2Exists:
            return self.passthrough2.statfs(path)
        else:
            return super().statfs(path)


    # def symlink(self, target, source):



    def truncate(self, path, length, fh=None):
        # get hypothetical path for both source folders
        fullPathRoot1 = self.passthrough1._full_path(path)
        fullPathRoot2 = self.passthrough2._full_path(path)
        
        pathRoot1Exists = os.path.isdir(fullPathRoot1)
        pathRoot2Exists = os.path.isdir(fullPathRoot2)

        if pathRoot1Exists:
            return self.passthrough1.truncate(path, length)
        elif pathRoot2Exists:
            return self.passthrough2.truncate(path, length)
        else:
            return super().truncate(path, length)



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
            return super().utimens(path)


def main(mountpoint, root1, root2):
    FUSE(A2Fuse2(root1, root2), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # passes command line arguments into main (mount point is 3rd arg)
    main(sys.argv[3], sys.argv[1], sys.argv[2])


