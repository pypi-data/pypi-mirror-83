def plot_peak_heights():
    for file in os.listdir('./sheets/'):
        if 'Peak Heights' not in file:
            continue
        df = pd.read_excel('./sheets/'+file, index_col=0)
        df.plot()
        plt.savefig('./plots/'+file.replace('.xlsx', '.png'))
        plt.close()
    return
