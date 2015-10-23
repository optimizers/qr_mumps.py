#!/usr/bin/env python

"""
This file tests basic operations on **all** types supported by QR_MUMPS
and on symmetric and general matrices.
"""

from qr_mumps.solver import QRMUMPSSolver
import numpy as np
from numpy.testing import *
import sys


class NumpyQRMUMPSSolverTestCaseMoreLinesThanColumns_INT32_FLOAT32(TestCase):
    def setUp(self):
        self.m = 7
        self.n = 5
        self.A = np.array([[0,0.1,0,0,0], [0.7,0,0.3,0.5,0.1], [0.6,0,0,0.2,0], [0,0,0.6,0,0.6], [0,0,0.7,0,0], [0.4,0.1,0,0,0], [0,0,0.2,0,0]], dtype=np.float32)
        self.arow = np.array([1,2,5,0,5,1,3,4,6,1,2,1,3], dtype=np.int32)
        self.acol = np.array([0,0,0,1,1,2,2,2,2,3,3,4,4], dtype=np.int32)
        self.aval = np.array([0.7,0.6,0.4,0.1,0.1,0.3,0.6,0.7,0.2,0.5,0.2,0.1,0.6], dtype=np.float32)

    def test_init(self):
        solver1 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        assert_equal(self.n, solver1.n)

    def test_analyze(self):
        solver2 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver2.analyze()
        assert(solver2.analyzed==True)

    def test_factorize(self):
        solver3 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver3.factorize()
        assert(solver3.analyzed==True)
        assert(solver3.factorized==True)

    def test_dense_solve_single_rhs(self):
        solver4 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver4.factorize()
        e = np.ones(self.n, dtype=np.float32)
        rhs = np.dot(self.A, e)
        x = solver4.solve(rhs)
        assert_almost_equal(x, e, 5)

    def test_dense_solve_multiple_rhs(self):
        solver5 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver5.factorize()
        B = np.ones([self.n, 3], dtype=np.float32)
        B[: ,1] = 2 * B[:,1]
        B[: ,2] = 3 * B[:,2]
        rhs = np.dot(self.A,B)
        x = solver5.solve(rhs)
        assert_almost_equal(x, B, 5)


class NumpyQRMUMPSSolverTestCaseMoreColumnsThanLines_INT32_FLOAT32(TestCase):
    def setUp(self):
        self.m = 5
        self.n = 7
        self.A = np.array([[0,0.7,0.6,0,0,0.4,0,], [0.1,0,0,0,0,0.1,0], [0,0.3,0,0.6,0.7,0,0.2], [0,0.5,0.2,0,0,0,0], [0,0.1,0,0.6,0,0,0]], dtype=np.float32)
        self.acol = np.array([1,2,5,0,5,1,3,4,6,1,2,1,3], dtype=np.int32)
        self.arow = np.array([0,0,0,1,1,2,2,2,2,3,3,4,4], dtype=np.int32)
        self.aval = np.array([0.7,0.6,0.4,0.1,0.1,0.3,0.6,0.7,0.2,0.5,0.2,0.1,0.6], dtype=np.float32)

    def test_init(self):
        solver1 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        assert_equal(self.n, solver1.n)
        assert_equal(self.m, solver1.m)

    def test_analyze(self):
        solver2 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver2.analyze()
        assert(solver2.analyzed==True)

    def test_factorize(self):
        solver3 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver3.factorize()
        assert(solver3.analyzed==True)
        assert(solver3.factorized==True)

    def test_dense_solve_single_rhs(self):
        solver4 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver4.factorize()
        e = np.ones(self.n, dtype=np.float32)
        rhs = np.dot(self.A, e)
        x = solver4.solve(rhs)
        assert_almost_equal(np.dot(self.A,x), rhs, 5)

    def test_dense_solve_multiple_rhs(self):
        solver5 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver5.factorize()
        B = np.ones([self.n, 3], dtype=np.float32)
        B[: ,1] = 2 * B[:,1]
        B[: ,2] = 3 * B[:,2]
        rhs = np.dot(self.A,B)
        x = solver5.solve(rhs)
        print x
        assert_almost_equal(np.dot(self.A,x), rhs, 5)


