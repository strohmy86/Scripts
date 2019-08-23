#!/bin/bash

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

bold=$(tput bold)
normal=$(tput sgr0)

function show_help {
  echo 'Options:'
  echo ''
  echo '-m  Option to mount the bitlocker-encrypted drive.'
  echo ''
  echo '-u  Option to unmount the bitlocker encrypted drive.'
}

function mount_disk {
  ## Check to see if dislocer is installed
  if command -v dislocker 2>/dev/null; then
    ## Discover the encrypted volume
    sudo diskutil list
    echo ''
    echo ''
    echo ${bold}'Which volume is the encrypted one? (ex: /dev/sdb1)'${normal}
    read enc

    ## Decrypt and mount encrypted volume to /media/encrypted
    sudo mkdir -p /private/tmp/dislocker
    sudo dislocker -v -V ${enc} -u -- /private/tmp/dislocker
    sudo hdiutil attach -imagekey diskimage-class=CRawDiskImage -nomount /private/tmp/dislocker/dislocker-file
    diskutil mount /dev/disk3
  else
    echo ${bold}'Dislocker is not installed. '${normal}'Please install dislocker and try again.'
    exit 1
  fi
}

function unmount_disk {
  diskutil eject /dev/disk3
  sleep 2
  sudo umount dislocker-fuse@osxfuse0
}

while getopts "h?mu" opt; do
  case "$opt" in
    h|\?)
        show_help
        exit 0
        ;;
    m)  mount_disk
        ;;
    u)  unmount_disk
        ;;
  esac
done

shift $((OPTIND-1))
[ "${1:-}" = "--" ] && shift