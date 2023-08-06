import paramexplorer as pe
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

def main():
    pe.explore_params(path_to_files = '/Users/jeaadams/klip_thesis/optimizeKLIP/Line_smalltest_sliced',
                    outfile_name = 'test_function6',
                    iwa = 0,
                    klmodes = [1,20],
                    annuli_start = 1,
                    annuli_stop = 2,
                    annuli_inc = 1,
                    movement_start = 1,
                    movement_stop = 2,
                    movement_inc = 1,
                    subsections_start = 1,
                    subsections_stop = 1,
                    subsections_inc=1,
                    FWHM = 5, 
                    smooth = 0,
                    ra = [13],
                    pa = [120],
                    wid = [2,15],
                    input_contrast = 0.04,
                    x_positions = [216],
                    y_positions = [220],
                    saveSNR = True, 
                    singleAnn = False, 
                    highpass = True, 
                    verbose = False)

if __name__ == "__main__":
    main()
                  
                                
                  