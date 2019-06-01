# PyQt5 examples

### stacklayout.py
This code uses stacked layout feature to stack QLabel(which holds QPixmap) and QWidget(over which bounding boxes are drawn using QPainter). Also, allows you to draw rectangles on the image with mouse click and drag.

### window4.py
An extension of *stacklayout.py* to include more features. 
- Highlight/delete the selected table row and corresponding bounding box on the image.
- Draws bounding box around each word, on the input image. 
- Edit the table row
- Save the table

*Input files:* CSV and JPG image, both with the same filename

*CSV content format:* (x,y) of top left, (x,y) of top right, (x,y) of bottom right, (x,y) of bottom left, word
