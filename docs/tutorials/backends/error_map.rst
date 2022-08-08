#########
Error map
#########

.. jupyter-execute::

   from qiskit import IBMQ
   IBMQ.load_account()
   from kaleidoscope.qiskit.backends.interactive import system_error_map


Error map from backend instance
-------------------------------

.. jupyter-execute::

   pro = IBMQ.get_provider(group='open')
   backend = pro.backends.ibmq_lima
   system_error_map(backend)


Error map from backend properties
---------------------------------

.. jupyter-execute::

   import datetime
   # Grab ibmq_lima properties on Jan. 1, 2020.
   old_props = backend.properties(datetime=datetime.datetime(2020, 1, 1))
   system_error_map(old_props)


Change colormap
---------------

.. jupyter-execute::

   from kaleidoscope.qiskit import system_error_map
   from matplotlib.cm import cividis

   backend = pro.backends.ibmq_santiago
   system_error_map(backend, colormap=cividis)
