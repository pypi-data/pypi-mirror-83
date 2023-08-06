def plot_all_spectra(df, x, folder, new_dir):
    df.plot(x, df.columns[1:]).invert_xaxis()
    plt.xlabel(r'Wavenumber ($cm^{-1}$)')
    plt.ylabel('Transmission (%)')
    plt.title(folder)

    if len(df.columns) >= 10:
        plt.legend(bbox_to_anchor=(1.01, 1), prop={'size':5})
    else:
        plt.legend(bbox_to_anchor=(1.01, 1))

    plt.tight_layout()
    plt.savefig(new_dir + 'All' + '.png')
    plt.close()
    return
