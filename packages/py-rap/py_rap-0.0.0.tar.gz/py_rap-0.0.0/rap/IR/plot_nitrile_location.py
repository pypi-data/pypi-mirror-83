def plot_nitrile_location(df, new_dir):
    vals = []

    for col in df:
        if x in col:
            continue

        df2         = df[(df[x] < 2250) & (df[x] > 2150)]
        X           =   df2[x].values
        peaks, prom = find_peaks(-df2[col], prominence=0)

        try:
            p           = max(prom['prominences'])/2
        except:
            p = 0
        peaks, _    = find_peaks(-df2[col], prominence=p, width=6)

        try:
            vals.append(X[peaks[0]])
        except:
            pass


    c    = Counter(vals)
    plt.bar(c.keys(), c.values())
    plt.xticks(list(c.keys()))
    plt.savefig(new_dir + 'Nitrile-Location.png')
    plt.close()

    df3 = pd.DataFrame(c, index=[0])
    df3.to_excel(new_dir + 'Nitrile-Location.xlsx')
    return