class NumpyQRMUMPSSolverTestCaseMoreLinesThanColumns_INT32_FLOAT64(TestCase):
    def setUp(self):
        self.m = 7
        self.n = 5
        self.A = np.array([[0,0.1,0,0,0], [0.7,0,0.3,0.5,0.1], [0.6,0,0,0.2,0], [0,0,0.6,0,0.6], [0,0,0.7,0,0], [0.4,0.1,0,0,0], [0,0,0.2,0,0]], dtype=np.float64)
        self.arow = np.array([1,2,5,0,5,1,3,4,6,1,2,1,3], dtype=np.int32)
        self.acol = np.array([0,0,0,1,1,2,2,2,2,3,3,4,4], dtype=np.int32)
        self.aval = np.array([0.7,0.6,0.4,0.1,0.1,0.3,0.6,0.7,0.2,0.5,0.2,0.1,0.6], dtype=np.float64)

    def test_init(self):
        solver1 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        assert_equal(self.n, solver1.n)

    def test_analyze(self):
        solver2 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver2.analyze()
        assert(solver2.analyzed==True)

    def test_factorize(self):
        solver3 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver3.factorize()
        assert(solver3.analyzed==True)
        assert(solver3.factorized==True)

    def test_dense_solve_single_rhs(self):
        solver4 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver4.factorize()
        e = np.ones(self.n, dtype=np.float64)
        rhs = np.dot(self.A, e)
        x = solver4.solve(rhs)
        assert_almost_equal(x, e, 5)

    def test_dense_solve_multiple_rhs(self):
        solver5 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver5.factorize()
        B = np.ones([self.n, 3], dtype=np.float64)
        B[: ,1] = 2 * B[:,1]
        B[: ,2] = 3 * B[:,2]
        rhs = np.dot(self.A,B)
        x = solver5.solve(rhs)
        assert_almost_equal(x, B, 5)


class NumpyQRMUMPSSolverTestCaseMoreColumnsThanLines_INT32_FLOAT64(TestCase):
    def setUp(self):
        self.m = 5
        self.n = 7
        self.A = np.array([[0,0.7,0.6,0,0,0.4,0,], [0.1,0,0,0,0,0.1,0], [0,0.3,0,0.6,0.7,0,0.2], [0,0.5,0.2,0,0,0,0], [0,0.1,0,0.6,0,0,0]], dtype=np.float64)
        self.acol = np.array([1,2,5,0,5,1,3,4,6,1,2,1,3], dtype=np.int32)
        self.arow = np.array([0,0,0,1,1,2,2,2,2,3,3,4,4], dtype=np.int32)
        self.aval = np.array([0.7,0.6,0.4,0.1,0.1,0.3,0.6,0.7,0.2,0.5,0.2,0.1,0.6], dtype=np.float64)

    def test_init(self):
        solver1 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        assert_equal(self.n, solver1.n)
        assert_equal(self.m, solver1.m)

    def test_analyze(self):
        solver2 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver2.analyze()
        assert(solver2.analyzed==True)

    def test_factorize(self):
        solver3 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver3.factorize()
        assert(solver3.analyzed==True)
        assert(solver3.factorized==True)

    def test_dense_solve_single_rhs(self):
        solver4 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver4.factorize()
        e = np.ones(self.n, dtype=np.float64)
        rhs = np.dot(self.A, e)
        x = solver4.solve(rhs)
        assert_almost_equal(np.dot(self.A,x), rhs, 5)

    def test_dense_solve_multiple_rhs(self):
        solver5 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver5.factorize()
        B = np.ones([self.n, 3], dtype=np.float64)
        B[: ,1] = 2 * B[:,1]
        B[: ,2] = 3 * B[:,2]
        rhs = np.dot(self.A,B)
        x = solver5.solve(rhs)
        print x
        assert_almost_equal(np.dot(self.A,x), rhs, 5)


