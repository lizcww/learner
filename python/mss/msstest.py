import os
import os.path
import time
import cv2
import mss
import numpy
from PIL import Image


def on_exists(fname):
    # type: (str) -> None
    """
    Callback example when we try to overwrite an existing screenshot.
    """

    if os.path.isfile(fname):
        oldfile = fname + "." + str(time.time())
        print("{0} -> {1}".format(fname, oldfile))
        os.rename(fname, oldfile)

def take_screenshot():
    with mss.mss() as sct:
        filename = sct.shot(output="mon-{mon}.png", callback=on_exists)
        print(filename)

def take_screenshot02():
    time.sleep(5)
    with mss.mss() as sct:
        # Get rid of the first, as it represents the "All in One" monitor:
        for num, monitor in enumerate(sct.monitors[1:], 1):
            # Get raw pixels from the screen
            sct_img = sct.grab(monitor)

            # Create the Image
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

            # The same, but less efficient:
            # img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)

            img.thumbnail([img.width/2, img.height/2])
            img = img.convert('L')

            # And save it!
            output = "monitor-{0}.png".format(num)
            img.save(output)
            print(output)

            array = numpy.array(img)
            print(array[209][200:205])

            

def play_with_pixel():
    with mss.mss() as sct:
        # Get a screenshot of the 1st monitor
        sct_img = sct.grab(sct.monitors[1])

        # Create an Image
        img = Image.new("RGB", sct_img.size)

        # Best solution: create a list(tuple(R, G, B), ...) for putdata()
        pixels = zip(sct_img.raw[2::4], sct_img.raw[1::4], sct_img.raw[0::4])
        img.putdata(list(pixels))

        # But you can set individual pixels too (slower)
        """
        pixels = img.load()
        for x in range(sct_img.width):
            for y in range(sct_img.height):
                pixels[x, y] = sct_img.pixel(x, y)
        """

        # Show it!
        img.show()

def show_video():
    with mss.mss() as sct:
        # Part of the screen to capture
        monitor = {"top": 40, "left": 0, "width": 800, "height": 640}

        while "Screen capturing":
            last_time = time.time()

            # Get raw pixels from the screen, save it to a Numpy array
            img = numpy.array(sct.grab(monitor))

            # Display the picture
            cv2.imshow("OpenCV/Numpy normal", img)

            # Display the picture in grayscale
            # cv2.imshow('OpenCV/Numpy grayscale',
            #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

            print("fps: {0}".format(1 / (time.time() - last_time)))

            # Press "q" to quit
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
class screen_analyzer:
    def get_screen(self):
        with mss.mss() as sct:
            # Get raw pixels from the screen, save it to a Numpy array
            self.img = numpy.array(sct.grab(sct.monitors[1]))
    def show_array(self):
        print(self.img[1][2][3])
        new_numpy = self.img.sum(axis=2)
        print(new_numpy.shape)

#sa = screen_analyzer()
#sa.get_screen()
#sa.show_array()

take_screenshot02()





