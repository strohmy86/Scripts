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
    sudo fdisk -l
    echo ''
    echo ''
    echo ${bold}'Which volume is the encrypted one? (ex: /dev/sdb1)'${normal}
    read enc

    ## Decrypt and mount encrypted volume to /media/encrypted
    sudo mkdir -p /mnt/tmp
    sudo dislocker -v -V ${enc} -u -- /mnt/tmp
    if [ -d "/media/encrypted" ]; then
      sudo mount -o loop,rw /mnt/tmp/dislocker-file /media/encrypted/
    else
      sudo mkdir -p /media/encrypted
      sudo mount -o loop,rw /mnt/tmp/dislocker-file /media/encrypted/
    fi
  else
    echo ${bold}'Dislocker is not installed. '${normal}'Please install dislocker and try again.'
    exit 1
  fi
}

function unmount_disk {
  sudo umount /mnt/tmp/dislocker-file
  sudo umount dislocker
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
