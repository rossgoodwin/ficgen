import math
import argparse
import random
from random import choice as rc
from random import sample as rs
from random import randint as ri
import string
import math
from zipfile import ZipFile

import nltk
import en

from g_paths import gPaths
from erowid_experience_paths import erowidExpPaths
from tropes_character import characterTropeFiles
from tropes_setting import settingTropeFiles
from scp_paths import scpPaths
from firstnames_f import fFirstNames
from firstnames_m import mFirstNames
from surnames import surnames


# TODO:
# [ ] CLEAN UP TROPE FILE PATHS LIST
# [ ] Fix "I'm" and "I'll" problem
# [ ] Add Plot Points / Narrative Points / Phlebotinum
# [ ] subtrope / sub-trope
# [ ] add yelp reviews
# [ ] add livejournal
# [X] add SCP

# System Path

sysPath = "/Users/rg/Projects/plotgen/ficgen/"


# Argument Values

genre_list = ['literary', 'sci-fi', 'fantasy', 'history', 'romance', 'thriller', 
			  'mystery', 'crime', 'pulp', 'horror', 'beat', 'fan', 'western', 
			  'action', 'war', 'family', 'humor', 'sport', 'speculative']
conflict_list = ['nature', 'man', 'god', 'society', 'self', 'fate', 'tech', 'no god', 'reality', 'author']
narr_list = ['first', '1st', '1', 'third', '3rd', '3', 'alt', 'alternating', 'subjective', 
			 'objective', 'sub', 'obj', 'omniscient', 'omn', 'limited', 'lim']

parser = argparse.ArgumentParser(description='Story Parameters')
parser.add_argument('--charnames', nargs='*', help="Character Names")
parser.add_argument('--title', help="Story Title")
parser.add_argument('--length', help="Story Length (0-999)")
parser.add_argument('--charcount', help="Character Count (0-999)")
parser.add_argument('--genre', nargs='*', help="Genre", choices=genre_list)
parser.add_argument('--conflict', nargs='*', help="Conflict", choices=conflict_list)
parser.add_argument('--passion', help="Passion (0-999)")
parser.add_argument('--verbosity', help="Verbosity (0-999)")
parser.add_argument('--realism', help="Realism (0-999)")
parser.add_argument('--density', help="Density (0-999)")
parser.add_argument('--accessibility', help="Accessibility (0-999)")
parser.add_argument('--depravity', help="Depravity (0-999)")
parser.add_argument('--linearity', help="Linearity (0-999)")
parser.add_argument('--narrator', nargs='*', help="Narrative PoV", choices=narr_list)
args = parser.parse_args()


# ESTABLISH SYSTEM-WIDE COEFFICIENTS/CONSTANTS

# tsv = trope setting volume
TSV = (int(args.length)/2.0 + int(args.realism)/6.0 + int(args.passion)/3.0)/1000.0
if 'fan' in args.genre:
	TSV += 1.0
TSV = int(math.ceil(2.0*TSV))

# cc = actual number of extra characters / MAKE EXPONENTIAL
CC = int(math.exp(math.ceil(int(args.charcount)/160.0))/2.0)+10

# chc = chapter count
CHC = int(math.exp(math.ceil(int(args.length)/160.0))/2.0)+10

# dtv = drug trip volume
DTV = (int(args.length)/4.0 + int(args.realism)/12.0 + int(args.passion)/6.0 + int(args.depravity)*1.5)/1000.0
if 'beat' in args.genre:
	DTV += 1.0
if 'society' in args.conflict:
	DTV += 1.0
DTV = int(math.ceil(5.0*DTV))

# scp = scp article volume
SCP = int(args.length)/1000.0
if bool(set(['sci-fi', 'horror']) & set(args.genre)):
	SCP += 1.0
if bool(set(['tech', 'no god', 'reality', 'nature', 'god']) & set(args.conflict)):
	SCP += 1.0
SCP = int(math.ceil(2.0*SCP))

# den = length (in chars) of project gutenerg excerpts
DEN = int(args.density)*10

# ggv = gutenberg excerpt volume
GGV = (int(args.length) + int(args.density))/500.0
if 'literary' in args.genre:
	GGV += 2.0
GGV = int(math.ceil(5.0*GGV))

# chl = chapter length as percent of potential chapter length
CHL = int(args.length)/1000.0


# file text fetchers
def get_file(fp):

	f = open(sysPath+fp, 'r')
	t = f.read()
	f.close()

	return t

