import vtk as vtk

## Load the Volume Data
## -----------------------------------------------
reader = vtk.vtkXMLImageDataReader()              # 'reader' is a object of vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_3D.vti')          #  Using 'reader' we will read the '*.vti' file from given location.
reader.Update()                                   #  Updating the 'reader' so that we always get the updated file.
vtidata = reader.GetOutput()                      #  We are initializing the output of the .vti file into a variable 
                                                  #     named 'vtidata'
## ------------------------------------------------

## Creating an instance of vtk Color Transfer Function
## ---------------------------------------------------
color_trans = vtk.vtkColorTransferFunction()
color_trans.AddRGBPoint(-4931.54, 0, 1, 1)            ## Adding RGB point values to the Color Transfer Function
color_trans.AddRGBPoint(-2508.95, 0, 0, 1)
color_trans.AddRGBPoint(-1873.9, 0, 0, 0.5)
color_trans.AddRGBPoint(-1027.16, 1, 0, 0)
color_trans.AddRGBPoint(-298.031, 1, 0.4, 0)
color_trans.AddRGBPoint(2594.97, 1, 1, 0)
## ---------------------------------------------------

## Creating an instance of vtk Piecewise Function (Opacity Transfer Function)
## --------------------------------------------------------------------------
opacity_trans = vtk.vtkPiecewiseFunction()
opacity_trans.AddPoint(-4931.54, 1.0)                 ## Adding point values to the Opacity Transfer Function
opacity_trans.AddPoint(101.815, 0.002)
opacity_trans.AddPoint(2594.97, 0.0)
## --------------------------------------------------------------------------

## Creating a volume mapper using vtkSmartVolumeMapper function
## ------------------------------------------------------------
volumeMapper = vtk.vtkSmartVolumeMapper()
volumeMapper.SetInputData(reader.GetOutput())      ## Giving input to the volume mapper as reader's output
## ------------------------------------------------------------

## Creating a Volume Property using vtkVolumeProperty
## -------------------------------------------------- 
v_prop = vtk.vtkVolumeProperty()   
v_prop.SetColor(color_trans)                   ## Setting Color value as the Color Transfer Function
v_prop.SetScalarOpacity(opacity_trans)         ## Setting Scalar Opacity value as the Opacity Transfer Function   
## -------------------------------------------------- 

## Deciding that the Phong should be ON or OFF
## ----------------------------------------------------------------
v_prop.ShadeOff()                         ## Initially I made the Phong OFF
v_prop.SetInterpolationTypeToLinear()

decision = input("Do you want to use the Phong Shading ? (yes/no) : ")
if decision == "yes":                     ## If user wants the Phong to be on then we are making Phong ON
    v_prop.ShadeOn()
    v_prop.SetInterpolationTypeToLinear()
## ----------------------------------------------------------------

## Creating a Volume for mapper to map
## -----------------------------------
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(v_prop)

volume.GetProperty().SetAmbient(0.5)    ## Setting the Ambient Coefficient as 0.5
volume.GetProperty().SetDiffuse(0.5)    ## Setting the Diffuse Coefficient as 0.5
volume.GetProperty().SetSpecular(0.5)   ## Setting the Specular Coefficient as 0.5
## -----------------------------------

## Creating a Renderer and adding the Volume 
## -----------------------------------------
renderer = vtk.vtkRenderer()
renderer.AddVolume(volume)
## -----------------------------------------


## Creating a Render Window and adding the Renderer
## ------------------------------------------------
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(1000,1000)           ## Setting rendering window size as (1000 x 1000) as mentioned
## ------------------------------------------------

## Creating an Interactor and starting the Rendering
## -------------------------------------------------
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.Start()
## -------------------------------------------------