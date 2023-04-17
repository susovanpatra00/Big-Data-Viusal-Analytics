import vtk as vtk


## Load Data
## -----------------------------------------------
reader = vtk.vtkXMLImageDataReader()              # 'reader' is a object of vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_2D.vti')          #  Using 'reader' we will read the '*.vti' file from given location.
reader.Update()                                   #  Updating the 'reader' so that we always get the updated file.
vtidata = reader.GetOutput()                      #  We are initializing the output of the .vti file into a variable 
                                                  #     named 'vtidata'
## -----------------------------------------------


## Number Of cells to use it for iterating all the cells
## -----------------------------------------------------
numCells = vtidata.GetNumberOfCells()       # We will use the function 'GetNumberOfcells()' of vtk Library to 
                                            #    count the total number of cells in the .vti data.
## -----------------------------------------------------

## Finding Range in which we can have the isovalue
## ------------------------------------------------------------
range_ = vtidata.GetPointData().GetArray('Pressure').GetRange()    
## ------------------------------------------------------------


## Taking isovalue from User 
## --------------------------------------
iso = float(input("Enter the iso value: "))
## --------------------------------------


## Creating vtkPoints object
## -----------------------------------------
points = vtk.vtkPoints()                    # Creating an object of vtkPoints as 'points'
pol_data = vtk.vtkPolyData()                # Creating an object of vtkPolyData as 'pol_data'
contour_lines = vtk.vtkCellArray()          # Creating an global object of vtkCellAray as 'contour_lines' to insert
                                            #    each contour segments
## -----------------------------------------


