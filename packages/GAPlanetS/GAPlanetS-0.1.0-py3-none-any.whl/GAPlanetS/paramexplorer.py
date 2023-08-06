import glob
import inspect
import os
import pyklip.instruments.MagAO as MagAO
import pyklip.parallelized as parallelized
import numpy as np
import sys
import pyklip.klip as klip
from astropy.io import fits
import SNRMap_new as snr
import time
import warnings
import pyklip.fakes as fakes
import pdb
from astropy.utils.exceptions import AstropyWarning
from tqdm import tqdm

warnings.filterwarnings('ignore', category=AstropyWarning, append=True)



def explore_params(path_to_files, outfile_name, iwa, klmodes, annuli_start, annuli_stop, annuli_inc, movement_start, movement_stop, movement_inc, subsections_start, subsections_stop, subsections_inc, FWHM, smooth, ra, pa, wid, input_contrast, x_positions, y_positions, saveSNR = True, singleAnn = False, highpass = True, verbose = False):

    # Make function to write out data 

    def writeData(im, prihdr, allParams = False, snrmap = False, pre = ''):
        #function writes out fits files with important info captured in fits headers
        
        if (allParams):
        #for parameter explorer cube output - capture full range of parameter values
            annuli_fname = annuli
            annuli_head = annuli
            movement_fname = movement
            movement_head = movement
            subsections_fname = subsections
            subsections_head = subsections
           
            #if program iterates over several parameter values, formats these for fits headers and file names
            if (isinstance(annuli, tuple)):
                annuli_fname = str(annuli[0]) + '-' + str(annuli[1]) + 'x' + str(annuli[2])
                annuli_head = str(annuli[0]) + 'to' + str(annuli[1]) + 'by' + str(annuli[2])  
            if (isinstance(movement, tuple)):
                movement_fname = str(movement[0]) + '-' + str(movement[1]) + 'x' + str(movement[2])
                movement_head = str(movement[0]) + 'to' + str(movement[1]) + 'by' + str(movement[2])
            if (isinstance(subsections, tuple)):
                subsections_head = str(subsections[0]) + 'to' + str(subsections[1]) + 'by' + str(subsections[2])
                subsections_fname = str(subsections[0]) + '-' + str(subsections[1]) + '-' + str(subsections[2])
        else:
            #for individual images and SNR maps, capture the single parameter values used
            annuli_head = a
            movement_head = m
            subsections_head = s
            annuli_fname = a
            movement_fname = m
            subsections_fname = s
    
        #shortens file path to bottom 4 directories so it will fit in fits header
        try:
            path_to_files_short = '/'.join(path_to_files.split(os.path.sep)[-4:])
        except:
            path_to_files_short = path_to_files
                
        #adds info to fits headers
        prihdr['ANNULI']=str(annuli_head)
        prihdr['MOVEMENT']=str(movement_head)
        prihdr['SUBSCTNS']=str(subsections_head)
        prihdr['IWA'] = str(iwa)
        prihdr['KLMODES']=str(klmodes)
        prihdr['FILEPATH']=str(path_to_files_short)
     
        if(snrmap):
            rad, pa, wid = mask 
            prihdr['MASK_RAD']=str(rad)
            prihdr['MASK_PA']=str(pa)
            prihdr['MASK_WID']=str(wid)
            prihdr['SNRSMTH']=str(smooth)
            prihdr['SNRFWHM']=str(FWHM)
    
        if(allParams):
            prihdr["SLICE1"]="average planet peak value under mask in standard deviation noise map"
            prihdr["SLICE2"] = "average planet peak value under mask in median absolute value noise map"
            prihdr["SLICE3"] = "average value of positive pixels under mask in standard deviation noise map"
            prihdr["SLICE4"] = "average value of positive pixels under mask in median absolute value noise map"
            prihdr["SLICE5"] = "total number of pixels >5sigma outside of mask in standard deviation noise map"
            prihdr["SLICE6"] = "total number of pixels >5sigma outside of mask in median absolute value noise map"
            prihdr["SLICE7"] = "total number of pixels >5sigma outside of mask and at similar radius in standard deviation noise map"
            prihdr["SLICE8"] = "total number of pixels >5sigma outside of mask and at similar radius in median absolute value noise map"
    

    
        #writes out files
        fits.writeto(str(path_to_files) + "_klip/" + str(pre)  + outfile_name + "_a" + str(annuli_fname) + "m" + str(
            movement_fname) + "s" + str(subsections_fname) + "iwa" + str(iwa) + suff + '_klmodes-all.fits', im, prihdr, overwrite=True)

        return
    
    if verbose is True:
        print(f"File Path = {path_to_files}")   
        print()
        print(f"Output Filename = {outfile_name}")
        print("Parameters to explore:")
        print(f"Annuli: start = {annuli_start}; end = {annuli_stop}; increment = {annuli_inc}")
        print(f"Subsections: start = {subsections_start}; end = {subsections_stop}; increment = {subsections_inc} ")
        print(f"Movement: start = {movement_start}; end = {movement_stop}; increment = {movement_inc} ")
        print(f"IWA = {iwa}, KL Modes = {klmodes}, FWHM = {FWHM}, Smoothing Value = {smooth}")
        print()
        print("Planet Parameters")
        print(f"Radius= {ra}, Position Angle = {pa}, Mask Width = {wid}, Input Contrast - {input_contrast}, X Positions = {x_positions}, Y Positions = {y_positions} ")
        print()
        print("reading: " + path_to_files + "/*.fits")

    # create directory to save ouput to
    if not os.path.exists(path_to_files + "_klip"):
        os.makedirs(path_to_files + "_klip")
    
   
    # create tuples for easier eventual string formatting when saving files
    annuli = (annuli_start, annuli_stop, annuli_inc)
    movement = (movement_start, movement_stop, movement_inc)
    subsections = (subsections_start, subsections_stop, subsections_inc)

    # if only one parameter is iterated over, makes sure increment is 1 and changes touple to single int
    if(annuli_start == annuli_stop):
        annuli_inc = 1
        annuli = annuli_start
   
    # if parameter is not set to change, makes sure increment is 1 and changes touple to single int
    if(movement_start == movement_stop):
        movement_inc = 1
        movement = movement_start

    # if parameter is not set to change, makes sure increment is 1 and changes touple to single int
    if(subsections_start == subsections_stop):
        subsections_inc = 1
        subsections = subsections_start

    # check that position angle and radius lists have the same number of elements
    if len(ra) != len(pa):
        print("List of separations is not equal in length to list of position angles. Duplicating to match.")
        ra=np.repeat(ra,len(pa))
    
    # Add suffix to filenames depending on user-specified values
    suff = ''    
    if singleAnn is True:
        suff += '_min-annuli'
    
    if highpass is True:
        suff += '_highpass'
    
    # object to hold mask parameters for snr map 
    mask = (ra, pa, wid)
                    
    
    print("Reading: " + path_to_files + "/*.fits")
    
    start_time = time.time()
    print("Start clock time is", time.time())
    
    start_process_time = time.process_time()
    print("Start process time is", time.process_time())
    

    
    # grab generic header from a generic single image
    hdr = fits.getheader(path_to_files + '/sliced_1.fits')

    # erase values that change through image cube
    del hdr['ROTOFF']
    try:
        del hdr['GSTPEAK']
    except:
        print('not a saturated dataset')
    del hdr['STARPEAK']
    
    
    # reads in files

    filelist = glob.glob(path_to_files + '/*.fits')

    # Get star peaks
    starpeak = []
    for i in np.arange(len(filelist)):
        head = fits.getheader(filelist[i])
        starpeak.append(head["STARPEAK"])

    dataset = MagAO.MagAOData(filelist)
    
    # set IWA and OWA
    dataset.IWA = iwa
    xDim = dataset._input.shape[2]
    yDim = dataset._input.shape[1]
    owa = min(xDim,yDim)/2

    nplanets = len(x_positions)
    
    # create cube to eventually hold parameter explorer data
    PECube = np.zeros((9+nplanets,int((subsections_stop-subsections_start)/subsections_inc+1), len(klmodes),
                        int((annuli_stop-annuli_start)/annuli_inc+1),
                        int((movement_stop-movement_start)/movement_inc+1)))
    
    # BEGIN LOOPS OVER ANNULI, MOVEMENT AND SUBSECTION PARAMETERS
    
    # used for indexing: keeps track of number of annuli values that have been tested
    acount = 0
    
    for a in range(annuli_start, annuli_stop+1, annuli_inc):
    
        # calculate size of annular zones
        dr = float(owa-iwa)/a

        # creates list of zone radii
        all_bounds = [dr*rad+iwa for rad in range(a+1)]

        # print('annuli bounds are', all_bounds)
        numAnn = a
        
        if(singleAnn):
            #find maximum annulus boundary radius that is still inside innermost planet injection radius
            lowBound = max([b for b in all_bounds if (min(ra)>b)])
            #find minimum exterior boundary radius that is outside outermost planet injection radius
            upBound = min([b for b in all_bounds if (max(ra)<b)])
            #list of zone boundaries for planets between the two bounds
            all_bounds = [b for b in all_bounds if (b>=lowBound and b<=upBound)]
            numAnn = int(round((upBound-lowBound)/dr))
            #reset iwa and owa to correspond to annulus
            dataset.IWA = lowBound
            dataset.OWA = upBound
    
        #check to see if any planets fall very close to a zone boundary 
        #if (len( [b for b in all_bounds for r in ra if(b <= r+FWHM/2 and b >= r-FWHM/2)] ) == 0):
    
        # used for indexing: keeps track of number of movement values that have been tested
        mcount = 0
    
        for m in tqdm(np.arange(movement_start, movement_stop+1, movement_inc)):
    
            scount = 0
    
            for s in range(subsections_start, subsections_stop+1, subsections_inc):

                if verbose is True:  
                    if(singleAnn):
                        print("Parameters: movement = %s; subections = %d" %(m,s))
                        print("Running for %d annuli, equivalent to single annulus of width %s pixels" %(annuli_start+acount, dr))
                    else:
                        print("Parameters: annuli = %d; movement = %s; subections = %d" %(a, m,s))
        
                    # create cube to hold snr maps 
                    #snrMapCube = np.zeros((2,len(klmodes),yDim,xDim))
    
                runKLIP = True
    
                if (os.path.isfile(str(path_to_files) + "_klip/med_" + outfile_name + "_a" + str(a) + "m" + str(m) + "s" + str(s) + "iwa" + str(iwa) + suff + '_klmodes-all.fits')):
                    incube = fits.getdata(str(path_to_files) + "_klip/med_" + outfile_name + "_a" + str(a) + "m" + str(m) + "s" + str(s) + "iwa" + str(iwa) + suff + '_klmodes-all.fits')
                    head = fits.getheader(str(path_to_files) + "_klip/med_" + outfile_name + "_a" + str(a) + "m" + str(m) + "s" + str(s) + "iwa" + str(iwa) + suff + '_klmodes-all.fits')
                    klmodes2 = head['KLMODES'][1:-1]
                    klmodes2 = list(map(int, klmodes2.split(",")))
    
                    if (len([k for k in klmodes if not k in klmodes2]) == 0):
                        print("Found KLIP processed images for same parameters saved to disk. Reading in data.")
                        #don't re-run KLIP
                        runKLIP = False
    
                if (runKLIP):
                    if verbose is True:
                        print("Starting KLIP")
                    #run klip for given parameters
                    parallelized.klip_dataset(dataset, outputdir=(path_to_files + "_klip/"), fileprefix=f"{outfile_name}_a{numAnn}_m{m}", 
                        annuli=numAnn, subsections=s, movement=m, numbasis=klmodes, calibrate_flux=True, 
                        mode="ADI", highpass = highpass, time_collapse='median', verbose = verbose)

                    
                    #collapse in time dimension
                    incube = np.nanmedian(dataset.output, axis=1)
                    #truncates wavelength dimension, which we don't use
                    incube = incube[:,0,:,:]
                    #print('check: input image shape goes from', dataset.output.shape, 'to', incube.shape)
                    #pdb.set_trace()

                    dataset_copy = np.copy(incube)
                    
                    # Collapse in KL dimension
                    # dataset_copy = np.nanmedian(dataset_copy, axis = 0)
                    # Loop through kl modes
                    cont_meas = np.zeros((len(klmodes), 1))
                    for k in range(len(klmodes)):
                    
                        dataset_contunits = dataset_copy[k]/np.median(starpeak)
                            
                        # Retrieve flux of injected planet
                        planet_fluxes = []
                        for sep, p in zip(ra, pa):
                            fake_flux = fakes.retrieve_planet_flux(dataset_contunits, dataset.centers[0], dataset.output_wcs[0], sep, p, searchrad=7)
                            planet_fluxes.append(fake_flux)

                    
                        # Calculate the throughput
                        tpt = np.array(planet_fluxes)/np.array(input_contrast)
                        
        
                        # Create an array with the indices are that of KL mode frame with index 2
                        ydat, xdat = np.indices(dataset_contunits.shape)

                        # Mask the planets
                        for x, y in zip(x_positions, y_positions):

                            # Create an array with the indices are that of KL mode frame with index 2
                            distance_from_star = np.sqrt((xdat - x) ** 2 + (ydat - y) ** 2)

                            # Mask
                            dataset_contunits[np.where(distance_from_star <= 2 * FWHM)] = np.nan

                            masked_cube = dataset_contunits

                        # Measure the raw contrast
                        contrast_seps, contrast = klip.meas_contrast(dat=masked_cube, iwa=iwa, owa=dataset.OWA, resolution=(7), center=dataset.centers[0], low_pass_filter=True)

                        # Find the contrast to be used 
                        use_contrast = np.interp(np.median(ra), contrast_seps, contrast)
                        

                        # Calibrate the contrast
                        cal_contrast = use_contrast/np.median(tpt)
                        cont_meas[k] = -cal_contrast
                        

                    
                #list of noise calculation methods
                methods = ['stddev', 'med']
    
                    # makes SNR map
                snrmaps, peaksnr, snrsums, snrspurious= snr.create_map(incube, FWHM, smooth=smooth, planets=mask, saveOutput=False)
                    
                    # compute contrast here!!!



                    #print(snrmaps.shape,peaksnr.shape,snrsums.shape,snrspurious.shape,PECube.shape)
    
                    #klmode index
                    #kcount = 0
                    # iterates over kl modes
                    #for k in klmodes:
                        #for methodctr in np.arange(2):
                            #loops over planets specified and returns their SNRs
                         #   planetSNRs = [snr.getPlanet_peak(snrmaps[methodctr,kcount,:,:], ra[x], pa[x], int(FWHM / 2) + 1) for x in range(len(ra))]
                            #print("planet SNRs are", planetSNRs, 'for', methods[methodctr])
                          #  planetSNR = np.nanmedian(planetSNRs)
                           # print(planetSNR)
                            #print("average planet SNR is", planetSNR, 'for', methods[methodctr])
    
                            #adds peak values from getPlanet_peak to PE cube first two slices of PE cube
                           # PECube[methodctr,scount,kcount,acount,mcount] = planetSNR
                        #kcount+=1
                        # adds sums under mask from snr.create_map to PE cube
                PECube[0:2, scount, :, acount, mcount] = np.nanmedian(peaksnr, axis=2)
                PECube[2:4, scount, :, acount, mcount] = np.nanmedian(snrsums, axis=2)
                PECube[4:6, scount, :, acount, mcount] = snrspurious[:,:,0]
                PECube[6:8, scount, :, acount, mcount] = snrspurious[:,:,1]
                PECube[8, scount, :, acount, mcount] = cont_meas[:,:]

                for p, r in zip(range(nplanets), ra):
                
                    p_cont = np.interp(r, contrast_seps, contrast)
                    
                    cal_cont = p_cont/tpt[p]
                    PECube[8+p+1, scount, :, acount, mcount] = -cal_cont

                
                
    
                if(runKLIP) and np.nanmedian(peaksnr)>3:
                    writeData(incube, hdr, pre = 'med_')
                if verbose is True:
                    print("Median peak SNR > 3. Writing median image combinations to " + path_to_files + "_klip/")
                    
                if saveSNR is True:
                    writeData(snrmaps, hdr, snrmap = True, pre = 'snrmap_')
                    if verbose is True:
                        print("Writing SNR maps to " + path_to_files + "_klip/")
    
                scount+=1
            mcount+=1
    
        #else: 
         #   print("Planet near annulus boundary; skipping KLIP for annuli = " + str(a))
         #   print()
            #assign a unique value as a flag for these cases in the parameter explorer map
         #   PECube[:,:,:,acount,:] = -1000
                    
        acount+=1
    
    if verbose is True:        
        print("Writing parameter explorer file to " + path_to_files + "_klip/")
    #write parameter explorer cube to disk
    writeData(PECube, hdr, allParams = True, snrmap = True, pre = 'paramexplore_')
    
    
    

    print("KLIP automation complete")    
    print("End clock time is", time.time())
    print("End process time is", time.process_time())
    print("Total clock runtime: ", time.time()- start_time)
    print("Total process runtime:", time.process_time()-start_process_time)