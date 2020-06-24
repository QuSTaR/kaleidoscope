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
   system_error_map(backend, as_widget=True)


Error map from backend properties
---------------------------------

.. jupyter-execute::

   import datetime
   # Grab ibmq_vigo properties on Jan. 1, 2020.
   old_props = backend.properties(datetime=datetime.datetime(2020, 1, 1))
   system_error_map(old_props, as_widget=True)