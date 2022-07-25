# langmuir-experiment-analysis-program

## Dependencies:

Custom tkinter: https://github.com/TomSchimansky/CustomTkinter  
Matplotlib: https://matplotlib.org/stable/users/installing/index.html  
Scipy: https://scipy.org/install/  

For data recording only:  
PyVisa: https://pypi.org/project/PyVISA/  
Tqdm: https://tqdm.github.io/  

## Guide

### Adding, deleting, and saving files

Located at the lower left hand corner of the application, the explorer button is used to open the file explorer and select a file to analyze. An optional sys.argv parameter specifies the starting directory of the file explorer.

Near the middle of the application is the file selector section. Without adding files the only entry is the "Select All:" checkbox. After adding a file using the explorer, a new widget containing the file and its own checkbox appears. This is how files are selected for the manipulations that will be discussed later on.

The rightmost section controls the files. The top half controls general graph settings which the lower half contains operations on the files.

The first button in the graph settings section is the delete button, which deletes every file selected by the file selector.

The save button is the first button in the operations section, and saves to the current directory.


### Changing General Settings

The next button in the graph settings section is the lin/log button, which toggles the y-axis scale between linear and logarithmic.

The legend button toggles the graph legend on and off.

The Rescale button is still a work in progress.


### Cursors

The last two controls in the general settings section control the cursor positions. These are two cursors that move across the x-axis and are used to set bounds or other inputs into the math functions. Cursor1 is controlled by the upper controls while Cursor2 by the lower. The rightmost checkboxes control the visibility of the cursors, not affecting the functionality of the math functions.


### Doing math on the data

"f'" button:

Takes the derivative of the selected files, file by file.

"box average" button:

Takes the box average of the selectef files, file by file.
Box average means every datapoint becomes the average of itself and its two neighbors.

"average" button:
 
Takes the average of the files selected by the file selector.

"floating potential" button:

Finds the floating potential of the selected file by using a linear fit through the two values in the dataset that are closest to 0.

"basic isat" button:

This fits a linear fit through the selected datafile between the two cursors, and takes this as isat. Then subtracts this value from the original data to give the electron current.

"savgol filter" button:

This employs the savgol filter for smoothing the selected data.

"EEDF" button:

This finds the electron energy distribution function of the data. Plasma potential must be provided in the command line. (NOT WORKING YET).

"|f|" button:

This simply takes the absolute value of the selected files, file by file.

"temp" button:

Fits a line between the cursors, and gives error bounds. For correct electron temp data must already be only the electron current and the natural logartihm must be taken.

"ln" button:

Takes the natural logarithm of every y value in the dataset.


## Example: Finding electron temperature

First, the desired file is chosen and uploaded to the program:

![alt text](https://github.com/Theallpro1/langmuir-experiment-analysis-program/blob/main/ExampleImages/first_step.png)

The two cursors are now turned on, and moved to the beginning and the end of the ion saturation region:

![alt text](https://github.com/Theallpro1/langmuir-experiment-analysis-program/blob/main/ExampleImages/second_step.png)

The sample is now selected in the file selector, and the "basic isat" button is pressed, making the extrapolated ion current and the calculated electron current appear:

![alt text](https://github.com/Theallpro1/langmuir-experiment-analysis-program/blob/main/ExampleImages/third_step.png)

The cursors are now turned off and the original file along with the extrapolated current are deleted to reduce cluttering:

![alt text](https://github.com/Theallpro1/langmuir-experiment-analysis-program/blob/main/ExampleImages/fourth_step.png)

The electron current is selected, and then the "ln" button is pressed, making the red graph on the image below appear. The original graph is compressed due to scaling, and is the green "line" at the top of the graph. Then the cursors are turned on again, and moved to the electron temperature fit region:

![alt text](https://github.com/Theallpro1/langmuir-experiment-analysis-program/blob/main/ExampleImages/fifth_step.png)

The "temp" button is now pressed, displaying the calculated temperature along with error bounds:

![alt text](https://github.com/Theallpro1/langmuir-experiment-analysis-program/blob/main/ExampleImages/sixth_step.png)
