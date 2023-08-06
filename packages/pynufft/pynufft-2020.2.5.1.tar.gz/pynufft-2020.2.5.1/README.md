
# PyNUFFT: Python non-uniform fast Fourier transform

A minimal "getting start" tutorial is available at http://jyhmiinlin.github.io/pynufft/ .

![](g5738.jpeg)

## Installation

$ pip install pynufft --user


### Using Numpy/Scipy

```
$ python
Python 3.6.11 (default, Aug 23 2020, 18:05:39) 
[GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pynufft import NUFFT
>>> import numpy
>>> A = NUFFT()
>>> om = numpy.random.randn(10,2)
>>> Nd = (64,64)
>>> Kd = (128,128)
>>> Jd = (6,6)
>>> A.plan(om, Nd, Kd, Jd)
0
>>> x=numpy.random.randn(*Nd)
>>> y = A.forward(x)
```

### Using PyCUDA

```
>>> from pynufft import NUFFT, helper
>>> import numpy
>>> A2= NUFFT(helper.device_list()[0])
>>> A2.device
<reikna.cluda.cuda.Device object at 0x7f9ad99923b0>
>>> om = numpy.random.randn(10,2)
>>> Nd = (64,64)
>>> Kd = (128,128)
>>> Jd = (6,6)
>>> A2.plan(om, Nd, Kd, Jd)
0
>>> x=numpy.random.randn(*Nd)
>>> y = A2.forward(x)
```

### Using NUDFT (double precision)

Some users ask for double precision. 
NUDFT is offered.

```
>>> from pynufft import  NUDFT
>>> import numpy
>>> x=numpy.random.randn(*Nd)
>>> A = NUDFT()
>>> A.plan(om, Nd)
>>> y_cpu = A.forward(x)

```


## Testing GPU acceleration

```
Python 3.6.11 (default, Aug 23 2020, 18:05:39) 
[GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pynufft import tests
>>> tests.test_init(0)
device name =  <reikna.cluda.cuda.Device object at 0x7f41d4098688>
0.06576069355010987
0.006289639472961426
error gx2= 2.0638987e-07
error gy= 1.0912560261408778e-07
acceleration= 10.455399523742015
17.97926664352417 2.710083246231079
acceleration in solver= 6.634211944790991
```
### Comparisons

![](Figure_1.png)


### On the RRSG challenge of reproducible research in ISMRM 2019

The RRSG Challenge aims to reproduce the CG-SENSE paper (Pruessmann KP, Weiger M, Börnert P, Boesiger P. Advances in Sensitivity Encoding With Arbitrary k-Space Trajectories.
Magnetic Resonance in Medicine 2001;(46):638–651.).

Actually, PyNUFFT does not fail in this challenge. Our result is as follows. (The code is available on request)

The basic idea is to extract the coil sensitivity profiles from the center of k-space (as the ACS in ESPIRiT).

The problem is ill-conditioned. The square root of the sampling-density compensation function D<sup>1/2</sup> is needed. 

A nice feature about Scipy/Numpy is that we can build a scipy.sparse.LinearOperator.

This LinearOperator allows the problem to be solved by scipy.sparse.linalg.lsmr or scipy.sparse.linalg.lsqr. (Normal equation is not used in this case)

![](with_espirit.png)


### Contact information
J.-M. Lin
email: pynufft@gamil.com

