from __future__ import division
from wand.image import Image
from wand.display import display
import sys, getopt, os

def main(argv):
    localfile = ''
    remotefile = ''
    try:
        opts, args = getopt.getopt(argv,"hl:r:",["lfile=","rfile="])
    except getopt.GetoptError:
        print 'set_background.py -l <localfile> -r <remotefile>'
    for opt, arg in opts:
        if opt in ("-l", "--lfile"):
            localfile = arg
            with Image(filename=localfile) as img:
                print(img.size)
                filename, extension = os.path.splitext(os.path.basename(localfile))
                for size in 460,720,980,1240,1500,1760,1920:
                    with img.clone() as i:
                        percentage = size/i.width
                        print(percentage)
                        i.resize(int(i.width * percentage), int(i.height * percentage))
                        i.save(filename='../website/static/{0}_{1}{2}'.format(filename,size,extension))
        elif opt in ("-r", "--rfile"):
            print("Not implemented")


if __name__ == "__main__":
   main(sys.argv[1:])
