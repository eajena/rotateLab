# rotateLab.py - rotate images in Lab color space

This script will rotate the colors of an image in Lab around the center. It also supports centering the mean color on (0,0) first.

Usage:

    -r:  --rotate=deg           rotate by deg degreed
    -i:  --in=in_dir            path to images to be rotated
    -o:  --out=out_dir          write out images to
    -p:  --plots=plot_dir       write plots to
    -m   --mean                 do mean correction before rotation

Example:

    for i (60 120 180 240 300) { mkdir -p rot$i plots$i && python rotateLab.py -r $i -i cropped -o rot$i -p plots$i }
