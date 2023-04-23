## Importing all the necessary libraries
## -------------------------------------
import random
import vtk
import numpy as np
from scipy.interpolate import griddata
import time
from vtk.util import numpy_support as ns
## -------------------------------------

## Taking Sampling Percentage and Recons. Type from user
## -----------------------------------------------------
samp_val = int(input("Sampling Percentage: "))
recon_val = int(input("Reconstruction Type (1 for nearest, 2 for linear): "))
## -----------------------------------------------------


## SNR computation function
## -------------------------------------------------------
def compute_SNR(arrgt, arr_recon):
    diff = arrgt - arr_recon
    sqd_max_diff = (np.max(arrgt) - np.min(arrgt)) ** 2
    snr = 10 * np.log10(sqd_max_diff / np.mean(diff ** 2))
    return snr
## -------------------------------------------------------


## Random Sampling Function and storing the data into sampled_points.vtp
## ---------------------------------------------------------------------
def simple_random_sampling(input_data, sampling_percentage):
    
    # Fetching total umber of points in the input data
    # ------------------------------------------------
    num_points = input_data.GetNumberOfPoints()
    # ------------------------------------------------

    # Computing the number of points to sample based on the sampling percentage
    # -------------------------------------------------------------------------
    num_sampled_points = int(num_points * sampling_percentage / 100)
    # -------------------------------------------------------------------------

    # Create an empty set to hold the sampled points
    # ----------------------------------------------
    sampled_points = set()
    # ----------------------------------------------

    # Adding the eight corner points to the sampled set
    # -------------------------------------------------
    for i in range(8):
        point_id = i
        point = input_data.GetPoint(point_id)
        point_data = input_data.GetPointData().GetScalars().GetTuple(point_id)
        sampled_points.add((point[0], point[1], point[2], point_data[0]))
    # -------------------------------------------------


    # Sampling the remaining points randomly
    # --------------------------------------
    while len(sampled_points) < num_sampled_points:
        point_id = random.randint(0, num_points - 1)
        point = input_data.GetPoint(point_id)
        point_data = input_data.GetPointData().GetScalars().GetTuple(point_id)
        sampled_points.add((point[0], point[1], point[2], point_data[0]))
    # --------------------------------------


    # Creating a VTK polydata object to store the sampled points
    # ----------------------------------------------------------
    polydata = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    scalars = vtk.vtkFloatArray()
    scalars.SetNumberOfComponents(1)
    scalars.SetName("Data")
    # ----------------------------------------------------------


    # Adding the sampled points to the polydata object
    # ------------------------------------------------
    for point in sampled_points:
        points.InsertNextPoint(point[0], point[1], point[2])
        scalars.InsertNextValue(point[3])

    polydata.SetPoints(points)
    polydata.GetPointData().SetScalars(scalars)
    # ------------------------------------------------

    

    # Writing the sampled points to a VTKPolyData file named sampled_points.vtp
    # -------------------------------------------------------------------------
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName("sampled_points.vtp")
    writer.SetInputData(polydata)
    writer.Write()
    # -------------------------------------------------------------------------
    
    return polydata
## ---------------------------------------------------------------------



## Loading the Isabel_3D.vti file
## ------------------------------------------------------------------
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("Isabel_3D.vti")
reader.Update()
vtidata = reader.GetOutput()
## ------------------------------------------------------------------

## Converting Isabel_3D to numpy array
## ------------------------------------------------------------------
num_vtk = ns.vtk_to_numpy(vtidata.GetPointData().GetArray('Pressure'))
## ------------------------------------------------------------------

# Calling the Random Sampling Function with a sampling percentage given by user
## ----------------------------------------------------------------------------
sampled_points = simple_random_sampling(vtidata, samp_val)
## ----------------------------------------------------------------------------


## Taking values from sample points
## ---------------------------------------------
points = sampled_points.GetPoints()
data = sampled_points.GetPointData().GetScalars()
## ---------------------------------------------


