File Test Operators
==============================================================================
.. contents::
    :local:
    :depth: 1

**Returns true if...**


Important Test
------------------------------------------------------------------------------
.. contents::
    :local:
    :depth: 1


``-e`` file exists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``-a`` file exists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is identical in effect to -e. It has been "deprecated," [1] and its use is discouraged.


``-f`` file is a regular file (not a directory or device file)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``-s`` file is not zero size
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``-d`` file is a directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``-r`` file has read permission (for the user running the test)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``-w`` file has write permission (for the user running the test)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``-x`` file has execute permission (for the user running the test)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``!``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"not" -- reverses the sense of the tests above (returns true if condition absent).


Less Important Test
------------------------------------------------------------------------------


``-b`` file is a block device
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``-c`` file is a character device
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    device0="/dev/sda2"    # /   (root directory)
    if [ -b "$device0" ]
    then
      echo "$device0 is a block device."
    fi
    # /dev/sda2 is a block device.

    device1="/dev/ttyS1"   # PCMCIA modem card.
    if [ -c "$device1" ]
    then
      echo "$device1 is a character device."
    fi

    # /dev/ttyS1 is a character device.


``-p`` file is a pipe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    function show_input_type()
    {
       [ -p /dev/fd/0 ] && echo PIPE || echo STDIN
    }

    show_input_type "Input"                           # STDIN
    echo "Input" | show_input_type                    # PIPE

    # This example courtesy of Carl Anderson.


``-h`` file is a symbolic link
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``-L`` file is a symbolic link
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``-S`` file is a socket
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``-t`` file (descriptor) is associated with a terminal device
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This test option may be used to check whether the stdin [ -t 0 ] or stdout [ -t 1 ] in a given script is a terminal.


``-g`` set-group-id (sgid) flag set on file or directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If a directory has the sgid flag set, then a file created within that directory belongs to the group that owns the directory, not necessarily to the group of the user who created the file. This may be useful for a directory shared by a workgroup.

``-u`` set-user-id (suid) flag set on file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A binary owned by root with set-user-id flag set runs with root privileges, even when an ordinary user invokes it. [2] This is useful for executables (such as pppd and cdrecord) that need to access system hardware. Lacking the suid flag, these binaries could not be invoked by a non-root user.

::

    -rwsr-xr-t    1 root       178236 Oct  2  2000 /usr/sbin/pppd

A file with the suid flag set shows an s in its permissions.


``-k`` ``sticky bit`` set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Commonly known as the sticky bit, the save-text-mode flag is a special type of file permission. If a file has this flag set, that file will be kept in cache memory, for quicker access. [3] If set on a directory, it restricts write permission. Setting the sticky bit adds a t to the permissions on the file or directory listing. This restricts altering or deleting specific files in that directory to the owner of those files.

::

    drwxrwxrwt    7 root         1024 May 19 21:26 tmp/

If a user does not own a directory that has the sticky bit set, but has write permission in that directory, she can only delete those files that she owns in it. This keeps users from inadvertently overwriting or deleting each other's files in a publicly accessible directory, such as /tmp. (The owner of the directory or root can, of course, delete or rename files there.)


``-O`` you are owner of file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``-G`` group-id of file same as yours
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``-N`` file modified since it was last read
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``f1 -nt f2`` file f1 is newer than f2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``f1 -ot f2`` file f1 is older than f2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


``f1 -ef f2`` files f1 and f2 are hard links to the same file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
