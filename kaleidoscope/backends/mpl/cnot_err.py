import numpy as np
import seaborn as sns
from scipy.stats import gaussian_kde
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt


def cnot_error_density(backends, figsize=None, xlim=None,
                      text_xval=None, xticks=None):
    
    if not isinstance(backends, list):
        backends = [backends]
        
    for back in backends:
        if back.configuration().n_qubits < 2:
            raise ValueError('Number of backend qubits must be > 1')
    
    # Attempt to autosize if figsize=None
    if figsize is None:
        if len(backends) > 1:
            fig = plt.figure(figsize=(12,len(backends)*1.5))
        else:
            fig = plt.figure(figsize=(12,2))

    text_color = 'k'
    offset = -100
    colors = [mpl.colors.rgb2hex(rgb) for rgb in sns.cubehelix_palette(len(backends))[0:]]

    cx_errors = []
    for idx, back in enumerate(backends):

        back_props = back.properties().to_dict()

        cx_errs = []
        meas_errs = []
        for gate in back_props['gates']:
            if len(gate['qubits']) == 2:
                # Ignore cx gates with values of 1.0
                if gate['parameters'][0]['value'] != 1.0:
                    cx_errs.append(gate['parameters'][0]['value'])

        for qubit in back_props['qubits']:
            for item in qubit:
                if item['name'] == 'readout_error':
                    meas_errs.append(item['value'])
        cx_errors.append(np.asarray(cx_errs))
        
    max_cx_err = max([cerr.max() for cerr in cx_errors])
    if xlim is None:
        xlim=[0, max_cx_err+0.02]
        
    if text_xval is None:
        text_xval = 0.8*xlim[1]

    for idx, back in enumerate(backends):
        cx_density = gaussian_kde(cx_errors[idx])
        xs = np.linspace(xlim[0], xlim[1],2000)
        cx_density.covariance_factor = lambda : 0.15
        cx_density._compute_covariance()

        plt.plot(xs,cx_density(xs)+offset*idx, zorder=idx, color=colors[idx])
        plt.fill_between(xs,offset*idx, cx_density(xs)+offset*idx,zorder=idx, color=colors[idx])

    
        qv_val = back.configuration().quantum_volume
        if qv_val:
            qv = "(QV"+str(qv_val)+")"
        else:
            qv = ''

        bname = back.name().split('_')[-1].title()+" {}".format(qv)
        plt.text(text_xval, offset*idx+10, bname, fontsize=20, color=colors[idx])

    fig.axes[0].get_yaxis().set_visible(False)

    # get rid of the frame
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    
    if xticks is None:
        xticks = np.round(np.linspace(xlim[0], xlim[1], 4), 2)
    else:
        xticks = np.asarray(xticks)/100.0
    plt.xticks(xticks, labels=np.ceil(100*xticks),color=text_color, fontsize=20)
    plt.tick_params(axis='x', colors=text_color)
    plt.xlabel('Gate Error (%)', fontsize=18, color=text_color)
    plt.title('CNOT Error Distributions', fontsize=18, color=text_color)
    fig.tight_layout()
    
    if matplotlib.get_backend() in ['module://ipykernel.pylab.backend_inline',
                                    'nbAgg']:
            plt.close(fig)
    return fig