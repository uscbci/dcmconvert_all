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

gear = fw.lookup("gears/dicom-mr-classifier")

for acq in acqs:
    print("Working on %s" % acq.label)

    #find the dicom file
    for file in acq.files:
        if file.type == "dicom":
            source_file = file

    #Set up the gear
    inputs = {'dicom':source_file}
   
    #Run the gear
    job_id = gear.run(inputs=inputs)
