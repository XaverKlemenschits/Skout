#!/bin/bash

#this generates an .ico file with the sizes 256, 128, 96, 64, 48, 32, 16
convert scaled_perspective.png -resize 256x256 -define icon:auto-resize="256,128,96,64,48,32,16" skout.ico
