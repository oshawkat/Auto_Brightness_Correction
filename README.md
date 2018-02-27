# Automatic Brightness Correction

The goal of this project is to minimize the impact of excessively bright/dark areas of a photo (eg sun, street lamps, direct backlighting) and provide greater detail and range in the rest of the image.  As currently structured, the module provides a range of functions to enable exploration of image histograms and applying corrections.

For a detailed overview of development, capabilities, and results, please look at the included [Project Overview](Project-Overview.pdf)

Note that the current implementation of the module does require some hyperparameter setting by the user, as shown in the example script.  Please refer to [Project Overview](Project-Overview.pdf) for intended future extension and fully-automated brightness correction.

### Prerequisites

This module has been tested on Python 2.7 and requires Numpy, OpenCV2, and Matplotlib.  You can use PiP to install all required libraries:

```
pip install numpy matplotlib opencv-python==2.4.9
```
or view alternative installation instructions on the [Numpy](https://www.scipy.org/scipylib/download.html), [OpenCV](https://opencv.org/), and [Matplotlib](https://matplotlib.org/users/installing.html) sites.


### Use

The included *main.py* provides an example demonstration of the module functionality by applying automatic brightness correction to all the images found in the */input* directory and saving these new images, as well as histograms for both the uncorrected and corrected images, in the */output* directory.  The script can be run as follows:

```
python example.py
```

## Authors

* **Osman Shawkat** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* README template courtesy of Bille Thompson - [PurpleBooth](https://github.com/PurpleBooth)

