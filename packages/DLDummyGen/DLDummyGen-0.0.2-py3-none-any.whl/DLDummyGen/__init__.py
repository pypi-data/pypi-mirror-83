import inspect
import os
import sys

__version__ = '0.0.2'

real_path = os.path.dirname(os.path.abspath(__file__)).replace("\\","/")
sys.path.append(real_path)

try:
    from DLDummyGen import DLDummyGen
except ImportError as e:
    print(e," Can not import.")
    exit(1)


__all__ = [name for name, obj in locals().items()
           if not (name.startswith('_') or inspect.ismodule(obj))]