def save_peak_location(df, new_dir, savename, Prange):
    vals = []

    if ('Sample C1' in new_dir) or ('Sample C2' in new_dir):
        return

    for col in df:
        if x in col:
            continue

        df2         = df[(df[x] < Prange[0]) & (df[x] > Prange[1])]
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


    c   = Counter(vals)
    df3 = pd.DataFrame(c, index=[0])
    df3.to_excel(new_dir + savename)
    return