class NumpyQRMUMPSSolverTestCaseMoreLinesThanColumns_INT32_COMPLEX64(TestCase):
    def setUp(self):
        self.m = 7
        self.n = 5
        self.A = np.array([[0,0.1,0,0,0], [0.7,0,0.3,0.5,0.1], [0.6,0,0,0.2,0], [0,0,0.6,0,0.6], [0,0,0.7,0,0], [0.4,0.1,0,0,0], [0,0,0.2,0,0]], dtype=np.complex64)
        self.arow = np.array([1,2,5,0,5,1,3,4,6,1,2,1,3], dtype=np.int32)
        self.acol = np.array([0,0,0,1,1,2,2,2,2,3,3,4,4], dtype=np.int32)
        self.aval = np.array([0.7,0.6,0.4,0.1,0.1,0.3,0.6,0.7,0.2,0.5,0.2,0.1,0.6], dtype=np.complex64)

    def test_init(self):
        solver1 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        assert_equal(self.n, solver1.n)

    def test_analyze(self):
        solver2 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver2.analyze()
        assert(solver2.analyzed==True)

    def test_factorize(self):
        solver3 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver3.factorize()
        assert(solver3.analyzed==True)
        assert(solver3.factorized==True)

    def test_dense_solve_single_rhs(self):
        solver4 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver4.factorize()
        e = np.ones(self.n, dtype=np.complex64)
        rhs = np.dot(self.A, e)
        x = solver4.solve(rhs)
        assert_almost_equal(x, e, 5)

    def test_dense_solve_multiple_rhs(self):
        solver5 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver5.factorize()
        B = np.ones([self.n, 3], dtype=np.complex64)
        B[: ,1] = 2 * B[:,1]
        B[: ,2] = 3 * B[:,2]
        rhs = np.dot(self.A,B)
        x = solver5.solve(rhs)
        assert_almost_equal(x, B, 5)


class NumpyQRMUMPSSolverTestCaseMoreColumnsThanLines_INT32_COMPLEX64(TestCase):
    def setUp(self):
        self.m = 5
        self.n = 7
        self.A = np.array([[0,0.7,0.6,0,0,0.4,0,], [0.1,0,0,0,0,0.1,0], [0,0.3,0,0.6,0.7,0,0.2], [0,0.5,0.2,0,0,0,0], [0,0.1,0,0.6,0,0,0]], dtype=np.complex64)
        self.acol = np.array([1,2,5,0,5,1,3,4,6,1,2,1,3], dtype=np.int32)
        self.arow = np.array([0,0,0,1,1,2,2,2,2,3,3,4,4], dtype=np.int32)
        self.aval = np.array([0.7,0.6,0.4,0.1,0.1,0.3,0.6,0.7,0.2,0.5,0.2,0.1,0.6], dtype=np.complex64)

    def test_init(self):
        solver1 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        assert_equal(self.n, solver1.n)
        assert_equal(self.m, solver1.m)

    def test_analyze(self):
        solver2 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver2.analyze()
        assert(solver2.analyzed==True)

    def test_factorize(self):
        solver3 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver3.factorize()
        assert(solver3.analyzed==True)
        assert(solver3.factorized==True)

    def test_dense_solve_single_rhs(self):
        solver4 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver4.factorize()
        e = np.ones(self.n, dtype=np.complex64)
        rhs = np.dot(self.A, e)
        x = solver4.solve(rhs)
        assert_almost_equal(np.dot(self.A,x), rhs, 5)

    def test_dense_solve_multiple_rhs(self):
        solver5 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver5.factorize()
        B = np.ones([self.n, 3], dtype=np.complex64)
        B[: ,1] = 2 * B[:,1]
        B[: ,2] = 3 * B[:,2]
        rhs = np.dot(self.A,B)
        x = solver5.solve(rhs)
        print x
        assert_almost_equal(np.dot(self.A,x), rhs, 5)


