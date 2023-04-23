## 1. Data Query/Processing Task: 
### Print the following information about the dataset:
* Number of cells in the dataset
* The dimensions of the dataset
* The number of points present in the uniform grid of the data. (Think about the relationship between the total number of points and the data dimension)
* Print the range of Pressure values present in the dataset.
* Print the average Pressure value of the entire dataset, i.e., the Pressure array. For this, you will have to access the Pressure values and compute 
the average of all points.
* Extract a vtkCell object with cell id=0, i.e., the first cell. This is a quad cell, so the cell will have four vertices and four edges, and one face. 
Note that, the cell id in your program should be a parameter and if the user changes the cell id, then all the quantities that you are computing about the cell should get updated.
* Print the indices of the four corner vertices of the cell.
* Print the 3D coordinate of each vertex. Note that this is a 2D dataset, but all the points are stored as 3D points in the VTK data file with a constant Z-coordinate value=25.
* Compute the 3D coordinate of the cell center using its four corner vertices. The center location can be computed as the average of the corner vertices. Again, note that the Z coordinate of the center will be 25.
* Print the data/attribute value (Pressure) for all the four vertices of the extracted cell.
* Compute and print the mean (average) Pressure value at the cell center by averaging Pressure values from the four cell vertices.

## 2. Visualization Task:
Assuming you can access the information for the above task, you already know the coordinates of the four corner vertices of the cell that you have 
extracted with cell id=0. The coordinates are 3D points with a constant Z coordinate value=25. Now create a new VtkPolyData object, add these 4 points 
into the VtkPolyData and specify a separate color for each point. For example, you can represent the red color as (255,0,0) as an RGB 3-value tuple. For help assign a color to the points, you can consult the ColoredTriangle example [1] as a reference. Next, use vtkVertexGlyphFilter() to create visual representations for each point in the form of a Vertex Glyph. Finally, use VTK mapper, actor, and renderer to show the output of the vtkVertexGlyphFilter() as points in the screen. If you are doing it right, your output should look like the following image. Note that you may have different colors for vertices depending on what color you have assigned to them in your code.
