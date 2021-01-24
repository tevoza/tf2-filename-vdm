#!/bin/bash

movieCount=$(ls -l movie* | wc -l)
echo "$movieCount"

while [ $movieCount -gt 0 ]; do
	vid=$(ls -l vid* | wc -l)
	((vid++))
	mov=$(ls movie* | head -n 1)
	movie=${mov%_*}
	echo "generating clip $vid from $movie"
	ffmpeg -r 60 -f image2 -s 1920x1080 -i ./${movie}_%04d.tga -vcodec libx264 -crf 15 -pix_fmt yuv420p vid$vid.mp4
	rm ${movie}*
	movieCount=$(ls -l movie* | wc -l) &&
echo "$movieCount"
done
