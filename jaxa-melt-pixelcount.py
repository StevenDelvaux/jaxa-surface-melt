import numpy as np
import matplotlib.pyplot as plt
from math import *
from collections import defaultdict
from PIL import Image, ImageFont, ImageDraw
from datetime import date, datetime, timedelta
import requests
import os
import matplotlib.ticker as ticker
import time
import contextlib
import dropbox_client

threshold = 5

aland = [0]
aocean = [0]
ablack = [0]
awhite = [0]
alightblue = [0]
amiddleblue = [0]
astrongblue = [0]
adeepblue = [0]
aice = [0]
agreen = [0]
aother = [0]
atotal = [0]

aavg = []

auto = True
export = True

prefix = "./"

year = 2025
startyear = year
endyear = year
startmonth = 6
endmonth = 6
startday = 1
endday = 7

monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]

uploadToDropbox = True
orbits = ['ascending','descending']

def add(x, y):
	return x+y

def getFilename(date, orbit):
	return prefix + orbit + '/VISHOP_JAXA_SIT_' + str(date.year) + padzeros(date.month) + padzeros(date.day) + '.png';

def getWebFilename(date, orbit):
	orbitname = (orbit[0]).capitalize()
	return 'https://ads.nipr.ac.jp/vishop/data/jaxa/data/' + str(date.year) + padzeros(date.month) + '/AM2SI' + str(date.year) + padzeros(date.month) + padzeros(date.day) + orbitname + '_SIT_NP.png'

def padzeros(n):
	"""
	Left pad a number with zeros. 
    """
	return str(n) if n >= 10 else '0'+str(n)

def pixcount(date, orbit):
	print('date: ' + str(date) + ', orbit: ' + orbit)
		
	filename = getFilename(date, orbit);
	exists = True
	if not os.path.isfile(filename):
		exists = False
		#downloadImage(date, orbit, filename)
		path = getWebFilename(date, orbit)
		print('path:' + path)
		print('file not found ' + filename)
		file_object = requests.get(path) 
		with open(filename, 'wb') as local_file:
			local_file.write(file_object.content)

	path = getFilename(date, orbit)
	im = Image.open(path)
	im = im.convert("RGBA")
	by_color = defaultdict(int)
	
	ocean = 0
	land = 0	
	
	black = 0
	white = 0
	
	lightblue = 0
	middleblue = 0
	strongblue = 0
	deepblue = 0
		
	green = 0
	yellow = 0
	red = 0
	ice = 0
		
	other = 0	
	total = 0

	width, height = im.size
	pixelmatrix = im.load()
	print('width: ' + str(width) + ', height: ' + str(height))
		
	for row in range(height):
		for col in range(width):
			radius = 0
			nradius = 0
			keeplooking = True
			if avgpixelmatrix:
				avgpixel = avgpixelmatrix[row][col]
				isnew = avgpixel[3] == 255
				bluecount = 0 if isnew else avgpixel[0]
				addedbluecount = bluecount + 1
				currentbluepixel = (bluecount, avgpixel[1], avgpixel[2], 254)
				addedbluepixel = (addedbluecount, avgpixel[1], avgpixel[2], 254)

			#if(row == 100 or row == 900 or col == 100 or col == 900):						
			#	pixelmatrix[col,row] = (249,218,180,0)

			while(keeplooking == True):
			
				keeplooking = False
				
				pixel = pixelmatrix[col,row]
				isblue = False
				isgreen = False
				if(radius == 0):							
					total += 1

				if(row <= 100 or row >= 900 or col <= (50 if plotAvg else 100) or col >= (950 if plotAvg else 900)):						
					yy = 1
				elif abs(pixel[0]-120) == 0 and abs(pixel[1]-120) == 0 and abs(pixel[2]-120) == 0:
					land += 1
				elif abs(pixel[0]) == 0 and abs(pixel[1] - 9) == 0 and abs(pixel[2]-119) == 0:
					ocean += 1
					if avgpixelmatrix:
						avgpixelmatrix[row][col] = (addedbluecount,0,0,253)
				elif abs(pixel[0]) == 0 and abs(pixel[1]) == 0 and abs(pixel[2]) == 0:
					black += 1
				elif abs(pixel[0]-255) == 0 and abs(pixel[1]-255) == 0 and abs(pixel[2]-255) == 0:
					black += 1
				elif abs(pixel[0]-204) == 0 and abs(pixel[1]-229) == 0 and abs(pixel[2]-255) == 0:
					lightblue += 1
					isblue = True
				elif abs(pixel[0]-153) == 0 and abs(pixel[1]-178) == 0 and abs(pixel[2]-255) == 0:
					middleblue += 1
					isblue = True
				elif abs(pixel[0]-51) == 0 and abs(pixel[1]-229) == 0 and abs(pixel[2]-255) == 0:
					strongblue += 1
					isblue = True
				elif abs(pixel[0]) == 0 and abs(pixel[1]-128) == 0 and abs(pixel[2]-255) == 0:
					deepblue += 1
					isblue = True
				elif abs(pixel[0]-6) == 0 and abs(pixel[1]-130) == 0 and abs(pixel[2]-62) == 0:
					isgreen = True
				elif abs(pixel[0]-8) == 0 and pixel[1] <= 180 and pixel[1] >= 120 and pixel[2] <= 90 and pixel[2] >= 25:
					isgreen = True
				elif pixel[0] >= 8 and pixel[0] <= 50 and pixel[1] <= 158 and pixel[1] >= 129 and pixel[2] <= 45 and pixel[2] >= 9:
					isgreen = True
				elif pixel[2] == 8 and pixel[0] <= 234 and pixel[0] >= 27 and pixel[1] >= 8 and pixel[1] <= 230:
					isgreen = True
				elif pixel[0] <= 125 and pixel[0] >= 97 and pixel[1] >= 8 and pixel[1] <= 35 and pixel[2] >= 8 and pixel[2] <= 35:
					isgreen = True
				else:
					other += 1
					#pixelmatrix[col,row] = (249,218,180,0)
				
				if isblue:
					if avgpixelmatrix:
						avgpixelmatrix[row][col] = addedbluepixel			
				elif isgreen:
					green += 1
					if avgpixelmatrix:
						avgpixelmatrix[row][col] = currentbluepixel			

	aland.append(land)
	aocean.append(ocean)

	ablack.append(black)
	awhite.append(white)
	
	agreen.append(green)

	alightblue.append(lightblue)
	amiddleblue.append(middleblue)
	astrongblue.append(strongblue)
	adeepblue.append(deepblue)
	
	aother.append(other)
	atotal.append(total)
	return (green,exists)
	
