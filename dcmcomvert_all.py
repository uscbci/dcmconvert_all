#!/usr/bin/env python
import flywheel

import argparse

#Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("sessionpath",help="in the form of group/session/subject/session")
parser.add_argument("api_key_file",help="file containing api key")
args = parser.parse_args()
api_key_file = args.api_key_file

#read in the api key
with open(api_key_file,'r') as file:
    api_key = file.read().replace('\n','')

#Set up the flywheel API
fw = flywheel.Client(api_key)

flywheel_session = fw.lookup(args.sessionpath)

acqs = flywheel_session.acquisitions()

gear = fw.lookup("gears/dcm2niix/2.1.1a_1.0.20240202")

for acq in acqs:
    print("Working on %s" % acq.label)

    #find the dicom file
    niftifound = 0
    for file in acq.files:
        if file.type == "dicom":
            source_file = file
        if file.type == "nifti":
            niftifound = 1

    if (niftifound):
        print("  Already converted")
    else:
        if ("Intent" in file.classification.keys()):
            if (file.classification["Intent"][0] == "Structural" or file.classification["Intent"][0] == "Functional"):
                #Set up the gear
                inputs = {'dcm2niix_input':source_file}
                config = {'anonymize_bids':True, 
                        'bids_sidecar': 'y',
                        'compress_images': 'y',
                        'compression_level': 6,
                        'filename': '%f_%p_%t_%s'
                        }
                
                #Run the gear
                job_id = gear.run(inputs=inputs, config=config)
            else:
                print("We don't convert this file, intent is %s" % file.classification["Intent"][0])
