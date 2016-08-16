#!/bin/bash

echo "======= rsyncing Metafor repo..."
rsync -e ssh -avz boman@blueberry:/home/metafor/SVN/ /hdd2/boman/Backups/rsync/SVN/
echo "======= done."