def plotLine(ax, lines, dates, idx, label, color, days):
	line = lines[idx].split(",")			
	row =  np.array([i.lstrip() for i in np.array(line[1:days+1])])
	numberOfDays = len(row)
	row = row.astype(float)
	if numberOfDays < days:
		row = np.pad(row, (0, days - numberOfDays), 'constant', constant_values=(np.nan,))	
	ax.plot(dates, row, label=label, color=color, linewidth=(3 if idx==-1 else 1));	
	
def plotGraph(inputFileName, outputFileName, suptitle, title, ymin, ymax, ylabel, days):
	fig, ax = plt.subplots(figsize=(8, 5))
	dates = np.arange(1,days+1)	
	with open(inputFileName, 'r') as f:
		lines = f.readlines()
	plotLine(ax, lines, dates, -14, '2012', (0.0,0.13,0.38), days)
	plotLine(ax, lines, dates, -13, '2013', (0,0.44,0.75), days)
	plotLine(ax, lines, dates, -12, '2014', (0.0,0.69,0.94), days)
	plotLine(ax, lines, dates, -11, '2015', (0,0.69,0.31), days)
	plotLine(ax, lines, dates, -10, '2016', (0.57,0.82,0.31), days)
	plotLine(ax, lines, dates, -9, '2017', (1.0,0.75,0), days)
	plotLine(ax, lines, dates, -8, '2018', (0.9,0.4,0.05), days)
	plotLine(ax, lines, dates, -7, '2019', (1.0,0.5,0.5), days)
	plotLine(ax, lines, dates, -6, '2020', (0.58,0.54,0.33), days)
	plotLine(ax, lines, dates, -5, '2021', (0.4,0,0.2), days)
	plotLine(ax, lines, dates, -4, '2022', (0.7,0.2,0.3), days)
	plotLine(ax, lines, dates, -3, '2023', (0.5,0.3,0.1), days)
	plotLine(ax, lines, dates, -2, '2024', (0.75,0,0), days)
	plotLine(ax, lines, dates, -1, '2025', (1,0,0), days)
		
	ax.set_ylabel(ylabel)
	fig.suptitle(suptitle)
	ax.set_title(title, fontsize=10)
	ax.legend(loc=1, prop={'size': 8})
	ax.axis([1, days, ymin, ymax])
	ax.grid(True);
	
	months = ['1 Jun', '11 Jun', '21 Jun', '1 Jul', '11 Jul', '21 Jul', '31 Jul', '10 Aug', '20 Aug', '30 Aug']
	ax.set_xticks([1,11,21,31,41,51,61,71,81,91], ['', '', '', '', '', '', '', '', '', ''])
	ax.xaxis.set_minor_locator(ticker.FixedLocator([1.1,10.9,20.9,30.9,40.9,50.9,60.9,70.9,80.9,90.9]))
	ax.xaxis.set_minor_formatter(ticker.FixedFormatter(months))
	ax.tick_params(which='minor', length=0)	
	
	fig.savefig(outputFileName)

