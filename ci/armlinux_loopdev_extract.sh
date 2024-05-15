#!/bin/bash

# Check if the user provided an image file and output file
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <image_file> <output_file>"
    exit 1
fi

IMG_FILE=$1
OUTPUT_FILE=$2
PWD=$(pwd)
MNT_POINT="$PWD/mnt"

# Check if the file exists
if [ ! -f "$IMG_FILE" ]; then
    echo "File not found: $IMG_FILE"
    exit 1
fi

# Setup loop device and get partitions info
LOOP_DEVICE=$(sudo losetup -fP --show "$IMG_FILE")

if [ $? -ne 0 ]; then
    echo "Failed to setup loop device for $IMG_FILE"
    exit 1
fi

echo "Created loopback device ${LOOP_DEVICE}"

# Check the partition table
sudo parted -s "$LOOP_DEVICE" print

# Get partition information
PARTITION_INFO=$(sudo parted -s "$LOOP_DEVICE" unit s print | grep "^ [0-9]")

if [ $? -ne 0 ]; then
    echo "Failed to get partition information"
    sudo losetup -d "$LOOP_DEVICE"
    exit 1
fi

# Parse the second partition details
PARTITION_OFFSET=$(echo "$PARTITION_INFO" | awk 'NR==2 {print $2}' | sed 's/s//')
PARTITION_SIZE=$(echo "$PARTITION_INFO" | awk 'NR==2 {print $4}' | sed 's/s//')

# Create a loop device for the second partition
PARTITION_LOOP_DEVICE=$(sudo losetup -o $((PARTITION_OFFSET * 512)) --sizelimit $((PARTITION_SIZE * 512)) --show -f "$LOOP_DEVICE")

if [ $? -ne 0 ]; then
    echo "Failed to create loop device for partition"
    sudo losetup -d "$LOOP_DEVICE"
    exit 1
fi

# Create the mount point directory if it doesn't exist
mkdir -p $MNT_POINT

# Mount the partition
sudo mount "$PARTITION_LOOP_DEVICE" $MNT_POINT

if [ $? -ne 0 ]; then
    echo "Failed to mount partition"
    sudo losetup -d "$PARTITION_LOOP_DEVICE"
    sudo losetup -d "$LOOP_DEVICE"
    exit 1
fi

# Copy the binary file from the mounted partition to the output file
sudo cp $MNT_POINT/cg/*.elf $OUTPUT_FILE

if [ $? -ne 0 ]; then
    echo "Failed to copy the binary file"
    sudo umount $MNT_POINT
    sudo losetup -d "$PARTITION_LOOP_DEVICE"
    sudo losetup -d "$LOOP_DEVICE"
    exit 1
fi

echo "Binary file copied successfully to $OUTPUT_FILE"

# Cleanup function to unmount and detach loop devices
cleanup() {
    sudo umount $MNT_POINT
    sudo losetup -d "$PARTITION_LOOP_DEVICE"
    sudo losetup -d "$LOOP_DEVICE"
}

# Trap EXIT signal to ensure cleanup is done
trap cleanup EXIT
