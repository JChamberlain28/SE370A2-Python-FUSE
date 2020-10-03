# SOFTENG 370 A2 Answers
Note: This beutifil markdown has to be made .txt for submission >:(

## Question 1

### Explain the output you have just seen in terminal two. What did you see and why was it like that?

### Output:

```shell
jack@DESKTOP-Q6QKAUO:~/SE370A2$ ls -l source 
total 12
-rw-r--r-- 1 jack jack 2 Oct  1 01:59 one
-rw-r--r-- 1 jack jack 2 Oct  1 01:59 three
-rw-r--r-- 1 jack jack 2 Oct  1 01:59 two

jack@DESKTOP-Q6QKAUO:~/SE370A2$ ls -l mount
total 0
-rw-r--r-- 1 jack jack 2 Oct  1 01:59 one
-rw-r--r-- 1 jack jack 2 Oct  1 01:59 three
-rw-r--r-- 1 jack jack 2 Oct  1 01:59 two
```

### Answer:   
The output for both reading the source folder contents directly and the mounted file system are the same. This is because a passthrough file system is being used for the mount directory. The passthrough file system is defined in ```passthrough.py```. All file system operations defined 'recall' the same operations using the python 'os' module. When recalling, the root file system passed in to the Main function (in this case "source") is used. Therefore all file system operations are redirected to be performed by the OS on the "source" folder.   

## Question 2

### For each command in terminal two, copy the output from terminal 1 (user space file system logging) and explain each method call.   


### I THINK SOMETHING IS BROKEN COS OUTPUTS TOO LONG + ERRORS. HELP!

### Output and Explanation:
Command:   
```
cd mount
```
Output:
```
DEBUG:fuse.log-mixin:-> getattr / (None,)
DEBUG:fuse.log-mixin:<- getattr {'st_atime': 1601521110.04, 'st_ctime': 1601521109.25, 'st_gid': 1000, 'st_mode': 16877, 'st_mtime': 1601521109.25, 'st_nlink': 2, 'st_size': 4096, 'st_uid': 1000}
DEBUG:fuse.log-mixin:-> access / (1,)
DEBUG:fuse.log-mixin:<- access None
```

Explanation: 
Command:   
```
cat > newfile
```
 
Output:   
```
DEBUG:fuse.log-mixin:-> getattr / (None,)
DEBUG:fuse.log-mixin:<- getattr {'st_atime': 1601521110.04, 'st_ctime': 1601521109.25, 'st_gid': 1000, 'st_mode': 16877, 'st_mtime': 1601521109.25, 'st_nlink': 2, 'st_size': 4096, 'st_uid': 1000}
DEBUG:fuse.log-mixin:-> getattr /newfile (None,)
DEBUG:fuse.log-mixin:<- getattr "[Errno 2] No such file or directory: 'source/newfile'"
DEBUG:fuse:FUSE operation getattr raised a <class 'FileNotFoundError'>, returning errno 2.
Traceback (most recent call last):
  File "/home/jack/SE370A2/fuse.py", line 731, in _wrapper
    return func(*args, **kwargs) or 0
  File "/home/jack/SE370A2/fuse.py", line 771, in getattr
    return self.fgetattr(path, buf, None)
  File "/home/jack/SE370A2/fuse.py", line 1024, in fgetattr
    attrs = self.operations('getattr', self._decode_optional_path(path), fh)
  File "/home/jack/SE370A2/fuse.py", line 1240, in __call__
    ret = getattr(self, op)(path, *args)
  File "/home/jack/SE370A2/passthrough.py", line 43, in getattr
    st = os.lstat(full_path)
FileNotFoundError: [Errno 2] No such file or directory: 'source/newfile'
DEBUG:fuse.log-mixin:-> create /newfile (33188,)
DEBUG:fuse.log-mixin:<- create 4
DEBUG:fuse.log-mixin:-> getattr /newfile (4,)
DEBUG:fuse.log-mixin:<- getattr {'st_atime': 1601521307.29, 'st_ctime': 1601521307.29, 'st_gid': 1000, 'st_mode': 33188, 'st_mtime': 1601521307.29, 'st_nlink': 1, 'st_size': 0, 'st_uid': 1000}
DEBUG:fuse.log-mixin:-> flush /newfile (4,)
DEBUG:fuse.log-mixin:<- flush None
DEBUG:fuse.log-mixin:-> getattr / (None,)
DEBUG:fuse.log-mixin:<- getattr {'st_atime': 1601521307.29, 'st_ctime': 1601521307.29, 'st_gid': 1000, 'st_mode': 16877, 'st_mtime': 1601521307.29, 'st_nlink': 2, 'st_size': 4096, 'st_uid': 1000}
DEBUG:fuse.log-mixin:-> opendir / ()
DEBUG:fuse.log-mixin:<- opendir 0
DEBUG:fuse.log-mixin:-> readdir / (0,)
DEBUG:fuse.log-mixin:<- readdir <generator object Passthrough.readdir at 0x7fa8aad89dd0>
DEBUG:fuse.log-mixin:-> releasedir / (0,)
DEBUG:fuse.log-mixin:<- releasedir 0
DEBUG:fuse.log-mixin:-> getattr /one (None,)
DEBUG:fuse.log-mixin:<- getattr {'st_atime': 1601470779.13, 'st_ctime': 1601470763.1, 'st_gid': 1000, 'st_mode': 33188, 'st_mtime': 1601470763.117, 'st_nlink': 1, 'st_size': 2, 'st_uid': 1000}
DEBUG:fuse.log-mixin:-> getattr /three (None,)
DEBUG:fuse.log-mixin:<- getattr {'st_atime': 1601470762.89, 'st_ctime': 1601470762.86, 'st_gid': 1000, 'st_mode': 33188, 'st_mtime': 1601470762.873, 'st_nlink': 1, 'st_size': 2, 'st_uid': 1000}
DEBUG:fuse.log-mixin:-> getattr /two (None,)
DEBUG:fuse.log-mixin:<- getattr {'st_atime': 1601470779.13, 'st_ctime': 1601470763.02, 'st_gid': 1000, 'st_mode': 33188, 'st_mtime': 1601470763.022, 'st_nlink': 1, 'st_size': 2, 'st_uid': 1000}
DEBUG:fuse.log-mixin:-> getattr / (None,)
DEBUG:fuse.log-mixin:<- getattr {'st_atime': 1601521308.12, 'st_ctime': 1601521307.29, 'st_gid': 1000, 'st_mode': 16877, 'st_mtime': 1601521307.29, 'st_nlink': 2, 'st_size': 4096, 'st_uid': 1000}
DEBUG:fuse.log-mixin:-> getattr /.gitignore (None,)
DEBUG:fuse.log-mixin:<- getattr "[Errno 2] No such file or directory: 'source/.gitignore'"
DEBUG:fuse:FUSE operation getattr raised a <class 'FileNotFoundError'>, returning errno 2.
Traceback (most recent call last):
  File "/home/jack/SE370A2/fuse.py", line 731, in _wrapper
    return func(*args, **kwargs) or 0
  File "/home/jack/SE370A2/fuse.py", line 771, in getattr
    return self.fgetattr(path, buf, None)
  File "/home/jack/SE370A2/fuse.py", line 1024, in fgetattr
    attrs = self.operations('getattr', self._decode_optional_path(path), fh)
  File "/home/jack/SE370A2/fuse.py", line 1240, in __call__
    ret = getattr(self, op)(path, *args)
  File "/home/jack/SE370A2/passthrough.py", line 43, in getattr
    st = os.lstat(full_path)
FileNotFoundError: [Errno 2] No such file or directory: 'source/.gitignore'
DEBUG:fuse.log-mixin:-> getattr /newfile (None,)
DEBUG:fuse.log-mixin:<- getattr {'st_atime': 1601521307.29, 'st_ctime': 1601521307.29, 'st_gid': 1000, 'st_mode': 33188, 'st_mtime': 1601521307.29, 'st_nlink': 1, 'st_size': 0, 'st_uid': 1000}
```

Command:   
```
hello world
```

Output:
```
DEBUG:fuse.log-mixin:-> getxattr /newfile ('security.capability',)
DEBUG:fuse.log-mixin:<- getxattr '[Errno 95] Operation not supported'
DEBUG:fuse:FUSE operation getxattr raised a <class 'fuse.FuseOSError'>, returning errno 95.
Traceback (most recent call last):
  File "/home/jack/SE370A2/fuse.py", line 731, in _wrapper
    return func(*args, **kwargs) or 0
  File "/home/jack/SE370A2/fuse.py", line 906, in getxattr
    ret = self.operations('getxattr', path.decode(self.encoding),
  File "/home/jack/SE370A2/fuse.py", line 1240, in __call__
    ret = getattr(self, op)(path, *args)
  File "/home/jack/SE370A2/fuse.py", line 1124, in getxattr
    raise FuseOSError(ENOTSUP)
fuse.FuseOSError: [Errno 95] Operation not supported
DEBUG:fuse.log-mixin:-> write /newfile (b'hello word\n', 0, 4)
DEBUG:fuse.log-mixin:<- write 11

```

Command:   
```
^D (CTRL+D)
```

Output:
```
DEBUG:fuse.log-mixin:-> flush /newfile (4,)
DEBUG:fuse.log-mixin:<- flush None
DEBUG:fuse.log-mixin:-> release /newfile (4,)
DEBUG:fuse.log-mixin:<- release None
```
Notes:
* Changing directory to "mount" folder
  * Getting attributes of the mount folder (its a file in linux)

Command:   
```
cd ../
```

Output:   
```
DEBUG:fuse.log-mixin:-> getattr / (None,)
DEBUG:fuse.log-mixin:<- getattr {'st_atime': 1601521308.12, 'st_ctime': 1601521307.29, 'st_gid': 1000, 'st_mode': 16877, 'st_mtime': 1601521307.29, 'st_nlink': 2, 'st_size': 4096, 'st_uid': 1000}
```

Command:   
```
fusermount -u mount
```

Output:   
```
DEBUG:fuse.log-mixin:-> destroy / ()
DEBUG:fuse.log-mixin:<- destroy None
```






Contents of source and mount:   
```
jack@DESKTOP-Q6QKAUO:~/SE370A2$ ls -l mount
total 0
jack@DESKTOP-Q6QKAUO:~/SE370A2$ ls -l source
total 16
-rw-r--r-- 1 jack jack 11 Oct  1 16:02 newfile
-rw-r--r-- 1 jack jack  2 Oct  1 01:59 one
-rw-r--r-- 1 jack jack  2 Oct  1 01:59 three
-rw-r--r-- 1 jack jack  2 Oct  1 01:59 two
```
Note, newfile was saved to source containing "hello world" as mount was a passthrough

IN VSCODE files:   
mount
 - newfile
 - one (DELETED)
 - two (DELETED)
 - three (DELETED)   

source
 - one
 - two
 - three