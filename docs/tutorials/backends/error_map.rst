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
   backend = pro.backends.ibmq_vigo
   system_error_map(backend)


Error map from backend properties
---------------------------------

.. jupyter-execute::

   import datetime
   # Grab ibmq_vigo properties on Jan. 1, 2020.
   old_props = backend.properties(datetime=datetime.datetime(2020, 1, 1))
   system_error_map(old_props)


Change colormap
---------------

.. jupyter-execute::

   from kaleidoscope.qiskit import system_error_map
   from kaleidoscope.qiskit.services import Systems
   from matplotlib.cm import cividis

   backend = Systems.ibmq_santiago𖼯5Q𖼞
   system_error_map(backend, colormap=cividis)
