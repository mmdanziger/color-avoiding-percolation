Color Avoiding Percolation
=================

This repository contains the code used for the color-avoiding percolation papers:

Hidden Connectivity in Networks with Vulnerable Classes of Nodes  
Sebastian M. Krause, Michael M. Danziger, and Vinko Zlatić  
Phys. Rev. X 6, 041022 – Published 27 October 2016  
https://doi.org/10.1103/PhysRevX.6.041022  

Color-avoiding percolation
Sebastian M. Krause, Michael M. Danziger, and Vinko Zlatić  
Phys. Rev. E 96, 022313 – Published 14 August 2017  
https://doi.org/10.1103/PhysRevE.96.022313  


Subdirectories
--------------
colornet - generate a random network and use a disjoint sets based algorithm to calculate the color-avoiding connectivity  
manycolornet - generate a random network or read a network from a file and use BFS to calculate the color-avoiding connectivity  
colornet_scripts - python scripts used to load simulation results, generate plots, and calculate theoretical predictions  
real_data - directory for CAIDE AS data (the data is not publicly available, please contact us if you are interested in using it)  
data_scripts - scripts for loading the real data and plotting maps based on it  

If you would like to use this code, please cite the original paper(s).
