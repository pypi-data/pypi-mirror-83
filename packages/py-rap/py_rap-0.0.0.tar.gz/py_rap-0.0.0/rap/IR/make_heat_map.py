def make_heat_map(maindir, Nrange, filename, savedir):
    samples   = ['C3', 'C4', 'C5', 'C6']
    rad_types = ['293 eV', 'BB']

    for sample in samples:
        for rad_type in rad_types:
            df        = pd.DataFrame()
            df[x]     = Nrange
            l         = len(Nrange)

            glob_str = maindir + '*' + sample + '*' + rad_type + '*/'

            for folder in glob.glob(glob_str):
                col     = folder.split(',')[1].split(')')[0]
                df[col] = np.zeros(l)

                df2 = pd.read_excel(folder + 'plots/' + filename,
                                    index_col=0)

                for col2 in df2:
                    df[col][df[x] == col2]= df2[col2].iloc[0]

            df.to_excel('./sheets/Sample ' + sample + ' ' + rad_type + '.xlsx')
            tmp = df.set_index(x)

            if 'BB' in rad_type:
                new = [' 5 s', ' 20 s', ' 1 min', ' 5 min', ' 30 min', ' 2 h']
                tmp = tmp[new]
            else:
                new = [' 1 min', ' 10 min', ' 30 min', ' 3 h', ' 6 h', ' 12 h']
                tmp = tmp[new]

            sb.heatmap(tmp.T, linewidths=.5, cmap='RdYlBu_r', annot=True)

            try:
                os.makedirs(savedir)
            except:
                pass

            plt.title('Sample ' + sample + ' ' + rad_type)
            plt.xticks(np.arange(0.5, l, 1), df[x].values)
            plt.yticks(np.arange(0.5, len(tmp.columns), 1), tmp.columns)
            plt.setp(plt.gca().get_xticklabels(), rotation=65, ha="right",
                     rotation_mode="anchor")
            plt.tight_layout()
            plt.savefig(savedir + 'Sample ' + sample + ' ' + rad_type + '.png')
            plt.close()

    return