## Extracting the x, y, and z coordinates of the points for use in reconstructing
## ------------------------------------------------------------------------------
num_points = points.GetNumberOfPoints()
x = np.empty(num_points)
y = np.empty(num_points)
z = np.empty(num_points)
for i in range(num_points):
    point = points.GetPoint(i)
    z[i] = point[0]
    y[i] = point[1]
    x[i] = point[2]

X, Y, Z = np.mgrid[min(x):max(x):50j,min(y):max(y):250j,min(z):max(z):250j]
## ------------------------------------------------------------------------------

## If condition for Reconstruction type (1 for nearest & 2 for linear)
## -------------------------------------------------------------------
if (recon_val == 1):

    # Placing the time variable
    # -------------------------
    start_time = time.time()
    # -------------------------


    # Reconstructing the volume data using nearest neighbor interpolation
    # ----------------------------------------------------------------------
    reconstructed_data = griddata((x, y, z), data, (X,Y,Z), method='nearest')
    # ----------------------------------------------------------------------
    

    # Converting the reconstructed data to a VTKImageData object
    # ----------------------------------------------------------
    image_data = vtk.vtkImageData()
    image_data.SetDimensions(reconstructed_data.shape)
    image_data.SetDimensions(250,250,50)
    vtk_data = vtk.vtkFloatArray()
    vtk_data.SetNumberOfComponents(1)
    vtk_data.SetName("Data")
    vtk_data.SetVoidArray(reconstructed_data.flatten(), reconstructed_data.size, 1)
    image_data.GetPointData().SetScalars(vtk_data)
    # ----------------------------------------------------------


    # Writing the reconstructed volume data to a VTI file
    # ---------------------------------------------------
    writer = vtk.vtkXMLImageDataWriter()
    writer.SetFileName("reconstructed_nearest_original.vti")
    writer.SetInputData(image_data)
    writer.Write()
    # ---------------------------------------------------


    # Converting nearest data to numpy and then Printing the SNR value
    # ---------------------------------------------------------------------
    num_image_data = ns.vtk_to_numpy(image_data.GetPointData().GetScalars())
    print("SNR value for nearest : ",compute_SNR(num_vtk,num_image_data))
    # ---------------------------------------------------------------------


    # Ending the time
    # ---------------
    end_time = time.time()
    # ---------------

    print(f"Elapsed time: {end_time - start_time} seconds")
elif(recon_val == 2):

    # Placing the time variable
    # -------------------------
    start_time = time.time()
    # -------------------------


    # Reconstructing the volume data using nearest neighbor interpolation
    # -------------------------------------------------------------------
    reconstructed_linear = griddata((x, y, z), data, (X,Y,Z), method='linear')
    # -------------------------------------------------------------------


    # Replacing nan values with nearest values
    # ----------------------------------------
    nan = np.isnan(reconstructed_linear)
    nearest = griddata((x, y, z), data, np.transpose(np.nonzero(nan)), method='nearest')
    reconstructed_linear[nan] = nearest
    # ----------------------------------------


    # Convert the reconstructed data to a VTKImageData object
    # -------------------------------------------------------
    image_linear = vtk.vtkImageData()
    image_linear.SetDimensions(reconstructed_linear.shape)
    image_linear.SetDimensions(250,250,50)
    image_linear.GetPointData().SetScalars(ns.numpy_to_vtk(reconstructed_linear.flatten(), deep= True))
    # -------------------------------------------------------


    # Writing the reconstructed volume data to a VTI file
    # ---------------------------------------------------
    writer = vtk.vtkXMLImageDataWriter()
    writer.SetFileName("reconstructed_linear_original.vti")
    writer.SetInputData(image_linear)
    writer.Write()
    # -------------------------------------------------------


    # Converting linear data to numpy and then Printing the SNR value
    # ----------------------------------------------------------------
    num_linear_data = ns.vtk_to_numpy(image_linear.GetPointData().GetScalars())
    print("SNR value for linear : ",compute_SNR(num_vtk,num_linear_data))
    # ----------------------------------------------------------------

    # Ending the time
    # ---------------
    end_time = time.time()
    # ---------------

    print(f"Elapsed time: {end_time - start_time} seconds")



