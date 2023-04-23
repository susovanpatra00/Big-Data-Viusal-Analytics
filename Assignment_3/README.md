## Here is what your interface should do:
* In the left side, your interface should show an interactive Isosurface visualization of the 3D dataset provided with this assignment. Plotly has an API 
  to draw Isosurfaces. [See Fig. 1]
* On the right side, your interface should plot a histogram visualization of the 3D dataset. Histogram should have labels and markers for axes as shown 
   in the figure. Plotly has an API to draw histograms. [See Fig. 1]
* Your interface should contain a slider that allows changing the isovalue for the Isosurface. This slider value range should be mapped to the entire 
   data range and by sliding to through different scalar values, the Isosurface plot should get updated automatically. You should also color your 
   Isosurface using a standard Python/Plotly colormap so that the color of your Isosurface changes as you change the isovalue. You can use Jupyter Widgets 
   to add the slider. [See Fig. 1]
*  At the beginning, you should show Isosurface of isovalue=0.0 and the histogram of the entire volume data set as seen in the Figure. [See Fig. 1]
*  When you change your slider, you will also update the histogram plot. Let’s say, you have selected the isovalue = x in from the slider by changing it. Then your histogram plot should contain data points with the following conditions: (x - 0.25) <= points with data values in histogram <= (x + 0.25). So, essentially, you will update the histogram plot with data values around (within +/- 0.25) your current selected isovalue from the slider. This will be histogram of a subset of the data and your histogram axes labels should get updated with the new data range. [See Fig. 2]
* Finally, you will add a button called ‘Reset’. When this button is clicked, the plot will get reset to its initial/beginning configuration, i.e., the slider value should be set back to 0.0, Isosurface plot should get updated with the isovalue = 0.0, the histogram plot should show the histogram of the entire data set and not of a subset. You can use Jupyter Widgets to add the button. [See Fig. 1 and 2]
* Your interface should be interactive, and users can change the slider value freely to see different isosurfaces and the corresponding histograms.
