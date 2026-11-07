#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
mkdir -p media
ffmpeg -nostdin -y -f lavfi -i 'testsrc2=size=1280x720:rate=30' \
  -f lavfi -i 'sine=frequency=440:sample_rate=48000' -t 12 \
  -c:v libx264 -profile:v main -level 3.1 -pix_fmt yuv420p \
  -c:a aac -b:a 96k -movflags +faststart media/diagnostic.mp4