## Iterating through all the cells and finding the points where given isovalue from user is matching
## -------------------------------------------------------------------------------------------------
for i in range (0, numCells):

    cell = vtidata.GetCell(i)         
    ##############################       All the point IDs
    pid1 = cell.GetPointId(0)    #    
    pid2 = cell.GetPointId(1)    #     
    pid3 = cell.GetPointId(3)    #
    pid4 = cell.GetPointId(2)    #
    ############################## 

    #####################################################################    All the Point Values
    val1 = vtidata.GetPointData().GetArray('Pressure').GetTuple1(pid1)  #   
    val2 = vtidata.GetPointData().GetArray('Pressure').GetTuple1(pid2)  #   
    val3 = vtidata.GetPointData().GetArray('Pressure').GetTuple1(pid3)  #   
    val4 = vtidata.GetPointData().GetArray('Pressure').GetTuple1(pid4)  #
    #####################################################################

    ## Now I will check all the 16 conditions for each cell and perform respective action according to that for finding the contour

    if (val1 > iso and val2 > iso and val3 > iso and val4 > iso): ## Case 1 : All the 4 points have higher value than given isovalue
        continue
    elif (val1 < iso and val2 < iso and val3 < iso and val4 < iso): ## Case 2 : All the 4 points have lesser value than given isovalue
        continue
    else:
        ## When only one point has greater value than given isovalue till the 6th block (Case 3, 4, 5, 6)

        if (val1 > iso and val2 < iso and val3 < iso and val4 < iso): # Case 3 : Only pid1 has greater value than given isovalue, all others have isovalue less than given isovalue
            
            x_1_2 = (val1 - iso)/(val1 - val2) * (vtidata.GetPoint(pid2)[0] - vtidata.GetPoint(pid1)[0]) + vtidata.GetPoint(pid1)[0]
            y_1_2 = (val1 - iso)/(val1 - val2) * (vtidata.GetPoint(pid2)[1] - vtidata.GetPoint(pid1)[1]) + vtidata.GetPoint(pid1)[1]
            x_y_1_2 = [x_1_2,y_1_2,25]
            points.InsertNextPoint(x_y_1_2)

            x_1_4 = (val1 - iso)/(val1 - val4) * (vtidata.GetPoint(pid4)[0] - vtidata.GetPoint(pid1)[0]) + vtidata.GetPoint(pid1)[0]
            y_1_4 = (val1 - iso)/(val1 - val4) * (vtidata.GetPoint(pid4)[1] - vtidata.GetPoint(pid1)[1]) + vtidata.GetPoint(pid1)[1]
            x_y_1_4 = [x_1_4,y_1_4,25]
            points.InsertNextPoint(x_y_1_4)


        elif (val1 < iso and val2 > iso and val3 < iso and val4 < iso): # Case 4 : Only pid2 has greater value than given isovalue, all others have isovalue less than given isovalue

            x_2_1 = (val2 - iso)/(val2 - val1) * (vtidata.GetPoint(pid1)[0] - vtidata.GetPoint(pid2)[0]) + vtidata.GetPoint(pid2)[0]
            y_2_1 = (val2 - iso)/(val2 - val1) * (vtidata.GetPoint(pid1)[1] - vtidata.GetPoint(pid2)[1]) + vtidata.GetPoint(pid2)[1]
            x_y_2_1 = [x_2_1,y_2_1,25]
            points.InsertNextPoint(x_y_2_1)

            x_2_3 = (val2 - iso)/(val2 - val3) * (vtidata.GetPoint(pid3)[0] - vtidata.GetPoint(pid2)[0]) + vtidata.GetPoint(pid2)[0]
            y_2_3 = (val2 - iso)/(val2 - val3) * (vtidata.GetPoint(pid3)[1] - vtidata.GetPoint(pid2)[1]) + vtidata.GetPoint(pid2)[1]
            x_y_2_3 = [x_2_3,y_2_3,25]
            points.InsertNextPoint(x_y_2_3)


        elif (val1 < iso and val2 < iso and val3 > iso and val4 < iso): # Case 5 : Only pid3 has greater value than given isovalue, all others have isovalue less than given isovalue

            x_3_2 = (val3 - iso)/(val3 - val2) * (vtidata.GetPoint(pid2)[0] - vtidata.GetPoint(pid3)[0]) + vtidata.GetPoint(pid3)[0]
            y_3_2 = (val3 - iso)/(val3 - val2) * (vtidata.GetPoint(pid2)[1] - vtidata.GetPoint(pid3)[1]) + vtidata.GetPoint(pid3)[1]
            x_y_3_2 = [x_3_2,y_3_2,25]
            points.InsertNextPoint(x_y_3_2)

            x_3_4 = (val3 - iso)/(val3 - val4) * (vtidata.GetPoint(pid4)[0] - vtidata.GetPoint(pid3)[0]) + vtidata.GetPoint(pid3)[0]
            y_3_4 = (val3 - iso)/(val3 - val4) * (vtidata.GetPoint(pid4)[1] - vtidata.GetPoint(pid3)[1]) + vtidata.GetPoint(pid3)[1]
            x_y_3_4 = [x_3_4,y_3_4,25]
            points.InsertNextPoint(x_y_3_4)


        elif (val1 < iso and val2 < iso and val3 < iso and val4 > iso): # Case 6 : Only pid4 has greater value than given isovalue, all others have isovalue less than given isovalue

            x_4_3 = (val4 - iso)/(val4 - val3) * (vtidata.GetPoint(pid3)[0] - vtidata.GetPoint(pid4)[0]) + vtidata.GetPoint(pid4)[0]
            y_4_3 = (val4 - iso)/(val4 - val3) * (vtidata.GetPoint(pid3)[1] - vtidata.GetPoint(pid4)[1]) + vtidata.GetPoint(pid4)[1]
            x_y_4_3 = [x_4_3,y_4_3,25]
            points.InsertNextPoint(x_y_4_3)

            x_4_1 = (val4 - iso)/(val4 - val1) * (vtidata.GetPoint(pid1)[0] - vtidata.GetPoint(pid4)[0]) + vtidata.GetPoint(pid4)[0]
            y_4_1 = (val4 - iso)/(val4 - val1) * (vtidata.GetPoint(pid1)[1] - vtidata.GetPoint(pid4)[1]) + vtidata.GetPoint(pid4)[1]
            x_y_4_1 = [x_4_1,y_4_1,25]
            points.InsertNextPoint(x_y_4_1)

        ## When two points have greater value than given isovalue till the 12th block (Case 7, 8, 9, 10, 11, 12)

        elif (val1 > iso and val2 > iso and val3 < iso and val4 < iso): # Case 7 : Only 1 and 2 have greater value than given isovalue, 3 and 4 have less value than given isovalue

            x_2_3 = (val2 - iso)/(val2 - val3) * (vtidata.GetPoint(pid3)[0] - vtidata.GetPoint(pid2)[0]) + vtidata.GetPoint(pid2)[0]
            y_2_3 = (val2 - iso)/(val2 - val3) * (vtidata.GetPoint(pid3)[1] - vtidata.GetPoint(pid2)[1]) + vtidata.GetPoint(pid2)[1]
            x_y_2_3 = [x_2_3,y_2_3,25]
            points.InsertNextPoint(x_y_2_3)

            x_1_4 = (val1 - iso)/(val1 - val4) * (vtidata.GetPoint(pid4)[0] - vtidata.GetPoint(pid1)[0]) + vtidata.GetPoint(pid1)[0]
            y_1_4 = (val1 - iso)/(val1 - val4) * (vtidata.GetPoint(pid4)[1] - vtidata.GetPoint(pid1)[1]) + vtidata.GetPoint(pid1)[1]
            x_y_1_4 = [x_1_4,y_1_4,25]
            points.InsertNextPoint(x_y_1_4)


        elif (val1 > iso and val2 < iso and val3 > iso and val4 < iso): # Case 8 : Only 1 and 3 have greater value than given isovalue, 2 and 4 have less value than given isovalue

            x_1_2 = (val1 - iso)/(val1 - val2) * (vtidata.GetPoint(pid2)[0] - vtidata.GetPoint(pid1)[0]) + vtidata.GetPoint(pid1)[0]
            y_1_2 = (val1 - iso)/(val1 - val2) * (vtidata.GetPoint(pid2)[1] - vtidata.GetPoint(pid1)[1]) + vtidata.GetPoint(pid1)[1]
            x_y_1_2 = [x_1_2,y_1_2,25]
            points.InsertNextPoint(x_y_1_2)

            x_2_3 = (val2 - iso)/(val2 - val3) * (vtidata.GetPoint(pid3)[0] - vtidata.GetPoint(pid2)[0]) + vtidata.GetPoint(pid2)[0]
            y_2_3 = (val2 - iso)/(val2 - val3) * (vtidata.GetPoint(pid3)[1] - vtidata.GetPoint(pid2)[1]) + vtidata.GetPoint(pid2)[1]
            x_y_2_3 = [x_2_3,y_2_3,25]
            points.InsertNextPoint(x_y_2_3)

            x_3_4 = (val3 - iso)/(val3 - val4) * (vtidata.GetPoint(pid4)[0] - vtidata.GetPoint(pid3)[0]) + vtidata.GetPoint(pid3)[0]
            y_3_4 = (val3 - iso)/(val3 - val4) * (vtidata.GetPoint(pid4)[1] - vtidata.GetPoint(pid3)[1]) + vtidata.GetPoint(pid3)[1]
            x_y_3_4 = [x_3_4,y_3_4,25]
            points.InsertNextPoint(x_y_3_4)

            x_1_4 = (val1 - iso)/(val1 - val4) * (vtidata.GetPoint(pid4)[0] - vtidata.GetPoint(pid1)[0]) + vtidata.GetPoint(pid1)[0]
            y_1_4 = (val1 - iso)/(val1 - val4) * (vtidata.GetPoint(pid4)[1] - vtidata.GetPoint(pid1)[1]) + vtidata.GetPoint(pid1)[1]
            x_y_1_4 = [x_1_4,y_1_4,25]
            points.InsertNextPoint(x_y_1_4)


        elif (val1 > iso and val2 < iso and val3 < iso and val4 > iso): # Case 9 : Only 1 and 4 have greater value than given isovalue, 3 and 2 have less value than given isovalue

            x_1_2 = (val1 - iso)/(val1 - val2) * (vtidata.GetPoint(pid2)[0] - vtidata.GetPoint(pid1)[0]) + vtidata.GetPoint(pid1)[0]
            y_1_2 = (val1 - iso)/(val1 - val2) * (vtidata.GetPoint(pid2)[1] - vtidata.GetPoint(pid1)[1]) + vtidata.GetPoint(pid1)[1]
            x_y_1_2 = [x_1_2,y_1_2,25]
            points.InsertNextPoint(x_y_1_2)

            x_4_3 = (val4 - iso)/(val4 - val3) * (vtidata.GetPoint(pid3)[0] - vtidata.GetPoint(pid4)[0]) + vtidata.GetPoint(pid4)[0]
            y_4_3 = (val4 - iso)/(val4 - val3) * (vtidata.GetPoint(pid3)[1] - vtidata.GetPoint(pid4)[1]) + vtidata.GetPoint(pid4)[1]
            x_y_4_3 = [x_4_3,y_4_3,25]
            points.InsertNextPoint(x_y_4_3)

        
        elif (val1 < iso and val2 > iso and val3 > iso and val4 < iso): # Case 10 : Only 2 and 3 have greater value than given isovalue, 1 and 4 have less value than given isovalue
            
            x_2_1 = (val2 - iso)/(val2 - val1) * (vtidata.GetPoint(pid1)[0] - vtidata.GetPoint(pid2)[0]) + vtidata.GetPoint(pid2)[0]
            y_2_1 = (val2 - iso)/(val2 - val1) * (vtidata.GetPoint(pid1)[1] - vtidata.GetPoint(pid2)[1]) + vtidata.GetPoint(pid2)[1]
            x_y_2_1 = [x_2_1,y_2_1,25]
            points.InsertNextPoint(x_y_2_1)

            x_3_4 = (val3 - iso)/(val3 - val4) * (vtidata.GetPoint(pid4)[0] - vtidata.GetPoint(pid3)[0]) + vtidata.GetPoint(pid3)[0]
            y_3_4 = (val3 - iso)/(val3 - val4) * (vtidata.GetPoint(pid4)[1] - vtidata.GetPoint(pid3)[1]) + vtidata.GetPoint(pid3)[1]
            x_y_3_4 = [x_3_4,y_3_4,25]
            points.InsertNextPoint(x_y_3_4)


        elif (val1 < iso and val2 > iso and val3 < iso and val4 > iso): # Case 11 : Only 2 and 4 have greater value than given isovalue, 1 and 3 have less value than given isovalue     

            x_2_1 = (val2 - iso)/(val2 - val1) * (vtidata.GetPoint(pid1)[0] - vtidata.GetPoint(pid2)[0]) + vtidata.GetPoint(pid2)[0]
            y_2_1 = (val2 - iso)/(val2 - val1) * (vtidata.GetPoint(pid1)[1] - vtidata.GetPoint(pid2)[1]) + vtidata.GetPoint(pid2)[1]
            x_y_2_1 = [x_2_1,y_2_1,25]
            points.InsertNextPoint(x_y_2_1)

            x_2_3 = (val2 - iso)/(val2 - val3) * (vtidata.GetPoint(pid3)[0] - vtidata.GetPoint(pid2)[0]) + vtidata.GetPoint(pid2)[0]
            y_2_3 = (val2 - iso)/(val2 - val3) * (vtidata.GetPoint(pid3)[1] - vtidata.GetPoint(pid2)[1]) + vtidata.GetPoint(pid2)[1]
            x_y_2_3 = [x_2_3,y_2_3,25]
            points.InsertNextPoint(x_y_2_3)

            x_4_3 = (val4 - iso)/(val4 - val3) * (vtidata.GetPoint(pid3)[0] - vtidata.GetPoint(pid4)[0]) + vtidata.GetPoint(pid4)[0]
            y_4_3 = (val4 - iso)/(val4 - val3) * (vtidata.GetPoint(pid3)[1] - vtidata.GetPoint(pid4)[1]) + vtidata.GetPoint(pid4)[1]
            x_y_4_3 = [x_4_3,y_4_3,25]
            points.InsertNextPoint(x_y_4_3)

            x_4_1 = (val4 - iso)/(val4 - val1) * (vtidata.GetPoint(pid1)[0] - vtidata.GetPoint(pid4)[0]) + vtidata.GetPoint(pid4)[0]
            y_4_1 = (val4 - iso)/(val4 - val1) * (vtidata.GetPoint(pid1)[1] - vtidata.GetPoint(pid4)[1]) + vtidata.GetPoint(pid4)[1]
            x_y_4_1 = [x_4_1,y_4_1,25]
            points.InsertNextPoint(x_y_4_1)


        elif (val1 < iso and val2 < iso and val3 > iso and val4 > iso): # Case 12 : Only 3 and 4 have greater value than given isovalue, 1 and 2 have less value than given isovalue

            x_3_2 = (val3 - iso)/(val3 - val2) * (vtidata.GetPoint(pid2)[0] - vtidata.GetPoint(pid3)[0]) + vtidata.GetPoint(pid3)[0]
            y_3_2 = (val3 - iso)/(val3 - val2) * (vtidata.GetPoint(pid2)[1] - vtidata.GetPoint(pid3)[1]) + vtidata.GetPoint(pid3)[1]
            x_y_3_2 = [x_3_2,y_3_2,25]
            points.InsertNextPoint(x_y_3_2)

            x_4_1 = (val4 - iso)/(val4 - val1) * (vtidata.GetPoint(pid1)[0] - vtidata.GetPoint(pid4)[0]) + vtidata.GetPoint(pid4)[0]
            y_4_1 = (val4 - iso)/(val4 - val1) * (vtidata.GetPoint(pid1)[1] - vtidata.GetPoint(pid4)[1]) + vtidata.GetPoint(pid4)[1]
            x_y_4_1 = [x_4_1,y_4_1,25]
            points.InsertNextPoint(x_y_4_1)

        ## When two points have greater value than given isovalue till the 12th block (Case 13, 14, 15, 16)

        elif (val1 > iso and val2 > iso and val3 < iso and val4 > iso): # Case 13 : 1, 2, 4 is have large value than given isovalue, 3 is smaller

            x_2_3 = (val2 - iso)/(val2 - val3) * (vtidata.GetPoint(pid3)[0] - vtidata.GetPoint(pid2)[0]) + vtidata.GetPoint(pid2)[0]
            y_2_3 = (val2 - iso)/(val2 - val3) * (vtidata.GetPoint(pid3)[1] - vtidata.GetPoint(pid2)[1]) + vtidata.GetPoint(pid2)[1]
            x_y_2_3 = [x_2_3,y_2_3,25]
            points.InsertNextPoint(x_y_2_3)

            x_4_3 = (val4 - iso)/(val4 - val3) * (vtidata.GetPoint(pid3)[0] - vtidata.GetPoint(pid4)[0]) + vtidata.GetPoint(pid4)[0]
            y_4_3 = (val4 - iso)/(val4 - val3) * (vtidata.GetPoint(pid3)[1] - vtidata.GetPoint(pid4)[1]) + vtidata.GetPoint(pid4)[1]
            x_y_4_3 = [x_4_3,y_4_3,25]
            points.InsertNextPoint(x_y_4_3)


        elif (val1 > iso and val2 > iso and val3 > iso and val4 < iso): # Case 14 : 1, 2, 3 is have large value than given isovalue, 4 is smaller

            x_3_4 = (val3 - iso)/(val3 - val4) * (vtidata.GetPoint(pid4)[0] - vtidata.GetPoint(pid3)[0]) + vtidata.GetPoint(pid3)[0]
            y_3_4 = (val3 - iso)/(val3 - val4) * (vtidata.GetPoint(pid4)[1] - vtidata.GetPoint(pid3)[1]) + vtidata.GetPoint(pid3)[1]
            x_y_3_4 = [x_3_4,y_3_4,25]
            points.InsertNextPoint(x_y_3_4)

            x_1_4 = (val1 - iso)/(val1 - val4) * (vtidata.GetPoint(pid4)[0] - vtidata.GetPoint(pid1)[0]) + vtidata.GetPoint(pid1)[0]
            y_1_4 = (val1 - iso)/(val1 - val4) * (vtidata.GetPoint(pid4)[1] - vtidata.GetPoint(pid1)[1]) + vtidata.GetPoint(pid1)[1]
            x_y_1_4 = [x_1_4,y_1_4,25]
            points.InsertNextPoint(x_y_1_4)


        elif (val1 > iso and val2 < iso and val3 > iso and val4 > iso): # Case 15 : 1, 3, 4 is have large value than given isovalue, 2 is smaller

            x_1_2 = (val1 - iso)/(val1 - val2) * (vtidata.GetPoint(pid2)[0] - vtidata.GetPoint(pid1)[0]) + vtidata.GetPoint(pid1)[0]
            y_1_2 = (val1 - iso)/(val1 - val2) * (vtidata.GetPoint(pid2)[1] - vtidata.GetPoint(pid1)[1]) + vtidata.GetPoint(pid1)[1]
            x_y_1_2 = [x_1_2,y_1_2,25]
            points.InsertNextPoint(x_y_1_2)

            x_3_2 = (val3 - iso)/(val3 - val2) * (vtidata.GetPoint(pid2)[0] - vtidata.GetPoint(pid3)[0]) + vtidata.GetPoint(pid3)[0]
            y_3_2 = (val3 - iso)/(val3 - val2) * (vtidata.GetPoint(pid2)[1] - vtidata.GetPoint(pid3)[1]) + vtidata.GetPoint(pid3)[1]
            x_y_3_2 = [x_3_2,y_3_2,25]
            points.InsertNextPoint(x_y_3_2)

        
        elif (val1 < iso and val2 > iso and val3 > iso and val4 > iso): # Case 16 : 2, 3, 4 is have large value than given isovalue, 1 is smaller

            x_2_1 = (val2 - iso)/(val2 - val1) * (vtidata.GetPoint(pid1)[0] - vtidata.GetPoint(pid2)[0]) + vtidata.GetPoint(pid2)[0]
            y_2_1 = (val2 - iso)/(val2 - val1) * (vtidata.GetPoint(pid1)[1] - vtidata.GetPoint(pid2)[1]) + vtidata.GetPoint(pid2)[1]
            x_y_2_1 = [x_2_1,y_2_1,25]
            points.InsertNextPoint(x_y_2_1)

            x_4_1 = (val4 - iso)/(val4 - val1) * (vtidata.GetPoint(pid1)[0] - vtidata.GetPoint(pid4)[0]) + vtidata.GetPoint(pid4)[0]
            y_4_1 = (val4 - iso)/(val4 - val1) * (vtidata.GetPoint(pid1)[1] - vtidata.GetPoint(pid4)[1]) + vtidata.GetPoint(pid4)[1]
            x_y_4_1 = [x_4_1,y_4_1,25]
            points.InsertNextPoint(x_y_4_1)
