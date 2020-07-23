*************************
Using interactive figures
*************************

Interactive figures are the core of Kaleidoscope.  All interactive figures
use `Plotly <https://plotly.com/python/>`_ as the rendering engine.  However,
to make things a bit easier, all Kaleidoscope figures use wrappers over the 
Plotly `Figure` and `Widget` instances.  Here we explain how to use them.


Figures verses widgets
======================
By default, all plots are displayed as :class:`PlotlyFigure` instances.  For
use in a Jupyter notebook environment this is likely all that you need.  However,
there are often cases where you want the Javascript widget to remain interactive
after converting the notebook to a different format, e.g. Sphinx documentation, or to
automatically instantiate when a notebook is reloaded.  To do this, each interactive
figure has a `as_widget` keyword argument that returns a :class:`PlotlyWidget` that
can be rendered inside of documentation or persist when a notebook is saved and reloaded.

For example, the following two figures both work in a Jupyter notebook, but only the
second renders in this documentation:


.. jupyter-execute::

    from qiskit import QuantumCircuit
    import kaleidoscope.qiskit
    from kaleidoscope.interactive import bloch_disc
    
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.tdg(0)

    state = qc.statevector()
    bloch_disc(state)


.. jupyter-execute::

    bloch_disc(state, as_widget=True)

To embed the widget inside a notebook so that it reloads in the future, from the
notebook menu do:``Widgets -> Save Notebook Widget State``.


Saving figures and widgets
===========================

The wrappers provide an interface for saving to images that is similar to Matplotlib:

.. jupyter-execute::

    fig = bloch_disc(state)
    fig.savefig('bloch_disc.png')


The figure size (in pixels), and transparency can also be set.  In addition, for
formats like ``png`` the ``scale`` parameter can be set to increase the physical
resolution.

.. jupyter-execute::

    fig.savefig('bloch_disc.png', figsize=(800,600), scale=3, transparent=True)


Exporting as other formats
==========================
Because :class:`PlotlyFigure` and :class:`PlotlyWidget` are simple wrappers over their
Plotly counterparts, all of the original functionality still exists.  For example,
to export a figure as HTML.
