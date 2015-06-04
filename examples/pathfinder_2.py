import os

from PIL import Image, ImageSequence
import numpy as np
import matplotlib.pyplot as plt

import sibunlabs

im = Image.open(os.path.join(*["bin", "example-cells", "cell_real_1.png"])).convert("I")
imarr = np.array(im, dtype = np.float32)

pathfinder = sibunlabs.Pathfinder(im)
radpath = pathfinder.getRadialPath()
# Sort
radpath.view('f8,f8').sort(order=['f1'], axis=0)

plt.plot(radpath[:,1], radpath[:,0])
plt.ylabel("Length r")
plt.xlabel("Angle in °")
plt.show()