def get_zip(fp):

	fileName = fp.split('/')[-1]
	noExtName = fileName.split('.')[0]
	txtName = noExtName + ".txt"

	ff = ZipFile(fp, 'r')
	fileNames = ff.namelist()
	oo = ff.open(fileNames[0], 'r')
	tt = oo.read()
	oo.close()
	ff.close()

	return tt



# CLASSES

class Character(object):

	def __init__(self, firstName, lastName):
		self.firstName = firstName
		self.lastName = lastName
		self.introDesc = ""
		self.scenes = []
		self.drugTrips = []
		self.scpReports = [] 
		self.gbergExcerpts = []
		self.friends = [] # list of objects


class Chapter(object):

	def __init__(self, charObj):
		self.charObj = charObj
		self.title = ""
		self.blocks = []


	def title_maker(self):
		charTitle = ri(0, 2)

		if not bool(charTitle):

			ttl = self.charObj.firstName + " " + self.charObj.lastName

		else:
			
			titleSource = ri(0, 3)

			if titleSource == 0:
				textSource = rc(self.charObj.scenes)
			elif titleSource == 1:
				textSource = rc(self.charObj.drugTrips)
			elif titleSource == 2:
				textSource = rc(self.charObj.scpReports)
			elif titleSource == 3:
				textSource = rc(self.charObj.gbergExcerpts)

			tokens = nltk.word_tokenize(textSource)

			if len(tokens) > 20:
				index = ri(0, len(tokens)-10)
				titleLen = ri(2, 6)
				ttl = ' '.join(tokens[index:index+titleLen])
			else:
				ttl = self.charObj.firstName + " " + self.charObj.lastName

		self.title = ttl


	def chapter_builder(self):
		blockList = [self.charObj.introDesc] + self.charObj.scenes + self.charObj.drugTrips + self.charObj.scpReports + self.charObj.gbergExcerpts
		
		random.shuffle(blockList)

		stopAt = int(math.ceil(CHL*len(blockList)))

		blockList = blockList[:stopAt]

		self.blocks = blockList

		# self.blocks.append("stuff")



