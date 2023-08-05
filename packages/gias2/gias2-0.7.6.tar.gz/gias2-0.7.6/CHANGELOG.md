# GIAS2 Change log

## 0.7.6
- disable reload_support from cython modules. This has been reported to cause a crash on windows. See https://github.com/cython/cython/issues/3837

## 0.7.5
- fix cython build warnings from duplicate implementation in cython_csg.pyx

## 0.7.4
- vectorise make_sub_mesh to increase performance of creating a mesh from the faces of another mesh
- fix matrix multiplication in SVD calculation of rigid transform matrix

## 0.7.3
- type hinting across the following modules
  - image_tools
  - csgtools
  - inp
  - plywriter
  - simplemesh
  - smutils
  - vtktools
  - shapemodel

## 0.7.2
- more type hinting

## 0.7.1
- logging fixes
- tests for geometry functions
- type hinting for geoprimitives.py and transform3D.py

## 0.7.0
- removed all print statements, replaced by logging
- TODO configure default logging
- From here on:
  - python 2 support for be discontinued
  - pep8 naming convention will be implemented

## 0.6.17
- code clean up
- added VTK as a dependency

## 0.6.16
- removed matplotlib as a requirement. User should install it it separately if they need 3D plotting functionalities

## 0.6.15
- allow NPZ files to be loaded with object arrays to handle old PCA npz result files. This was disabled in numpy 1.18.
- increased numpy dependency to latest version.
- fixed rigid body sliders in fieldvi.
- specified dependency versions for numpy, scipy, cython, skimage, sklearn

## 0.6.14
- Added pydicom 1.3.0 as a requirement for dicom reading
- updates to dicom_series to work with pydicom 1.3.0

## 0.6.12
- cleaned up cython language-levels
- PyPi compliant readme
- Plane method to get close-by points
- dicom_series fix for scans with no slope (e.g. MRI)

## 0.6.12
- improved dicom slice reordering

## 0.6.11
- fix to smutil for removing small regions

## 0.6.10
- transform barycenters when affine transforming a simple mesh

## 0.6.9
- Corrected orientation and dimension of slices sampled from scans

## 0.6.8
- Use ImagePositionPatient if SliceLocation is missing for slice ordering
- clip values to 1 in angle calculation

## 0.6.7
- better scan slicing method

## 0.6.6
- added rigidbody visualisation tab for fieldvi
- auto loads dicom series with the most number of slices

## 0.6.5
- avoid using numpy helps when convering numpy points to vtk points in python 2. This should fix the issue of giasrbfreg outputting meshes with a vertex at origin.

## 0.6.4
- enabled 2way fitmode for pc fitting
- fixed set_affine_matrix in Scan class

## 0.6.3
- added hasFaceNormals attribute to Simplemesh for consistency

## 0.6.2
- calculate intersection between plane and line
- affine transform for CSG
- fixed CSG cube

## 0.6.1
- update i2c and c2i matrices in downscale method if copy==False 

## 0.6.0
- optimised Cython implementation of csg package included.
- csgtools now uses the included Cython csg module.

## 0.5.3
- optionally use least_squares for point-cloud shapemodel fitting

## 0.5.2
- for arrays for be contiguous when passed to VTK

## 0.5.1
- fixes for app in points-only mode

## 0.5.0
- upgrade to depending on pydicom 1.1. May not work with pydicom <1.0.
- added dicom_series module

## 0.4.29
- simplemesh affine also transforms normals
- set methods for scan i2c and c2i matrices

## 0.4.28
- fallback ply writer for including vertex normals

## 0.4.27
- bug fixes with scan zoom method

## 0.4.26
- improved handling of dicom handling, now longer require z-flipping
- dicom affine updated in cropping, zoom, and downscaling.

## 0.4.25
- dicom affine tested against itksnap, however flip z need to be flipped manually

## 0.4.24
- added keyboard input wait after visualisation in application scripts
- added Line3D method for projecting a coordinate
- control rbf registration verbosity

## 0.4.23
- improvements to cartesian coordinates system class
- improvements to 3D plane visualisation
- fixed api misused in fieldvi
- RBF multipass reg added to registration

## 0.4.22
- added gias-inpsampledicom app

## 0.4.21
- rbfreg now reads in a config file (in examples) to control fitting and allows arbitrary number of iterations
- vtk included in requirements

## 0.4.20-RC1
- inp_sample_dicom.py and hmf_inp_2_surf.py examples
- giashmfinp2surf application
- Scan optionally uses transformation matrix for index2Coord and coord2Index
- inp module handles elsets and other under the hood improvements
- fixed gias2trainpcashapemodel plotting bug
- fixed vtk image to surface pipelining
- merge sm function

## 0.4.18
- removed version requirement for VTK

## 0.4.17
- updated install_requires list to include vtk, skimage, and cython
- added downscale method for image_tools.Scan
- fixed missing marker bug when parsing lower limb markers
- fixed image2surf conversion in vtk 6+ due to datatype bug
- pretty stable on python 3.5

## 0.4.16
- Updates the RBF registration
- surface distance application
- INP file reading only reads nodes referenced by ELSET

## 0.4.15
- Tri-surface pc registration module and application.
- Colour options for pctraining application.

## 0.4.13
- application scripts

## 0.4.12
- RBF module added the registration subpackage for non-rigid registration.
- Added 3 scripts to the new applications folder
	- rigidreg.py: rigid body registration between point clouds or surface meshes
	- rbfreg.py: RBF-based non-rigid registration between point clouds or surface meshes
	- trainpcashapemodel.py: train a pca-based shape model using a set of correspondent point clouds or surface meshes

## 0.4.11
- updated HJC regression functions to match ISB coordinate system

## 0.4.10
- fixed vector normalisation in fw_segmentation_tools

## 0.4.9
Minor bug fixes.
- tidied up use of common.math.norm in geometric_field
- optional args for array2vtkimage
- fixed spline_tools import

## 0.4.8
- Fixed VTK6 compatibility with image array conversion and binary mask creation

## 0.4.7
- Fixed quadratic simplex element basis functions
- Fixed normalsmoother2 getting edge direction confused with quadratic elements. New method for finding shared edges and their relative directions.

## 0.4.6

This release focuses on the addition of simplex quadratric Lagrange elements and evaluation of arc-lengths to the fieldwork sub-package.

### General
- utility functions for working with simplemeshes
- LineSegment3D setAB method added 
- added version_info variable

### Fieldwork
- new method to create 1d curve elements from sets of nodes
- derivation of quadratric arclength
- test scripts for 1d element arc length evaluation 
- updated hostmeshfit function to working order
- derivation for quadratic simplex elements
- changed topolopy of template 2tri quad patches to be more symmetric
- fixed simplex quadratic lagrange invert mapping 
- completed implementation of simplex_L2_L2 basis

### Image Analysis
- added gaussian_filter method

### Visualisation
- check if scene object is a list of objects when toggling visibility
- draw 1-D mesh using separate curves for each element
- replaced text plotting using mlab.text to mlab.text3d

### OpenSim
- wrapping object class added