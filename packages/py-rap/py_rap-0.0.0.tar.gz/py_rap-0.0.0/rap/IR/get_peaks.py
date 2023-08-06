def get_peaks(df, h, savename):
    l   = len(df[x].values)
    df2 = pd.DataFrame()

    for col in df:
        if x in col:
            continue
        peaks, _ = find_peaks(-df[col], prominence=h)
        a        = np.full(l, np.nan)
        a[peaks] = df[x][peaks]
        df2[col] = a

    df2 = df2.apply(lambda x: pd.Series(x.dropna().values))
    df2.to_excel(savename)
    return
