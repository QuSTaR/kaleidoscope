=============
API reference
=============

The Kaleidoscope API is currently broken into two parts:

1.) General interactive figures.

2.) IBM Quantum system plots via Qiskit.

The general interactive figures take generic Python objects as inputs and therefore
will work with any quantum computing framework.  In addition, these functions will also
accept Qiskit classes, where applicable.  Qiskit does not need to be installed to use
these routines.

The IBM Quantum system plots require having Qiskit and an 
`IBM Quantum Experience <https://quantum-computing.ibm.com/>`_
account for use.  Some of these routines mirror functionality
available in Qiskit, but are difficult to use due to complex optional
installation dependencies.  Others are generalized versions of figures
that have been used in various IBM Quantum press releases, presentations,
and other materials.

.. toctree::
  :maxdepth: 1
  :caption: API reference
  :hidden:

  Interactive figures<apidocs/interactive>
  IBM Quantum system visualizations<apidocs/backends>
