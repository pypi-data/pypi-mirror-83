def plot_peak_counts(data, new_dir):
    df = pd.read_excel(data, index_col=0)
    df.stack().plot.hist(bins=1750, legend=False)
    plt.savefig(new_dir+'Histogram.png')
    plt.close()
    df.stack().plot.kde(legend=False)
    plt.savefig(new_dir+'KDE.png')
    plt.close()
    return
