def subtract_spectra(maindir):
    samples   = ['C3', 'C4', 'C5', 'C6']
    rad_types = ['293 eV', 'BB']

    for sample in samples:
        glob_str = maindir + '*' + sample + ' (Astromix*/*.xlsx'
        df       = pd.read_excel(glob.glob(glob_str)[0], header=2)

        i=0
        for col in df:
            if x in col:
                continue
            try:
                tmp += preprocessing.normalize([df[col]], norm='max')
            except:
                tmp  = preprocessing.normalize([df[col]], norm='max')
            i+=1

        b4_avg = tmp/i
        del(tmp)

        for rad_type in rad_types:
            glob_str = maindir + '*' + sample + '*' + rad_type + '*/'

            for folder in glob.glob(glob_str):
                glob_str = folder + '*.xlsx'
                df2      = pd.read_excel(glob.glob(glob_str)[0], header=2)

                i=0
                for col in df2:
                    if x in col:
                        continue
                    try:
                        tmp2 += preprocessing.normalize([df2[col]], norm='max')
                    except:
                        tmp2  = preprocessing.normalize([df2[col]], norm='max')
                    i+=1

                b5_avg = tmp2/i
                del(tmp2)

                avg    = (b5_avg / b4_avg)

                peaks, prom = find_peaks(-avg[0], prominence=0, distance=2)
                try:
                    p           = max(prom['prominences']) * (10/100)
                except:
                    p = 0
                peaks, _    = find_peaks(-avg[0], prominence=p)
                X           = df[x].values
                Y           = avg[0]

                plt.plot(df[x], avg[0])
                """
                ymin, ymax = plt.gca().get_ylim()
                j = ymax
                for i in X[peaks]:
                    if j < Y[np.where(X == i)]:
                        j = ymax - (ymax - ymin)/15
                    plt.vlines([i], ymin, j, linestyles='--', lw=0.5, color='red')
                    plt.annotate(str(int(round(i,0))), xy=(i, j), xytext=(-15,2.5),
                                 textcoords='offset points')
                    j -= (ymax - ymin)/15
                """

                plt.gca().invert_xaxis()
                plt.xlabel(r'Wavenumber ($cm^{-1}$)')
                plt.ylabel('Transmission (%)')
                plt.title('Sample ' + sample + ' ' + rad_type + ' Subtraction')
                plt.tight_layout()
                plt.savefig(folder + 'plots/Subtraction.png')
                plt.close()
                #sys.exit()
    return