class NumpyQRMUMPSSolverTestCaseMoreLinesThanColumns_INT32_COMPLEX128(TestCase):
    def setUp(self):
        self.m = 7
        self.n = 5
        self.A = np.array([[0,0.1,0,0,0], [0.7,0,0.3,0.5,0.1], [0.6,0,0,0.2,0], [0,0,0.6,0,0.6], [0,0,0.7,0,0], [0.4,0.1,0,0,0], [0,0,0.2,0,0]], dtype=np.complex128)
        self.arow = np.array([1,2,5,0,5,1,3,4,6,1,2,1,3], dtype=np.int32)
        self.acol = np.array([0,0,0,1,1,2,2,2,2,3,3,4,4], dtype=np.int32)
        self.aval = np.array([0.7,0.6,0.4,0.1,0.1,0.3,0.6,0.7,0.2,0.5,0.2,0.1,0.6], dtype=np.complex128)

    def test_init(self):
        solver1 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        assert_equal(self.n, solver1.n)

    def test_analyze(self):
        solver2 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver2.analyze()
        assert(solver2.analyzed==True)

    def test_factorize(self):
        solver3 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver3.factorize()
        assert(solver3.analyzed==True)
        assert(solver3.factorized==True)

    def test_dense_solve_single_rhs(self):
        solver4 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver4.factorize()
        e = np.ones(self.n, dtype=np.complex128)
        rhs = np.dot(self.A, e)
        x = solver4.solve(rhs)
        assert_almost_equal(x, e, 5)

    def test_dense_solve_multiple_rhs(self):
        solver5 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver5.factorize()
        B = np.ones([self.n, 3], dtype=np.complex128)
        B[: ,1] = 2 * B[:,1]
        B[: ,2] = 3 * B[:,2]
        rhs = np.dot(self.A,B)
        x = solver5.solve(rhs)
        assert_almost_equal(x, B, 5)


class NumpyQRMUMPSSolverTestCaseMoreColumnsThanLines_INT32_COMPLEX128(TestCase):
    def setUp(self):
        self.m = 5
        self.n = 7
        self.A = np.array([[0,0.7,0.6,0,0,0.4,0,], [0.1,0,0,0,0,0.1,0], [0,0.3,0,0.6,0.7,0,0.2], [0,0.5,0.2,0,0,0,0], [0,0.1,0,0.6,0,0,0]], dtype=np.complex128)
        self.acol = np.array([1,2,5,0,5,1,3,4,6,1,2,1,3], dtype=np.int32)
        self.arow = np.array([0,0,0,1,1,2,2,2,2,3,3,4,4], dtype=np.int32)
        self.aval = np.array([0.7,0.6,0.4,0.1,0.1,0.3,0.6,0.7,0.2,0.5,0.2,0.1,0.6], dtype=np.complex128)

    def test_init(self):
        solver1 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        assert_equal(self.n, solver1.n)
        assert_equal(self.m, solver1.m)

    def test_analyze(self):
        solver2 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver2.analyze()
        assert(solver2.analyzed==True)

    def test_factorize(self):
        solver3 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver3.factorize()
        assert(solver3.analyzed==True)
        assert(solver3.factorized==True)

    def test_dense_solve_single_rhs(self):
        solver4 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver4.factorize()
        e = np.ones(self.n, dtype=np.complex128)
        rhs = np.dot(self.A, e)
        x = solver4.solve(rhs)
        assert_almost_equal(np.dot(self.A,x), rhs, 5)

    def test_dense_solve_multiple_rhs(self):
        solver5 = QRMUMPSSolver((self.m, self.n, self.arow, self.acol, self.aval), verbose=False)
        solver5.factorize()
        B = np.ones([self.n, 3], dtype=np.complex128)
        B[: ,1] = 2 * B[:,1]
        B[: ,2] = 3 * B[:,2]
        rhs = np.dot(self.A,B)
        x = solver5.solve(rhs)
        print x
        assert_almost_equal(np.dot(self.A,x), rhs, 5)



if __name__ == "__main__":
      run_module_suite()