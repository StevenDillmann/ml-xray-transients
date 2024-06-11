import matplotlib.pyplot as plt
import numpy as np


def lc_flare(time, counts, bin_size=100, color='k', ecolor='k', fmt='.', capsize=0, markersize=5, lwe=1, fontsize=14, title='', reset_time=True, xlim=None):
    # Truncate leading and trailing zeros
    nonzero_indices = np.nonzero(counts)
    start, end = nonzero_indices[0][0], nonzero_indices[0][-1] + 1

    # Truncate the arrays and adjust start 
    time = time[start:end]
    counts = counts[start:end]
    if reset_time:
        time = time - time[0]

    # Bin the data
    bins = np.arange(0, time[-1]+ bin_size, bin_size)
    indices = np.digitize(time, bins)
    binned_time = np.array([time[indices == i].mean() for i in range(1, len(bins))])
    binned_counts = np.array([counts[indices == i].sum() for i in range(1, len(bins))])

    # Plot the lightcurve
    fig, ax = plt.subplots(figsize=(8.5,5.5))
    ax.plot(binned_time/1000, binned_counts, color='white', label=title)
    ax.errorbar(binned_time/1000, binned_counts, yerr=np.sqrt(binned_counts), fmt=fmt, color=color, ecolor=ecolor, capsize=capsize, markersize=markersize, linewidth=lwe, label=f'{bin_size}s Bins')
    ax.set_xlabel('Time [ks]', fontsize=fontsize)
    ax.set_ylabel('Counts', fontsize=fontsize)
    ax.tick_params(labelsize=fontsize)
    plt.xlim(xlim)
    plt.legend(loc = 'best', fontsize=fontsize)
    plt.show()
    return None

def spec_fit(data, model, resid = None, xlim=[0.5, 11], ylim = [0.00007, 0.1], ylim2 =[-0.06,0.06], color='k', ecolor='k', fmt='.', capsize=0, markersize=5, lw=1.5, lwe=1, fontsize=15):
    
    if resid is None:
        # Plot data and model
        fig, ax = plt.subplots(figsize=(8.5,5.5))
        ax.set_xlabel('Energy [keV]', fontsize=fontsize)
    else:
        # Plot data and model and residuals
        fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8.5,6.5), gridspec_kw={'height_ratios': [5, 2]},sharex=True)
        ax2.axhline(0, color='k', lw=0.6, ls='--')
        ax2.errorbar(resid.x, resid.y, yerr=resid.yerr, fmt=fmt, color=color, ecolor=color, capsize=capsize, markersize=markersize, lw=lwe, label = 'Residuals')
        ax2.set_ylabel('Residuals', fontsize=fontsize)
        ax2.set_xlabel('Energy [keV]', fontsize=fontsize)
        ax2.tick_params(which='both', direction='in', top=True, right=True)
        ax2.tick_params(labelsize=fontsize) 
        ax2.set_xscale('log')
        ax2.set_ylim(ylim2)
        # ax2.legend(fontsize=fontsize)
        for x, y, yerr, xlo, xhi in zip(resid.x, resid.y, resid.yerr, data.xlo, data.xhi):
            ax2.errorbar(x, y, yerr=yerr, xerr=[[x - xlo], [xhi - x]], fmt='none', linewidth=lwe, capsize=capsize, color=color)
        ax.tick_params(which='both', direction='in', top=True, right=True)
    # Plot data and model
    ax.errorbar(data.x, data.y, yerr=data.yerr, fmt=fmt, color=ecolor, ecolor=ecolor, capsize=capsize, markersize=markersize, lw=lwe, label = 'Data')
    for x, y, yerr, xlo, xhi in zip(data.x, data.y, data.yerr, data.xlo, data.xhi):
        ax.errorbar(x, y, yerr=yerr, xerr=[[x - xlo], [xhi - x]], fmt='none', linewidth=lwe, capsize=capsize, color=ecolor)
    ax.plot(model.x, model.y, color=color, lw=lw, label = 'Model')
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_ylabel('Counts/s/keV', fontsize=fontsize)
    ax.tick_params(labelsize=fontsize)
    ax.legend(fontsize=fontsize, loc='upper left')
    ax.set_ylim(ylim)
    plt.xlim(xlim)
    plt.subplots_adjust(hspace=0)
    # plt.tight_layout()
    plt.show()
    return None

def lc_fit(x, y, y_err,model_fit, x_lo, x_hi, hr_results = None, xlim = [0.1, 1000], ylim2 = [-0.5,1.1], color='k', ecolor='k', fmt='.', capsize=0, markersize=5, lw=1.5, lwe=1, fontsize=15):

    if hr_results is None:
        # Plot data and model
        fig, ax = plt.subplots(figsize=(8.5,5.5)) 
        ax.set_xlabel('Time [s]', fontsize=fontsize)
    else:
        # Load HR data
        hr = np.array(hr_results['hr'])
        hr_lo = hr - np.array(hr_results['hr_lo'])
        hr_hi = np.array(hr_results['hr_hi']) - hr
        # Plot data and model and HR
        fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8.5,6.5), gridspec_kw={'height_ratios': [5, 2]},sharex=True)
        ax2.axhline(0, color='k', lw=0.6, ls='--')
        ax2.errorbar(x, hr, yerr=[hr_lo, hr_hi], fmt=fmt, color=color, ecolor=color, capsize=capsize, markersize=markersize, lw=lwe, label='HR')
        ax2.set_ylabel('HR', fontsize=fontsize)
        ax2.set_xlabel('Time [s]', fontsize=fontsize)
        ax2.tick_params(which='both', direction='in', top=True, right=True)
        ax2.tick_params(labelsize=fontsize) 
        ax2.set_xscale('log')
        ax2.set_ylim(ylim2)
        # ax2.legend(fontsize=fontsize)
        for xh, yh, xlo, xhi in zip(x, hr, x_lo, x_hi):
            ax2.errorbar(xh, yh, xerr=[[xh - xlo], [xhi - xh]], fmt='none', linewidth=lwe, capsize=capsize, color=color)
        ax.tick_params(which='both', direction='in', top=True, right=True)
    # Plot data and model
    ax.errorbar(x, y, yerr=y_err, fmt=fmt, color=ecolor, ecolor=ecolor, capsize=capsize, markersize=markersize, lw=lwe, label = 'Data')
    for xm, ym, xlo, xhi in zip(x, y, x_lo, x_hi):
        ax.errorbar(xm, ym, xerr=[[xm - xlo], [xhi - xm]], fmt='none', linewidth=lwe, capsize=capsize, color=ecolor)
    ax.plot(x, model_fit, color=color, lw=lw, label = 'Model')
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_ylabel(r'Flux [ergs/s/$\mathrm{cm^2}$]', fontsize=fontsize)
    ax.tick_params(labelsize=fontsize)
    ax.legend(fontsize=fontsize, loc='upper right')
    plt.xlim(xlim)
    plt.subplots_adjust(hspace=0)
    # plt.tight_layout()
    plt.show()
    return None