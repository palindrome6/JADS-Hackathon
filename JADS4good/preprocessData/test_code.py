from googletrans import Translator
from summary import get_summary
import os
from spacy_text_summarise import spacy_summarise
from langdetect import detect
from read_pdf import pdf_to_text
from entity import get_entity

all_files = []
for dirpath, dirnames, filenames in os.walk("/Users/parvathykrishnank/Desktop/Work/Hack4Good 2019/National Rapporteur Publications_1/"):
	for filename in [f for f in filenames if f.endswith(".pdf")]:
		path_file = os.path.join(dirpath, filename)

		print(filename)
		
		# Convert PDF to TEXT
		completePDF = pdf_to_text(path_file)
		# Detect the language of the text
		lan_detected = detect(completePDF)

		language = None 
		if(lan_detected=="en"):
			language = 'english'
		if(lan_detected=="nl"):
			language = 'dutch'
		
		# If language is detected

		if (language):
			noSentences = 5

			# Summarise using NLTK
			summaryTextList = (get_summary(completePDF,noSentences,language))

			# Summarise using SPACY
			summarySpacyList = (spacy_summarise(completePDF,noSentences,language))

			# Merge summary sentences from both the lists and find the set
			summaryList = (summaryTextList + summarySpacyList)
			summaryList = list(set(summaryList))
			summaryText = '.'.join(summaryList)
			#print(summaryText)

			#Array of dict with text and label
			labelsText = get_entity(completePDF,language,10)
			print(labelsText)

			#Translate to check if it makes sense!
			translator = Translator()

			summaryEng = translator.translate(summaryText).text
			print(summaryEng)

		else:
			print('Error Reading File: ', filename)

