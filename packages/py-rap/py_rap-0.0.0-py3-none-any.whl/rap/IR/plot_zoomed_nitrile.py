def plot_zoomed_nitrile(df, folder, new_dir):

    for col in df:
        if x in col:
            continue

        df2         = df[(df[x] < 2250) & (df[x] > 2150)]
        df3         = df[(df[x] < 2350) & (df[x] > 2150)]
        peaks, prom = find_peaks(-df2[col], prominence=0)
        try:
            p           = max(prom['prominences'])/2
        except:
            p = 0
        peaks, _    = find_peaks(-df2[col], prominence=p, width=6)
        X           =   df2[x].values
        Y           = df2[col].values

        fig, ax = plt.subplots()
        plt.plot(df[x], df[col])
        plt.gca().invert_xaxis()
        #plt.ylim(top = max(df[df[x] < 1750][col]) + 10 )
        plt.xlabel(r'Wavenumber ($cm^{-1}$)')
        plt.ylabel('Transmission (%)')
        plt.title(folder + ' ' + col + ' Zoom')

        ax2 = inset_axes(ax, width='30%', height=1., loc=1)

        plt.plot(df3[x], df3[col])
        plt.plot(X[peaks], Y[peaks], '|', lw=2.5, color='red')
        for peak in peaks:
            plt.annotate(str(round(X[peak],1)), xy=(X[peak], Y[peak]),
                         xytext=(-15,-15), textcoords='offset points')

        plt.gca().invert_xaxis()
        plt.gca().axes.get_xaxis().set_visible(False)
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.savefig(new_dir + '-' + col + '-Zoom.png')
        plt.close()

    return
