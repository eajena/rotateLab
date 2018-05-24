#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, os, getopt, glob
import numpy as np
import matplotlib.pyplot as plt

from skimage import io
from skimage.color import rgb2lab, lab2rgb


def do_rot(lab, theta):
    h,w,c = lab.shape
    assert c==3
    result = np.zeros_like(lab)
    theta_r = np.radians(theta)
    c, s = np.cos(theta_r), np.sin(theta_r)
    R = np.asarray([[c,-s],[s,c]])
    f = np.hstack( (lab[:,:,1].reshape(-1,1),
                    lab[:,:,2].reshape(-1,1)))
    m = np.mean(f,axis=0)
    if option["mean"]:
        f-=m
    r = np.dot(f, R)
    result[:,:,0] = lab[:,:,0]
    result[:,:,1] = r[:,0].reshape(h,w)
    result[:,:,2] = r[:,1].reshape(h,w)
    if option["verbose"]:
        plt.scatter(lab[:,:,1],lab[:,:,2], color="blue")
        plt.scatter(result[:,:,1],result[:,:,2], color="green")
        plt.scatter(result[:,:,1],result[:,:,2], color="green")
        plt.plot(0, 0, 'ro')
        plt.axes().set_aspect('equal')
        plt.show()
    return result


def all_files(in_dir, out_dir, rotate):
    files = glob.glob('%s/*' % in_dir)
    for f in files:
        img = io.imread(f)
        if img.shape[2]==4:
            img = img[:,:,:3]
        lab = rgb2lab(img)

        if rotate is None:
            #mask = np.logical_and(25.<lab[:,:,0], lab[:,:,0]<75.)
            #plt.figure(1),plt.imshow(lab[:,:,0]), plt.colorbar()
            #plt.figure(2),plt.imshow(mask)
            #plt.show()
            #m = np.std(lab[:,:,1][mask]) * np.std(lab[:,:,2][mask])
            m = np.std(lab[:,:,1]) * np.std(lab[:,:,2])
            print m, f
            io.imsave("%s/%.4f-%s" % (out_dir, m, os.path.basename(f)), img)
        else:
            r = lab2rgb(do_rot(lab, rotate))
            if f[-4:]==".tif" or f[-5:]==".tiff":
                f+=".jpg"
            io.imsave("%s/%s" % (out_dir, os.path.basename(f)), r)


def read_options():
  try:
    opts, args = getopt.getopt(sys.argv[1:], 'ar:i:o:vm',
                        ["analyse","rotate=","in=","out="])
  except getopt.GetoptError as err:
    leave(str(err))

  for o, a in opts:
    if   o in ('-a',"--analyze"): option["rotate"] = None
    elif o in ("-r","--rotate"):  option["rotate"] = float(a)
    elif o in ("-i","--in"):      option["in"] = a
    elif o in ('-o',"--out"):     option["out"] = a
    elif o in ('-m',"--mean"):    option["mean"] = True
    elif o in ('-v',"--verbose"): option["verbose"] = True
    else: assert False, "unhandled option: %s" % str(o)

  assert os.path.isdir(option["in"]), "No such directory: %s" % option["in"]
  assert os.path.isdir(option["out"]), "No such directory: %s" % option["out"]


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')

    option = {
        "verbose" : False,
        "mean"    : False,
        "rotate"  : None,
        "in"      : "in",
        "out"     : "out"
    }
    read_options()

    all_files(option["in"], option["out"], option["rotate"])

    #plt.imshow(lab2rgb(r))
    #plt.show()
