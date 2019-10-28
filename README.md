# 3D-Printer-ML

## Description
This project looked at using machine learning to optimise printing parameters. We used a Monoprice Select IIIP with standard 1.75mm PLA Extrude. We optimised for subjective print quality of a regular simple structure by altering printer head movement speed (feed rate) and extrusion amount. 

## Investigation
We initially obtained some sample data to observe the state space of feed rate and extrusion amount. By fixing each parameter in turn, we were able to observe clear trends and local maxima in performance. 

<img src="https://github.com/AryamanReddi99/3D-Printer-ML/blob/master/Images/Picture1.png?raw=true"> 
<img src="https://github.com/AryamanReddi99/3D-Printer-ML/blob/master/Images/Picture2.png?raw=true">

By fitting a best-fit function to our sample data, we were able to estimate the required constraint space and the magnitude of the partial derivatives of score with respect to x and y.

<img src="https://github.com/AryamanReddi99/3D-Printer-ML/blob/master/Images/Picture3.png?raw=true"> 

We followed a rudimentary reinforcement learning loop for our program: 

<img src="https://github.com/AryamanReddi99/3D-Printer-ML/blob/master/Images/workflow.png?raw=true"> 

The funtion "create test params" was defined as such:

<img src="https://github.com/AryamanReddi99/3D-Printer-ML/blob/master/Images/workflow1.png?raw=true"> 

Note that a logarithmic regressive learning rate was used to ensure our parameters converged on the global maximum. 

<img src="https://github.com/AryamanReddi99/3D-Printer-ML/blob/master/Images/workflow2.png?raw=true"> 

Applying this workflow to some initial sample data yielded the following fit optimisation. The green data point in each plot is the printer's choice for the next data point to try.

<img src="https://github.com/AryamanReddi99/3D-Printer-ML/blob/master/Images/Picture4.png?raw=true"> 

Here's are images of a simple print for a cube. As feed rate and extrude amount are optimised for simultaneously, we can observe a clear increase in quality over each iteration.

<img src="https://github.com/AryamanReddi99/3D-Printer-ML/blob/master/Images/Picture5.png?raw=true"> 

Here is an alternate run of the program where the intial random sample data happened to be worse. Note that the final print has not been as finely tuned by the learning program as in the above example, but the change in quality over the total run is larger. 

<img src="https://github.com/AryamanReddi99/3D-Printer-ML/blob/master/Images/Picture6.png?raw=true"> 
