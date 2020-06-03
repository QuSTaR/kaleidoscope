# -*- coding: utf-8 -*-

# This code is part of Kaleidoscope.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Interactive plotting utility functions"""

import numpy as np
import scipy.sparse as sp
from numba import vectorize, uint32, int32, complex128, jit, prange

@vectorize([uint32(uint32)], target='parallel', nopython=True, cache=True)
def count_set_bits(val):
    """Computes the number of set bits in a uint32 value.

    Parameters:
        val (uint32): Input unsigned int.

    Returns:
        uint32: Output unsigned int.
    """
    val = (val & 0x55555555) + ((val >> 1) & 0x55555555)
    val = (val & 0x33333333) + ((val >> 2) & 0x33333333)
    val = (val & 0x0f0f0f0f) + ((val >> 4) & 0x0f0f0f0f)
    val = (val & 0x00ff00ff) + ((val >> 8) & 0x00ff00ff)
    val = (val & 0x0000ffff) + ((val >> 16) &0x0000ffff)
    return val

@jit(complex128(complex128[:], int32[:], int32[:], complex128[:]),
     nopython=True, cache=True)
def expect_psi_csr(data, ind, ptr, vec):
    """Computes the expectation value of a complex matrix in CSR sparse format.

    Note that this routine returns a complex type regardless of whether
    the matrix is Hermitian or not.  If so, take the real part.

    Parameters:
        data (ndarray): A complex128 array of data.
        ind (ndarray): A int32 array of indices.
        ptr (ndarray): A int32 array of indptrs.
        vec (ndarray): A complex128 array for the statevector.

    Returns:
        complex: A complex number representing the expectation value.
    """
    nrows = vec.shape[0]
    expt = 0
    for row in prange(nrows):  # pylint: disable=not-an-iterable
        cval = np.conj(vec[row])
        temp = 0
        for jj in range(ptr[row], ptr[row+1]):
            temp += data[jj]*vec[ind[jj]]
        expt += cval*temp
    return expt

def sparse_pauli(num_qubits, idx, kind):
    """Returns a sparse CSR pauli matrix.

    Parameters:
        num_qubits (int): The number of qubits in the statevector.
        idx (int): The index (qubit) on which the Pauli acts.
        kind (str): The kind of Pauli, 'X', 'Y', or 'Z'.

    Returns:
        csr_matrix: A Pauli operator as a sparse CSR matrix.

    Raises:
        ValueError: Invalid 'kind' given.
    """
    if kind == 'X':
        x = 1
        z = 0
    elif kind == 'Y':
        x = 1
        z = 1
    elif kind == 'Z':
        x = 0
        z = 1
    else:
        raise ValueError("kind must be 'X', 'Y', or 'Z'.")
    n = 2**num_qubits
    xs = 2**idx if x else 0
    zs = 2**idx if z else 0
    rows = np.arange(n+1, dtype=np.uint32)
    columns = rows ^ xs
    global_factor = (-1j)**(x*z)
    data = global_factor*(-1)**np.mod(count_set_bits(zs & rows), 2)
    return sp.csr_matrix((data, columns, rows), shape=(n, n))


def bloch_components(rho):
    """Computes the Bloch components of a given statevector or density matrix.

    Parameters:
        rho (ndarray): Input statevector (1D) or density matrix (2D) array.

    Returns:
        list: List of [x,y,z] Bloch components for each qubit in the system.

    Raises:
        ValueError: Invalid input state.
    """
    dim_error = ValueError('Invalid input state.')
    num = np.log2(rho.shape[0])
    if num % 1:
        raise dim_error
    if len(rho.shape) == 2:
        if np.log2(rho.shape[1]) % 1:
            raise dim_error
    num = int(num)
    dims = len(rho.shape)

    out = []
    for i in range(num):
        pauli_singles = [
            sparse_pauli(num, i, 'X'),
            sparse_pauli(num, i, 'Y'),
            sparse_pauli(num, i, 'Z')
        ]
        if dims == 1:
            out.append(list(
                map(lambda x: np.real(expect_psi_csr(x.data, x.indices, x.indptr, rho)),
                    pauli_singles)))

        else:
            out.append(list(
                map(lambda x: np.real(np.trace(x.dot(rho))),
                    pauli_singles)))

    return out
