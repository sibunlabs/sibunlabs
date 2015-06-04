import os

from PIL import Image, ImageSequence
import numpy as np
import matplotlib.pyplot as plt

import sibunlabs

im = Image.open(os.path.join(*["bin", "example-cells", "cell_real_1.png"])).convert("I")
imarr = np.array(im, dtype = np.float32)

pathfinder = sibunlabs.Pathfinder(im)
path = pathfinder.getPath(centered = False).tolist()

for point in path:
    imarr[point[1],point[0]] = 0


plt.imshow(imarr, interpolation = "nearest")
plt.show()