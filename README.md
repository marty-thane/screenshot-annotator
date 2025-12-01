# Screenshot Annotator

A simple graphical tool built with Python and Tkinter to quickly annotate screenshots. You can draw rectangles and automatically add numbered labels to highlight areas of an image.

## Features

-   Load various image formats (PNG, JPEG, etc.).
-   Draw rectangles to highlight areas of interest.
-   Optionally, automatically add numbered labels next to each rectangle.
-   Save the annotated image to a new file or save over the original file.
-   Annotation thickness and font size scale automatically based on the image size, but can also be controlled manually.

## Dependencies

The only dependency is the Pillow library for image manipulation.

## Installation

1.  Ensure you have Python 3 and `tkinter` installed. On some Linux distributions, you may need to install it separately (e.g., `sudo apt-get install python3-tk`).

2.  Clone the repository or download the source code.

3.  Install the required Python package:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

You can run the application from the command line.

**Basic Usage:**

To open the application and then select a file via the "Open" dialog:
```bash
python3 main.py
```

To open a specific image file directly:
```bash
python3 main.py /path/to/your/image.png
```

### How to Annotate

1.  If you didn't provide a file at the command line, click the **Open** button to load an image.
2.  Click and drag the mouse on the image to draw a rectangle.
3.  The rectangle and an optional number will be drawn when you release the mouse button.
4.  Click the **Save** button to save the annotated image.

### Command-Line Arguments

-   `file`: (Optional) The path to the image file to open.
-   `--inplace`: If specified, saving will overwrite the original file. Use with caution.
-   `--numbers`: If specified, each rectangle you draw will be automatically labeled with an incrementing number.
-   `--scale <FLOAT>`: A manual scaling factor for the thickness of the rectangle lines and the font size. This overrides the automatic scaling.

**Example with options:**

This will open `my_screenshot.png`, allow you to add numbered labels, and will save changes directly back to `my_screenshot.png`.

```bash
python3 main.py --numbers --inplace my_screenshot.png
```
