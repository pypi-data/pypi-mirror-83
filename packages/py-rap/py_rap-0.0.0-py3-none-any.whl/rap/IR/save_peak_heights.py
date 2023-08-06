def save_peak_heights(maindir):
    samples   = ['C3', 'C4', 'C5', 'C6']
    rad_types = ['293 eV', 'BB']
    index1    = [' 1 min', ' 10 min', ' 30 min', ' 3 h', ' 6 h', ' 12 h']
    index2    = [' 5 s', ' 20 s', ' 1 min', ' 5 min', ' 30 min', ' 2 h' ]
    ranges    = [(2250, 2150, 'Nitrile'), (840, 800, '820'), (780, 740, '760')]
    lol       = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]

    for sample in samples:
        for rad_type in rad_types:
            if '293' in rad_type:
                df = pd.DataFrame({'Nitrile':lol, '820':lol, '760':lol},
                                  index=index1)
            else:
                df = pd.DataFrame({'Nitrile':lol, '820':lol, '760':lol},
                                  index=index2)

            glob_str = maindir + '*' + sample + '*' + rad_type + '*/'

            for folder in glob.glob(glob_str):
                ind = folder.split(',')[1].split(')')[0]
                df2 = pd.read_excel(folder + 'plots/Average.xlsx',
                                    index_col=0)

                for range in ranges:
                    hi, low, col = range

                    df3 = df2[(df2[x] < hi) & (df2[x] > low)]

                    peaks, prom = find_peaks(-df3['Avg'], prominence=0)
                    try:
                        p           = max(prom['prominences'])/2
                    except:
                        p = 0
                    peaks, prom = find_peaks(-df3['Avg'], prominence=p, width=6)

                    if len(prom['prominences']) > 0:
                        h = prom['prominences'][0]
                    else:
                        h = 0

                    df.set_value(ind, col, h)

            df.to_excel('./sheets/Sample ' + sample + ' ' + rad_type +
                        ' Peak Heights.xlsx')
    return
