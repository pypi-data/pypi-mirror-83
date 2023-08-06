def plot_average_spectra(df, folder, new_dir):

    i=0
    for col in df:
        if x in col:
            continue
        try:
            tmp += preprocessing.normalize([df[col]], norm='max')
        except:
            tmp  = preprocessing.normalize([df[col]], norm='max')
        i+=1

    avg = tmp/i

    peaks, prom = find_peaks(-avg[0], prominence=0, distance=2)
    try:
        p           = max(prom['prominences']) * (5/100)
    except:
        p = 0
    peaks, _    = find_peaks(-avg[0], prominence=p)
    X           = df[x].values
    Y           = avg[0] *100

    tmp = pd.DataFrame({x:X, 'Avg':Y})
    tmp.to_excel(new_dir + 'Average.xlsx')

    plt.plot(df[x], avg[0]*100)
    ymin, ymax = plt.gca().get_ylim()
    j = ymax
    for i in X[peaks]:
        if j < Y[np.where(X == i)]:
            j = ymax - (ymax - ymin)/15
        plt.vlines([i], ymin, j, linestyles='--', lw=0.5, color='red')
        plt.annotate(str(int(round(i,0))), xy=(i, j), xytext=(-15,2.5),
                     textcoords='offset points')
        j -= (ymax - ymin)/15

    plt.gca().invert_xaxis()
    plt.xlabel(r'Wavenumber ($cm^{-1}$)')
    plt.ylabel('Transmission (%)')
    plt.title(folder + ' Average')
    plt.tight_layout()
    plt.savefig(new_dir + 'Average.png')
    plt.close()
    return
