import sys
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage.color import rgb2gray, rgb2lab, lab2rgb
from skimage.util import img_as_uint


def do_rot(lab, theta):
    h,w,c = lab.shape
    assert c==3
    result = np.zeros_like(lab)
    theta_r = np.radians(theta)
    c, s = np.cos(theta_r), np.sin(theta_r)
    R = np.asarray([[c,-s],[s,c]])
    f = np.hstack( (lab[:,:,1].reshape(-1,1),
                    lab[:,:,2].reshape(-1,1)))


    r = np.dot(f, R)
    result[:,:,0] = lab[:,:,0]
    result[:,:,1] = r[:,0].reshape(h,w)
    result[:,:,2] = r[:,1].reshape(h,w)
    if False:
        plt.scatter(lab[:,:,1],lab[:,:,2], color="blue")
        plt.scatter(result[:,:,1],result[:,:,2], color="green")
        plt.axes().set_aspect('equal')
        plt.show()
    return result



if __name__ == "__main__":
    if len(sys.argv)==4:
        img = io.imread(sys.argv[1])
        lab = rgb2lab(img)
        r = do_rot(lab, float(sys.argv[3]))
        io.imsave(sys.argv[2], lab2rgb(r))
        #plt.imshow(lab2rgb(r))
        #plt.show()

    if False:
        img = io.imread(sys.argv[1])
        plt.imshow(img)
        lab = rgb2lab(img)

        r1 = do_rot(lab, -180)
        r2 = do_rot(r1,  90)
        r3 = do_rot(r2,  90)
        restored = lab2rgb(lab)

        plt.subplot(221),plt.imshow(lab2rgb(lab))
        plt.subplot(222),plt.imshow(lab2rgb(r1))
        plt.subplot(223),plt.imshow(lab2rgb(r2))
        plt.subplot(224),plt.imshow(lab2rgb(r3))
        plt.show()
