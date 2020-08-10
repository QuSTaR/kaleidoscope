==============
Saving figures
==============

All interactive figures have wrappers provide an interface for saving to
images that is similar to Matplotlib (i.e. ``savefig()``):

.. jupyter-execute::

    from qiskit import QuantumCircuit
    import kaleidoscope.qiskit
    from kaleidoscope.interactive import bloch_disc

    qc = QuantumCircuit(1)
    qc.h(0)
    qc.tdg(0)

    state = qc.statevector()

    fig = bloch_disc(state)
    fig.savefig('bloch_disc.png')


The figure size (in pixels rather than inches as in MPL), and transparency can also be set.
In addition, for formats like ``png`` the ``scale`` parameter can be set to increase the
physical resolution.

.. jupyter-execute::

    fig.savefig('bloch_disc.png', figsize=(800,600), scale=3, transparent=True)


Exporting as other formats
==========================

Because :class:`kaleidoscope.interactive.plotly_wrapper.PlotlyFigure` and
:class:`kaleidoscope.interactive.plotly_wrapper.PlotlyWidget` are wrappers over their
Plotly counterparts, all of the original functionality still exists.  The
wrappers have the original figure instance as the attribute ``PlotlyFigure._fig``,
which can be used to do things like write an image to HTML:

.. jupyter-execute::

    fig._fig.write_html('bloch_disc.html')
