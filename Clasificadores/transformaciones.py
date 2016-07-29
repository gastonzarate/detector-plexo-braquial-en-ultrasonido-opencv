import os
import cv2
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import data, color, exposure

rutaOrigen = os.path.join("DatosNormalizados","train")
for base, dirs, files in os.walk(rutaOrigen):
    for name in files:
        #image = cv2.imread(os.path.join(rutaOrigen, name))

        image = color.rgb2gray(data.astronaut())

        fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16),
                            cells_per_block=(1, 1), visualise=True)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)

        ax1.axis('off')
        ax1.imshow(image, cmap=plt.cm.gray)
        ax1.set_title('Input image')
        ax1.set_adjustable('box-forced')

        # Rescale histogram for better display
        hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 0.02))

        ax2.axis('off')
        ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
        ax2.set_title('Histogram of Oriented Gradients')
        ax1.set_adjustable('box-forced')
        plt.show()
        cv2.waitKey(0)
