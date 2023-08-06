import os
import sys
from astro_ghost.PS1QueryFunctions import getAllPostageStamps
from astro_ghost.TNSQueryFunctions import getTNSSpectra
from astro_ghost.NEDQueryFunctions import getNEDSpectra
#from astro_ghost.ghostHelperFunctions import getTransientHosts, getGHOST
from astro_ghost.ghostHelperFunctions import *
from astropy.coordinates import SkyCoord
from astropy import units as u
import pandas as pd
from datetime import datetime

#we want to include print statements so we know what the algorithm is doing
verbose = 1

#download the database from ghost.ncsa.illinois.edu
#note: real=False creates an empty database, which
#allows you to use the association methods without
#needing to download the full database first
getGHOST(real=False, verbose=verbose)

#create a list of the supernova names, their skycoords, and their classes (these three are from TNS)
snName = ['SN 2012dt', 'SN 1998bn', 'SN 1957B']

snCoord = [SkyCoord(14.162*u.deg, -9.90253*u.deg, frame='icrs'), \
           SkyCoord(187.32867*u.deg, -23.16367*u.deg, frame='icrs'), \
           SkyCoord(186.26125*u.deg, +12.899444*u.deg, frame='icrs')]

# run the association algorithm!
# this first checks the GHOST database for a SN by name, then by coordinates, and
# if we have no match then it manually associates them.
hosts = getTransientHosts(snName, snCoord, verbose=verbose, starcut='normal')

#create directories to store the host spectra, the transient spectra, and the postage stamps
hSpecPath = "./hostSpectra/"
tSpecPath = "./SNspectra/"
psPath = "./hostPostageStamps/"
paths = [hSpecPath, tSpecPath, psPath]
for tempPath in paths:
    if not os.path.exists(tempPath):
        os.makedirs(tempPath)

now = datetime.now()
dateStr = "%i%.02i%.02i" % (now.year,now.month,now.day)
rad = 30 #arcsec
fn_SN = 'transients_%s.csv' % dateStr
transients = pd.read_csv("./transients_%s/tables/%s"%(dateStr,fn_SN))

#get postage stamps and spectra
getAllPostageStamps(hosts, 120, psPath, verbose) #get postage stamps of hosts
getNEDSpectra(hosts, hSpecPath, verbose) #get spectra of hosts
getTNSSpectra(transients, tSpecPath, verbose) #get spectra of transients (if on TNS)


####################### helper functions for querying the database #############

# Get cooordinates associated with NGC 4568
supernovaCoord = [SkyCoord(344.5011708333333*u.deg, 6.0634388888888875*u.deg, frame='icrs')]
table = fullData()

galaxyCoord = [SkyCoord(344.50184181*u.deg, 6.06983149*u.deg, frame='icrs')]
snName = ["PTF10llv"]

db, notFound = getDBHostFromTransientCoords(supernovaCoord)
db, notFound = getDBHostFromTransientName(snName)

snName = ["SN2017hpi"]
getHostStatsFromTransientName(snName)
getHostStatsFromTransientCoords(supernovaCoord)

getTransientStatsFromHostName('UGC 12266')
getTransientStatsFromHostCoords(galaxyCoord)

getcolorim(ra, dec, size=tempSize, filters=band, format="png")
getHostImage('PTF10llv', save=0)

path = "/home/alexgagliano/Documents/Research/Transient_ML/tables/SNspectra/"
hostPath = '/home/alexgagliano/Documents/Research/Transient_ML_Box/hostSpectra/'

getTransientSpectra('SN2019ur', path)
getHostSpectra('2019dfi', hostPath)

coneSearchPairs(supernovaCoord, 1.e5)
