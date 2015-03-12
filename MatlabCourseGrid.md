# Introduction #

How to make a grid in MatLab

Save your photo from google earth in /Documents/Matlab/

I saved mine as beagle.png

# Code #
```
clf
rgb = imread('beagle.png');
imshow(rgb)
hold on


M = size(rgb,1);
N = size(rgb,2);

for k = 1:8:M
    x = [1 N];
    y = [k k];
    plot(x,y,'Color','w','LineStyle','-');
    plot(x,y,'Color','k','LineStyle',':');
end

for k = 1:8:N
    x = [k k];
    y = [1 M];
    plot(x,y,'Color','w','LineStyle','-');
    plot(x,y,'Color','k','LineStyle',':');
end

x = [283,428,428,246,204,179,167,62,69,75,109,68,100,76,59]
y=[61,79,214,230,244,269,308,309,142,110,93,84,70,61,40]
plot(x,y)

hold off
```

## TODO ##

  * We need better, accurate plot points, we need "points of interest" to correctly calibrate the beagleboard during the course.

  * We need to figure out either to 1) spit out the piecewise linear functions from matlab to use in python or 2) figure out how to do piecewise linear functions in python.(preferably the latter)
    * http://www.scipy.org/Cookbook/Interpolation

  * Preferably switch to cubic spline interpolation instead of piecewise linear interpolation for a smoother function

  * We need a safe margin of error to be in.

  * We need gps point locations so we can translate that between the graph and the raw data.

  * Wheel encoder information and a solid way of doing dead reckoning