#!/bin/sh
user=$(whoami)
export PATH="$PATH:/opt/local/bin:/usr/local/bin:/Users/$user/bin"
exec /Applications/Cantata.app/Contents/MacOS/cantata