class Novel(object):

	def __init__(self):
		self.title = args.title
		self.characters = [] # list of characters
		self.chapters = [] # list of chapters

	def generate(self):
		self.make_chars()
		self.assemble_chapters()
		self.make_tex_file()


	def make_tex_file(self):
		# Look at PlotGen for this part
		outputFileName = self.title

		latex_special_char_1 = ['&', '%', '$', '#', '_', '{', '}']
		latex_special_char_2 = ['~', '^', '\\']

		outputFile = open(sysPath+"output/"+outputFileName+".tex", 'w')

		openingTexLines = ["\\documentclass[12pt]{book}",
						   "\\usepackage{ucs}",
						   "\\usepackage[utf8x]{inputenc}",
						   "\\usepackage{hyperref}",
						   "\\title{"+outputFileName+"}",
						   "\\author{collective consciousness fiction generator\\\\http://rossgoodwin.com/ficgen}",
						   "\\date{\\today}",
						   "\\begin{document}",
						   "\\maketitle"]

		closingTexLine = "\\end{document}"

		for line in openingTexLines:
			outputFile.write(line+"\n\r")
		outputFile.write("\n\r\n\r")

		x = 1
		for ch in self.chapters:

			outputFile.write("\\chapter{"+str(x)+"}\n\r")
			outputFile.write("\n\r\n\r")

			rawText = '\n\r\n\r\n\r'.join(ch.blocks)

			try:
				rawText = rawText.decode('utf8')
			except:
				pass
			try:
				rawText = rawText.encode('ascii', 'ignore')
			except:
				pass

			i = 0
			for char in rawText:

				if char == "\b":
					outputFile.seek(-1, 1)
				elif char in latex_special_char_1 and rawText[i-1] != "\\":
					outputFile.write("\\"+char)
				elif char in latex_special_char_2 and not rawText[i+1] in latex_special_char_1:
					outputFile.write("-")
				else:
					outputFile.write(char)

				i += 1

			outputFile.write("\n\r\n\r")
			x += 1

		outputFile.write("\n\r\n\r")
		outputFile.write(closingTexLine)

		outputFile.close()

		print '\"'+sysPath+'output/'+outputFileName+'.tex\"'


	def assemble_chapters(self):
		novel = []

		for c in self.characters:
			novel.append(Chapter(c))

		for ch in novel:
			ch.title_maker()
			ch.chapter_builder()

		random.shuffle(novel) # MAYBE RETHINK THIS LATER

		self.chapters = novel


	def make_chars(self):
		# establish gender ratio
		charGenders = [ri(0,1) for _ in range(CC)]
		
		# initialize list of characters
		chars = []

		# add user defined characters
		for firstlast in args.charnames:
			fl_list = firstlast.split('_')  # Note that split is an underscore!
			chars.append(Character(fl_list[0], fl_list[1]))

		# add generated characters
		for b in charGenders:
			if b:
				chars.append(Character(rc(fFirstNames), rc(surnames)))
			else:
				chars.append(Character(rc(mFirstNames), rc(surnames)))

		# establish list of intro scenes
		introScenePaths = rs(characterTropeFiles, len(chars))

		# establish list of settings
		settings = rs(settingTropeFiles, len(chars)*TSV)

		# establish list of drug trips
		trips = rs(erowidExpPaths, len(chars)*DTV)

		# establish list of scp articles
		scps = rs(scpPaths, len(chars)*SCP)

		# establish list of gberg excerpts
		gbergs = rs(gPaths.values(), len(chars)*GGV)

		i = 0
		j = 0
		m = 0
		p = 0
		s = 0
		for c in chars:

			# make friends
			c.friends += rs(chars, ri(1,len(chars)-1))
			if c in c.friends:
				c.friends.remove(c)

			# add introduction description
			c.introDesc = self.personal_trope([c], introScenePaths[i])

			# add setting scenes
			for k in range(TSV):
				c.scenes.append(self.personal_trope([c]+c.friends, settings[j+k]))

			# add drug trip scenes
			for n in range(DTV):
				c.drugTrips.append(self.personal_trip([c]+c.friends, trips[m+n]))

			# add scp articles
			for q in range(SCP):
				c.scpReports.append(self.personal_scp([c]+c.friends, scps[p+q]))

			# add gberg excerpts
			for t in range(GGV):
				c.gbergExcerpts.append(self.personal_gberg([c]+c.friends, gbergs[s+t]))

			i += 1
			j += TSV
			m += DTV
			p += SCP
			s += GGV

		self.characters = chars


	def personal_trope(self, charList, filePath):
		text = get_file(filePath)
		# text = text.decode('utf8')
		# text = text.encode('ascii', 'ignore')

		if len(charList) == 1:
			characterTrope = True
		else:
			characterTrope = False

		try:

			pos = en.sentence.tag(text)
			wordtag = map(list, zip(*pos))
			words = wordtag[0]
			tags = wordtag[1]

			for i in range(len(words)):
				charRef = rc([rc(charList), charList[0]])
				if words[i].lower() == "character" and i > 0:
					words[i-1] = charRef.firstName
					words[i] = charRef.lastName

				elif tags[i] == "PRP":
					words[i] = charRef.firstName
				elif tags[i] == "PRP$":
					words[i] = charRef.firstName+"\'s"
				elif tags[i] in ["VBD", "VBG", "VBN", "VBZ"]:
					try:
						words[i] = en.verb.past(words[i], person=3, negate=False)
					except:
						pass

				if characterTrope:

					if words[i] == "have":
						words[i] = "has"
					elif words[i] == "are":
						words[i] = "is"

			punc = [".", ",", ";", ":", "!", "?"]

			for i in range(len(words)):
				if words[i] in punc:
					words[i] = '\b'+words[i]

			final_text = " ".join(words)

			if characterTrope:

				mainCharRef = rc(charList)

				index = string.find(final_text, mainCharRef.firstName)

				if final_text[index+len(mainCharRef.firstName)+1:index+len(mainCharRef.firstName)+1+len(mainCharRef.lastName)] == mainCharRef.lastName:
					final_text = final_text[index:]
				else:
					final_text = mainCharRef.firstName+" "+mainCharRef.lastName+final_text[index+len(mainCharRef.firstName):]

			replacements = {"trope": "clue", "Trope": "clue", "TROPE": "CLUE"}

			for x, y in replacements.iteritems():
				final_text = string.replace(final_text, x, y)

		except:
			
			final_text = ""


		return final_text


	def personal_trip(self, charList, tripPath):

		fileText = get_file(tripPath)
		splitText = fileText.split('\\vspace{2mm}')
		endOfText = splitText[-1]
		text = endOfText[:len(endOfText)-15]

		try:

			pos = en.sentence.tag(text)
			wordtag = map(list, zip(*pos))
			words = wordtag[0]
			tags = wordtag[1]

			for i in range(len(words)):

				charRef = rc([rc(charList), charList[0]])

				if tags[i] == "PRP":
					words[i] = charRef.firstName
				elif tags[i] == "PRP$":
					words[i] = charRef.firstName+"\'s"
				elif tags[i] in ["VBD", "VBG", "VBN", "VBZ"]:
					try:
						words[i] = en.verb.past(words[i], person=3, negate=False)
					except:
						pass
				else:
					pass

			punc = [".", ",", ";", ":", "!", "?"]

			for i in range(len(words)):
				if words[i] in punc:
					words[i] = '\b'+words[i]

			final_text = " ".join(words)

			final_text = string.replace(final_text, "\\end{itemize}", "")
			final_text = string.replace(final_text, "\\begin{itemize}", "")
			final_text = string.replace(final_text, "\\end{center}", "")
			final_text = string.replace(final_text, "\\begin{center}", "")
			final_text = string.replace(final_text, "\\ldots", " . . . ")
			final_text = string.replace(final_text, "\\egroup", "")
			final_text = string.replace(final_text, "EROWID", "GOVERNMENT")
			final_text = string.replace(final_text, "erowid", "government")
			final_text = string.replace(final_text, "Erowid", "Government")

		except:

			final_text = ""

		return final_text


	def personal_scp(self, charList, scpPath):

		text = get_file(scpPath)

		text = string.replace(text, "SCP", charList[0].lastName)
		text = string.replace(text, "Foundation", charList[0].lastName)

		try:

			pos = en.sentence.tag(text)
			wordtag = map(list, zip(*pos))
			words = wordtag[0]
			tags = wordtag[1]

			for i in range(len(words)):

				charRef = rc(charList)

				if tags[i] == "PRP":
					words[i] = charRef.firstName
				elif tags[i] == "PRP$":
					words[i] = charRef.firstName+"\'s"
				elif tags[i] in ["VBD", "VBG", "VBN", "VBZ"]:
					try:
						words[i] = en.verb.past(words[i], person=3, negate=False)
					except:
						pass
				else:
					pass

			punc = [".", ",", ";", ":", "!", "?"]

			for i in range(len(words)):
				if words[i] in punc:
					words[i] = '\b'+words[i]

			final_text = " ".join(words)

		except:

			final_text = ""

		return final_text



	def personal_gberg(self, charList, gPath):

		full_text = ""
		while full_text == "":
			try:
				full_text = get_zip(gPath)
			except:
				full_text = ""
				gPath = rc(gPaths.values())

		endPart = full_text.split("*** START OF THIS PROJECT GUTENBERG EBOOK ")[-1]
		theMeat = endPart.split("*** END OF THIS PROJECT GUTENBERG EBOOK")[0]

		theMeat = string.replace(theMeat, "\r\n", " ")

		
		if len(theMeat) < DEN+5:
			text = theMeat
		else:
			startLoc = int(len(theMeat)/2.0 - DEN/2.0)
			text = theMeat[startLoc:startLoc+DEN]

		spLoc = text.find(" ")
		text = text[spLoc+1:]

		try:
			pos = en.sentence.tag(text)
			wordtag = map(list, zip(*pos))
			words = wordtag[0]
			tags = wordtag[1]

			for i in range(len(words)):

				charRef = rc([rc(charList), charList[0]])

				if tags[i] == "PRP":
					words[i] = charRef.firstName
				elif tags[i] == "PRP$":
					words[i] = charRef.firstName+"\'s"
				elif tags[i] in ["VBD", "VBG", "VBN", "VBZ"]:
					try:
						words[i] = en.verb.past(words[i], person=3, negate=False)
					except:
						pass
				else:
					pass

			punc = [".", ",", ";", ":", "!", "?"]

			for i in range(len(words)):
				if words[i] in punc:
					words[i] = '\b'+words[i]

			final_text = " ".join(words)

		except:
			final_text = ""


		return final_text


	def print_chars(self):

		c = self.make_chars()
		for character in c:
			print 'INTRO DESC'
			print '\n\n'
			print character.introDesc
			print '\n\n'
			print 'SCENES'
			print '\n\n'
			for s in character.scenes:
				print s
			print '\n\n'
			print 'DRUG TRIPS'
			print '\n\n'
			for t in character.drugTrips:
				print t
			print '\n\n'
			print 'SCP REPORTS'
			print '\n\n'
			for p in character.scpReports:
				print p
			print '\n\n'
			print 'GBERG EXCERPTS'
			print '\n\n'
			for q in character.gbergExcerpts:
				print q
			print '\n\n'




foobar = Novel()
foobar.generate()


# GENERAL FUBAR AREA

# def build_wireframe():
# 	if bool(args.length):
# 		chapterCount = int(args.length/10)
# 	else:
# 		chapterCount = random.randint
# 	chapters = [smp(range(100), ri(1, 15)) for _ in range(chapterCount)]




