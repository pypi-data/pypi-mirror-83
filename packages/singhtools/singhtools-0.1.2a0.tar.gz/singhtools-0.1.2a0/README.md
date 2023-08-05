# Singh-Tools
Tools for generating Singh plots

The function singhvals returns a sorted list of values in the interval [0,1] which should be used as x-coordinates in a 2D plot on the unit square, with a uniform function plotted on the y-axis.

The input c_struct should define an inverse confidence structure which determines the alpha confidence level required to cover the supplied 'true_param' for a given data set. This can be imprecise, but in this case the imprecision should be represented by a list or array of endpoints. Support for pba intervals will be added in the future.

