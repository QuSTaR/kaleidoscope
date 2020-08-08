#########
Gate map
#########

.. jupyter-execute::

   from qiskit import IBMQ
   IBMQ.load_account()
   from kaleidoscope.qiskit.backends.interactive import system_gate_map


Gate map from backend instance
-------------------------------

.. jupyter-execute::

   pro = IBMQ.get_provider(group='open')
   backend = pro.backends.ibmq_vigo
   system_gate_map(backend)


Gate map qubit labels
---------------------

.. jupyter-execute::

   system_gate_map(backend, qubit_labels=['A', 'B', 'C', 'D', 'E'])


Gate map qubit color
---------------------

.. jupyter-execute::

   system_gate_map(backend,
                qubit_labels=['A', 'B', 'C', 'D', 'E'],
                qubit_colors='#8b7b8b')


Gate map qubit colors as list
-----------------------------

.. jupyter-execute::

   system_gate_map(backend,
                qubit_labels=['A', 'B', 'C', 'D', 'E'],
                qubit_colors=['#8b7b8b', '#845e49', '#496b3a', '#e97fa5', '#ff9999'])


Gate map qubit and line colors
------------------------------

.. jupyter-execute::

   system_gate_map(backend,
                qubit_colors='#8b7b8b',
                line_colors='#ff9999')


Gate line colors as list
------------------------
**Must be careful that list is same length as coupling map**

.. jupyter-execute::

   system_gate_map(backend,
                line_colors=['#845e49', '#496b3a', '#e97fa5', '#ff9999']*2)


Disable qubit labels
--------------------

.. jupyter-execute::

   system_gate_map(backend, label_qubits=False)


Make gate map for black background
----------------------------------

.. jupyter-execute::

   system_gate_map(backend,
                   qubit_colors='white',
                   font_color="black",
                   line_colors='white',
                   background_color='black')