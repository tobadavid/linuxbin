
function private_mount
{
    encfs /hdd2/boman/Dropbox/Private/ /hdd2/boman/Private/
}

function private_umount
{
    fusermount -u /hdd2/boman/Private/
}

