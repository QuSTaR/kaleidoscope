=============
Installation
=============

Overview
--------

Kaleidoscope requires Python 3.6 or later and a Jupyter notebook environment.  Much of the
functionality also requires having Qiskit a
`IBM Quantum Experience <https://quantum-computing.ibm.com/>`_ account in order to access the
`IBM quantum systems <https://quantum-computing.ibm.com/docs/cloud/backends/systems/>`_.

Install
-------

Installation is simple:

.. code-block:: bash

   pip install kaleidoscope

Or if your adventurous you can install from `source code on Github <https://github.com/nonhermitian/kaleidoscope>`_.


Running in Jupyter Lab
~~~~~~~~~~~~~~~~~~~~~~

Running Kaleidoscope, and Plotly in general, in the Jupyter Lab environment requires
some `additional extensions to be installed <https://plotly.com/python/getting-started/>`_.


Qiskit functionality
--------------------

Although not necessary for many of the interactive visualizations, functionality that makes use
of Qiskit and the IBM Quantum devices requires the following installations:

.. code-block:: bash

   pip install qiskit-terra>=0.14
   pip install qiskit-ibmq-provider>=0.7