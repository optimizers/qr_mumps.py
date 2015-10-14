from qr_mumps.qr_mumps_context import qr_mumpsContext
import numpy as np
import sys

m = 7
n = 5
A = np.array([[0,0.1,0,0,0], [0.7,0,0.3,0.5,0.1], [0.6,0,0,0.2,0], [0,0,0.6,0,0.6], [0,0,0.7,0,0], [0.4,0.1,0,0,0], [0,0,0.2,0,0]], dtype=np.float64)
arow = np.array([1,2,5,0,5,1,3,4,6,1,2,1,3], dtype=np.int32)
acol = np.array([0,0,0,1,1,2,2,2,2,3,3,4,4], dtype=np.int32)
aval = np.array([0.7,0.6,0.4,0.1,0.1,0.3,0.6,0.7,0.2,0.5,0.2,0.1,0.6], dtype=np.float64)

context = qr_mumpsContext((m, n, arow, acol, aval), verbose=False)
print "ca marche"
context.analyze()
print context.analyzed

context.factorize()

e = np.ones(n, dtype=np.float64)
rhs = np.dot(A, e)

x = context.solve(rhs)
np.testing.assert_almost_equal(x,e)
print rhs, x


print "= " * 80

B = np.ones([n, 3], dtype=np.float64)
B[: ,1] = 2 * B[:,1]
B[: ,2] = 3 * B[:,2]
rhs = np.dot(A,B)

x = context.solve(rhs)
print rhs
print x
np.testing.assert_almost_equal(x,B)

print "= " * 80

B = np.ones([n, 3], dtype=np.float64)
B[: ,1] = 2 * B[:,1]
B[: ,2] = 3 * B[:,2]
rhs = np.dot(A,B)

x = context.least_squares(rhs)
print rhs
print x
np.testing.assert_almost_equal(x,B)


print "= " * 80

B = np.ones([m, 3], dtype=np.float64)
B[: ,1] = 2 * B[:,1]
B[: ,2] = 3 * B[:,2]
rhs = np.dot(A.T,B)

x = context.minimum_norm(rhs)
print rhs
print x
np.testing.assert_almost_equal(x,B)

