def plot_single_spectra(df, x, col, maindir, folder, new_dir):
    df.plot(x, col, color='red', legend=False).invert_xaxis()

    try:
        im_str = make_im_str(col, maindir, folder)
        img    = plt.imread(glob.glob(im_str)[0])
    except:
        catch_fail(col, im_str, folder)

    low    = min(df[col]) - 5
    hi     = max(df[col]) + 5
    plt.imshow(img, extent=[675,4000,low,hi], aspect='auto')


    rec = make_rectanlge(hi, low, 'darkviolet')
    ax  = plt.gca()
    ax.add_patch(rec)

    plt.xlabel(r'Wavenumber ($cm^{-1}$)')
    plt.ylabel('Transmission (%)')
    plt.title(folder + ' ' + col)
    plt.savefig(new_dir + col + '.png')
    plt.close()
    return
