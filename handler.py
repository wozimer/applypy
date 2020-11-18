from cv2 import cvtColor, COLOR_BGR2GRAY, GaussianBlur
from skimage.metrics import mean_squared_error


class BaseHandler:
    """Base class for media handlers"""

    def __init__(self, obj):
        self._obj = obj


class ImageHandler(BaseHandler):

    @property
    def mode(self):
        return ImageMode(self._obj)

    @property
    def metrics(self):
        return ImageMetrics(self._obj)

    @property
    def filter(self):
        return ImageFilter(self._obj)


class ImageBlur(BaseHandler):

    def gaussian(self, kernel_size, sigma_x, *args, region: tuple = None):
        """
        Smooths a rectangle area of the image using Gaussian  blur.
        :param sigma_x: Gaussian kernel standard deviation in X direction.
        :param kernel_size: Gaussian kernel size. ksize.width and ksize.height can differ but they both must be
        positive and odd. Or, they can be zero's and then they are computed from sigma.
        :param region: a tuple of top left and bottom right points of the smoothing area.
        The whole image will smoothed if not provided.
        :return: smoothed image.
        """

        if not region:
            top_left, bottom_right = (0, 0), (self._obj.width, self._obj.height)
        else:
            top_left, bottom_right = region

        smooth_area = self._obj.array[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        smoothed = GaussianBlur(smooth_area, kernel_size, sigma_x, *args)
        self._obj.array[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = smoothed

        return self._obj


class ImageFilter(BaseHandler):

    @property
    def blur(self):
        return ImageBlur(self._obj)


class ImageMode(BaseHandler):
    """ Implements color mode conversions."""

    def to_greyscale(self):
        """Convert to grey scale"""
        self._obj.array = cvtColor(self._obj.array, COLOR_BGR2GRAY)
        return self._obj


class ImageMetrics(BaseHandler):

    def mse(self, image) -> float:

        """
        Compute the mean-squared error between two images.
        :param image: Image to compare, must have same shape.
        :return: the mean-squared error (MSE) metric.
        """
        img1 = self._obj.mode.to_greyscale()
        img2 = image.mode.to_greyscale()

        return mean_squared_error(img1.array, img2.array)