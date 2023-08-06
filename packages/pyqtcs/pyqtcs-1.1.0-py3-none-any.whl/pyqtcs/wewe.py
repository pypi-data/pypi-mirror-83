import pyqtcs
import numpy as np

print(pyqtcs.__version__)

pyqtcs.qtclass.print_test()

a = np.array([1, 23, 45, 6, 78, 9])
print(pyqtcs.MA(a, 2))