def downloadImage(date, orbit, filename):
	path = getWebFilename(date, orbit)
	print('path:' + path)
	print('file not found ' + filename)
	file_object = requests.get(path) 
	with open(filename, 'wb') as local_file:
		local_file.write(file_object.content)

def makeAnimation(enddate, frames, orbit):
	date = enddate - timedelta(days = frames)
	filenames = []
	endpause = 5
	for k in range(frames):
		date = date + timedelta(days = 1)
		localfilename = getFilename(date, orbit)
		if not os.path.isfile(localfilename):
			downloadImage(date, orbit, localfilename)
		#img = Image.open(localfilename)
		#img1 = ImageDraw.Draw(img)
		#img1.rectangle(((360, 725), (530, 755)), fill ="#ffffff", outline ="white")
		#localfilenamebis = localfilename.replace(".png", "_bis.png" )
		#img.save(fp=localfilenamebis)	
		filenames.append(localfilename)
	print(filenames)
	lastfilename = filenames[-1]
	for k in range(endpause):
		filenames.append(lastfilename)
	with contextlib.ExitStack() as stack:
		imgs = (stack.enter_context(Image.open(f)) for f in filenames)
		img = next(imgs)
		# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
		startdate = enddate - timedelta(days = frames-1)
		filename = 'animation_jaxa_amsr2_melt_' + 'latest.gif' # getDateIsoString(startdate) + '_to_' + getDateIsoString(enddate) + '.gif'
		img.save(fp=filename, format='GIF', append_images=imgs, save_all=True, duration=500, loop=0) #, quality=25, optimize=True, compress_level=9)
		#compress_string = "magick mogrify -layers Optimize -fuzz 7% " + filename
		#subprocess.run(compress_string, shell=True)
		#optimize(filename)

def appendToCsvFile(filename, data):
	print('inside appendToCsvFile', filename, data)
	if len(data) == 0:
		return
	with open(filename, "a") as myfile:
		myfile.write( ',' + ','.join(map(str,data)))

def getLatestDate(today):
	date = today - timedelta(days=1)
	filename = getNcFilename(date)	
	while not os.path.isfile(prefix + filename) and date.month > 5:
		date = date - timedelta(days=1)
		filename = getNcFilename(date)
	return date	

