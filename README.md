# share_phymol
## The files in this project are meant to be reviewed by the PHYMOL committee according to the application procedure

I attached two folder containing to different project (one in C one in Python):

# bt_project
## C
This is the program of my Bachelor project made in spring 2021. 

  The program code-size_var_M1.c solves the micelle distribution (feeding in concentration of monomer to then obtain global concentration). 
In secondary steps the distributions are plotted and then combined with tex to the final TEX/standalone-size.pdf.
User input giving the range of parameters to be explored is given in the main function.

  The algorithm is found in header/header-distribution_SERIES.h. It relies on a bissection algorithm to solve (x-f(x)==0) where f is the sum over the distribution calculated by the boltzman distribution. The relative Free Energy is determined in the module /header/header-distribution_FREE-ENERGY-FRUST.h based on frustration potentials according to the packing parameter model.

  If I would do the script now again I would definitely read user input from a file and use Pyplot instead of gnuplot.

# rotation_script
## PYTHON
I did this project during my research internship in Thailand in summer 2022.

  It aims at the automatization of filtering multiple starting conformers to the one that shows the strongest transition dipole moment. The degrees of freedom are read from user input (example 1_generate_operations/CO_op.txt). Then the input geometries are obtained by performing and commuting through the operations (here only rotations, because these where important for the project) and optionally printed as gaussian input files for the optimization. The corresponding script 2_transforms_coords/script_displacement.py and its module 0-2_modules/mod_geometry.py is maybe the most interesting script to look at.

  The code is modularized and has a script for every step involved:
(evaluation and filtering of highest DP moments -> generation of new input file calculating Transition DP moment -> evaluation of highest TDPM -> plot)
The results are also plotted in the last module at 4_evaluate_TDIPM/logs/3_res_pdfs/CF3_B3LYP_TD_analysis.pdf.

  Unfortunatelly, the group is not using the script. They dont have experience in python and while I based my project completely on the script there would be certainly a collaboration needed to launch this script into pratical use and check for errors occuring in new files. I had started the goal with the aim of creating something usefull though and had fun creating the script.
  
  If I would do the script now again I would work with dictioniaries instead of arrays for better overview or more likely go the next step and work with classes in python.
