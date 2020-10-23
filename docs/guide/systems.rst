==============
Qiskit systems
==============

Overview
========

The Qiskit services module in kaleidoscope allows one to quickly and easily
access the quantum systems from IBM Quantum.  Here we show how to use the
``Systems`` class.

.. jupyter-execute::

    from kaleidoscope.qiskit import Systems


The ``Systems`` class contains all the information about the devices you have access to.
Qiskit allocates quantum systems via "providers".  A provider is just a way of organizing 
who has access to what systems, and the feature sets of those systems, e.g. pulse access.
The ``Systems`` class has the notion of a default provider, and if you have more than one,
then ``ALL`` providers as well.  Since everyone has access to the open-access quantum systems,
kaleidoscope starts with that as the default provider unless set otherwise.  To see all the
systems in the default provider, simply call the ``Systems`` class:


.. jupyter-execute::

    Systems()

To grab a specific system by name simply do:

.. jupyter-execute::

    Systems('ibmq_vigo')

The systems can also be accessed via autocompletion:

.. jupyter-execute::

    Systems.ibmq_vigo𖼯5Q𖼞

where the system identifier also includes the number of qubits.


Filtering systems
=================

It is also possible to filter systems in a variety of ways that currently includes:

- ``num_qubits`` - The number of qubits
- ``open_pulse`` - Whether the system has pulse access (boolean).
- ``quantum_volume`` - Filter based on the reported Quantum Volume.
- ``operational`` - Is the system currently operational (boolean).
- ``max_circuits`` - The maximum number of circuits that can be submitted in one job.
- ``max_shots`` - The maximum number of shots that can be performed on a circuit.

For example, lets find all systems in the default provider with Quantum Volume 16 or greater:

.. jupyter-execute::

    Systems.quantum_volume >= 16


Or all pulse capable systems of more than 5 qubits:

.. jupyter-execute::

    Systems.open_pulse.num_qubits > 5


Notice how the boolean filter ``open_pulse`` can be immediately called upon by another filter.
This could also be written as:

.. jupyter-execute::

    Systems.open_pulse & (Systems.num_qubits > 5)


``ALL`` systems
===============

If the users has more than one provider available to them, then the ``Systems`` class has an
``ALL`` attribute that allows for searching over all providers.  For example, lets get the
`ibmq_vigo` device from a different provider:

.. jupyter-execute::

    Systems.ALL.get_ibmq_vigo𖼯5Q𖼞.ibmーq_open_main


Here the ``get_ibmq_vigo𖼯5Q𖼞`` class contains the system instance from all available providers.

It is also possible t:o search ``ALL`` just like we did before.  All systems from every provider
are obtained using:

.. code-block:: python

    Systems.ALL()


Or a specific system from all providers is:

.. jupyter-execute::

    Systems.ALL('ibmq_rome')


You can also query for more than one system by name:

.. jupyter-execute::

    Systems.ALL(['ibmq_rome', 'ibmq_santiago'])


It is also possible to query by ``hub``, ``group``, and ``project``, but these are more specific use cases.



Changing the default provider
=============================

To view and/or change the default provider you must use the ``Account`` object:

.. jupyter-execute::

    from kaleidoscope.qiskit import Account

To get the current default provider:

.. jupyter-execute::
    
    Account.get_default_provider()


To change the default provider we use ``Account.set_default_provider``.  One can pass in the 
``hub``, ``group``, and ``project`` as keyword arguments.  However, it is often easier to
use a shortcut.  Consider the following,  I want to set the default provider to the open access
provider.  To do this, I can simply grab a system from the open provider:


.. jupyter-execute::

    open_vigo = Systems.ALL.get_ibmq_vigo𖼯5Q𖼞.ibmーq_open_main
    Account.set_default_provider(open_vigo.provider, overwrite=True)

I also need to set ``overwrite=True`` to overwrite the current default provider.

Upon doing so, we see that the default systems in ``Systems`` are automatically updated:


.. jupyter-execute::

    Systems()

Finally we set it back the old-fashion way:


.. jupyter-execute::

    open_vigo = Systems.ALL.get_ibmq_vigo𖼯5Q𖼞.ibmーq_open_main
    Account.set_default_provider(hub='ibm-q-internal',
                                 group='deployed',
                                 project='default', overwrite=True)