def plotavg(avgim, avgpixelmatrix, startdate, enddate):
	width, height = avgim.size
	avgim = avgim.convert("RGBA")
	avgmatrix = avgim.load()
	for row in range(height):
		for col in range(width):
			avgpixel = avgpixelmatrix[row][col]
			if avgpixel[3] == 253:
				avgpixelmatrix[row][col] = (0,9,119,255)
			elif avgpixel[3] == 254:
				meltdays = avgpixel[0]
				avgpixelmatrix[row][col] = (255-10*meltdays,255-5*meltdays,255,255)
			avgmatrix[col,row] = avgpixelmatrix[row][col]
			
			#if row > 20 and row < 47 and col > 815 and col < 955:
			#	avgmatrix[col,row] = (255,255,255,255)
			#if row > 20 and row < 47 and col > 815 and col < 955:
			#	avgmatrix[col,row] = (255,255,255,255)
			
			if row < 250:
				avgmatrix[col,row] = (255,255,255,255)

			if row > 780:
				if row > 784 and row < 804 and col > 300 and col < 800:
					avgmatrix[col,row] = (255-(col-300),255-(col-300)//2,255)
				else:
					avgmatrix[col,row] = (255,255,255,255)
			
			#if row < 50:
			#	avgmatrix[col,row] = (255,255,255,255)
			
			#if row > 950 and row < 1000:
			#	if row > 956 and row < 976 and col > 325 and col < 675:
			#		avgmatrix[col,row] = (255-(col-325),255-(col-325)//2,255)
			#	else:
			#		avgmatrix[col,row] = (255,255,255,255)
	printimtext = ImageDraw.Draw(avgim)
	color = (0,0,0)
	fontsize=24
	font = ImageFont.truetype("arialbd.ttf", fontsize)
	#printimtext.text((325,973), '0', color, font=font)
	#printimtext.text((425,973), '10', color, font=font)
	#printimtext.text((525,973), '20', color, font=font)
	#printimtext.text((625,973), '30', color, font=font)
	#printimtext.text((675,973), 'days', color, font=font)
	#printimtext.text((50,1), 'AMSR2 cumulative surface melt days', color, font=font)
	#printimtext.text((50,25), '1 June to 6 July 2024', color, font=font)
	#printimtext.text((760,1), orbit + ' orbit', color, font=font) # 820
	##printimtext.text((850,25), 'orbit', color, font=font)
	printimtext.text((295,803), '0', color, font=font)
	printimtext.text((388,803), '10', color, font=font)
	printimtext.text((488,803), '20', color, font=font)
	printimtext.text((588,803), '30', color, font=font)
	printimtext.text((688,803), '40', color, font=font)
	printimtext.text((788,803), '50', color, font=font)
	printimtext.text((850,803), 'days', color, font=font)
	printimtext.text((252,200), 'AMSR2 cumulative surface melt days', color, font=font)
	printimtext.text((252,224), str(startdate.day) + ' ' + str(monthNames[startdate.month-1]) + ' to ' + str(enddate.day) + ' ' + str(monthNames[enddate.month-1]) + ' ' + str(enddate.year), color, font=font)
	printimtext.text((730,224), orbit + ' orbit', color, font=font) # 820
	
	cropim = avgim.crop((250,200,930,830))

	cropim.save('jaxa-amsr2-melt-days-' + orbit + '.png')

plotAvg = False

avgpixelmatrix = None
if plotAvg:
	startdate = datetime(2024,6, 1)
	enddate = datetime(2024,7,30)
	orbit = 'ascending'

	avgfilename = 'VISHOP_JAXA_SIT_20240415_' + orbit + '.png'
	avgim = Image.open(avgfilename)	
	avgdata = avgim.getdata();
	avgdatalist = list(avgdata);
	avgwidth, avgheight = avgim.size
	avgpixelmatrix = [avgdatalist[i * avgwidth:(i + 1) * avgwidth] for i in range(avgheight)]
	date = startdate
	while date <= enddate:
		pixcount(date, orbit)
		date = date + timedelta(days = 1)
	plotavg(avgim, avgpixelmatrix, startdate, enddate)
	exit()

date = datetime(startyear, startmonth, startday)
to = datetime(endyear, endmonth, endday)

#plotGraph("jaxa-amsr2-nonmelting.csv", "jaxa-amsr2-nonmelting-2023.png", "JAXA AMSR2: number of non-melting pixels", "average of ascending and descending orbits", 20000, 90000, "pixels", 31)
#exit()
#date = datetime(2024,6,1)
#orbits = ['descending', 'ascending']
#while date <= datetime(2024,6,7):
#	for orbit in orbits:
#		filename = getFilename(date, orbit)
#		downloadImage(date, orbit, filename)
#		time.sleep(10)
#	date = date + timedelta(days = 1)
#exit()
if(auto):
	orbits = ['ascending', 'descending']
	yesterday = date.today() - timedelta(days = 1)
	date = yesterday
	to = date.today() - timedelta(days = 1)
	
if date > to:
	exit()
	
while date <= to:
	greenavg = 0
	counter = 0
	for orbit in orbits:
		(green,exists) = pixcount(date, orbit)
		greenavg += green
		counter += 1
	greenavg = greenavg/counter
	if not auto or not exists:
		aavg.append(greenavg)
	date = date + timedelta(days = 1) 

if(auto):
	print('inside aavg', aavg)
	csvFilename = "jaxa-amsr2-nonmelting.csv"
	if len(aavg) > 0:
		#dropbox_client.downloadFromDropbox([csvFilename])
		time.sleep(5)
		appendToCsvFile(csvFilename, aavg)
		time.sleep(10)
	plotGraph(csvFilename, "jaxa-amsr2-nonmelting.png", "JAXA AMSR2: number of non-melting pixels", "average of ascending and descending orbits", 0, 90000, "pixels", 92)
	time.sleep(10)
	if uploadToDropbox:
		filenames = ['jaxa-amsr2-nonmelting.png', csvFilename]
		dropbox_client.uploadToDropbox(filenames)
		
alldata = [ablack, awhite, aland, aocean, agreen, alightblue, 
amiddleblue, astrongblue, adeepblue, aother, atotal]
np.savetxt("jaxadata.csv", aavg, delimiter=",", fmt="%.0f")
#makeAnimation(datetime.today() - timedelta(days = 1), 10, 'ascending')

print('')
print('black = ' + str(ablack))
print('white = ' + str(awhite))
print('land = ' + str(aland))
print('ocean = ' + str(aocean))

print('green = ' + str(agreen))

print('light blue = ' + str(alightblue))
print('middle blue = ' + str(amiddleblue))
print('strong blue = ' + str(astrongblue))
print('deep blue = ' + str(adeepblue))

print('other = ' + str(aother))
print('total = ' + str(atotal))
print('combined = ' + str(aavg))
	