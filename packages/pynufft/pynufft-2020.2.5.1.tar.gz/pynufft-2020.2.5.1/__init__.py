# from . import src 
#from .linalg.nufft_cpu import NUFFT_cpu#, NUFFT_excalibur#, NUFFT_mCoil, NUFFT_excalibur
#from .linalg.nudft_cupy import NUDFT_cupy
from .nufft import NUFFT

from .linalg.nufft_cpu import NUFFT_cpu

try:
    from .linalg.nufft_hsa import NUFFT_hsa
except:
    pass
    print("Failed to import NUFFT_hsa (deprecated). Use NUFFT() instead. ")

from .linalg.nudft_cpu import NUDFT

try:
    from .linalg.nudft_cupy import NUDFT_cupy
except:
    pass
    print("Failed to import NUFFT_hsa (deprecated). Use NUFFT() instead. ")
#from .linalg.nufft_hsa import NUFFT_hsa
#from .linalg.nufft_hsa_legacy import NUFFT_hsa_legacy
from .src._helper import helper
