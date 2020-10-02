# Parafoil-Designer
CRT Parafoil Design Software

Credit for CD and CL calculations as well as design parameters, Steven Lingard, Basic Analysis of Ram Air Parachute
---Basic intro to Parafoil Designer---
This software must be used in tandem with xfoil.

Use xfoil to generate a list of alphas vs CL and CD, save these to a file.

Make sure this list covers from CL = 0 to max L/D.

Using spreadsheet software of choice, convert raw xfoil export file into a csv with headers "alpha", "CL", and "CD" for relevant columns. 

Make sure to have a json file created to store your final parachute. Tutorial parafoils are included in the release of Parafoil Designer.

Make sure to have a parafoil with an aspect ratio of 2. Any other aspect ratio will not work with this program out of the box, the tau and delta values will need to be edited
according to Steven Lingard's Basic Analysis of Ram Air Parachute.

These json format files should eventually work with ParaSim, but they currently do not, just copy the data over in the code.


---coeffCalc.py---
This is an old standalone script for calculating CL and CD, it is up to date in calculations and is compatible with Parafoil Designer json files.
Currently used only for generating pie charts of the CD components.

---parafoilPlot.py---
This is an old standalone script for plotting various things from xfoil csv files. Only used for demo purposes and visualization.