## -------------------------------------------------------------------------------------------------


## Finding Total No. of Isocontour Points found
## ----------------------------------------------
no_of_contour_points = points.GetNumberOfPoints()
print("Total no. of Contour Points :" ,no_of_contour_points)
## ----------------------------------------------

## Inserting points into the vtkPolyData object
## --------------------------------------------
pol_data.SetPoints(points)
## --------------------------------------------

## Creating an object of vtkPolyLine to store the lines and give it to vtkCellArray
## --------------------------------------------------------------------------------
polyLine = vtk.vtkPolyLine()
## --------------------------------------------------------------------------------


## Adding all the Line segments and taking 2 points at a time 
## ----------------------------------------------------------
i = 0
while (i < no_of_contour_points):
    polyLine.GetPointIds().SetNumberOfIds(2)  ## I am taking 2 points at a time because all the pair wise points are linked to each other (in if conditions)
    polyLine.GetPointIds().SetId(0,i)         ## Taking first point 
    polyLine.GetPointIds().SetId(1,i+1)       ## Taking second point
    contour_lines.InsertNextCell(polyLine)    ## Linking them and making the line
    i += 2
## ----------------------------------------------------------

## Setting contour lines in the vtkPolyData
## ----------------------------------------
pol_data.SetLines(contour_lines)  
## ----------------------------------------



## Writing the polydata into a vtkpolydata file with extension *.vtp (isocontour_2D.vtp)
## ---------------------------------------------------------------------------------------------
writer = vtk.vtkXMLPolyDataWriter()
writer.SetInputData(pol_data)
writer.SetFileName('isocontour_2D.vtp')
writer.Write()
## ---------------------------------------------------------------------------------------------