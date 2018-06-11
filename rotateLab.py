#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, os, getopt, glob
import numpy as np
import matplotlib.pyplot as plt

from skimage import io
from skimage.color import rgb2lab, lab2rgb


def do_rot(lab, theta, filename):
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
    if option["plots"]:
        plt.figure("scatter")
        plt.scatter(lab[:,:,1],lab[:,:,2], color="blue", alpha=0.01)
        plt.scatter(result[:,:,1],result[:,:,2], color="green", alpha=0.01)
        plt.plot(0,0, 'wo')
        plt.plot(m[0], m[1], 'yo')
        mr = np.mean(r,axis=0)
        plt.plot(mr[0], mr[1], 'ro')
        plt.xlim([-100,100])
        plt.ylim([-100,100])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.savefig(os.path.join(option["plots"], "plot-%s.jpg" % os.path.basename(filename)));
        plt.close()
        plt.figure("histogram")
        hist, xe, ye = np.histogram2d(lab[:,:,1].flatten(), lab[:,:,2].flatten(), bins=(50,50))
        plt.imshow(hist.T, interpolation='none', origin='low', aspect='equal',
                   extent=[xe[0], xe[-1], ye[0], ye[-1]])
        plt.colorbar()
        plt.savefig(os.path.join(option["plots"], "hist-%s.jpg" % os.path.basename(filename)));
        plt.close()
    return result


def all_files(in_dir, out_dir, rotate):
    files = glob.glob('%s/*' % in_dir)
    for f in files:
        print f
        img = io.imread(f)
        if img.shape[2]==4:
            img = img[:,:,:3]
        lab = rgb2lab(img)

        r = lab2rgb(do_rot(lab, rotate, f))
        io.imsave(os.path.join(out_dir, "%s.jpg" % os.path.basename(f)), r)

def read_options():
  try:
    opts, args = getopt.getopt(sys.argv[1:], 'r:i:o:mp:',
                        ["rotate=","in=","out=","plots="])
  except getopt.GetoptError as err:
    print "Error:", err
    exit(1)

  for o, a in opts:
    if   o in ('-a',"--analyze"): option["rotate"] = None
    elif o in ("-r","--rotate"):  option["rotate"] = float(a)
    elif o in ("-i","--in"):      option["in"] = a
    elif o in ('-o',"--out"):     option["out"] = a
    elif o in ('-m',"--mean"):    option["mean"] = True
    elif o in ('-p',"--plots"):   option["plots"] = a
    else: assert False, "unhandled option: %s" % str(o)

  assert os.path.isdir(option["in"]), "No such dir: %s" % option["in"]
  assert os.path.isdir(option["out"]), "No such dir: %s" % option["out"]
  assert (not option["plots"] or
         os.path.isdir(option["out"])), "No such dir: %s" % option["plots"]


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')
    option = {
        "mean"    : False,
        "rotate"  : None,
        "plots"   : None,
        "in"      : "in",
        "out"     : "out"
    }
    read_options()
    all_files(option["in"], option["out"], option["rotate"])
