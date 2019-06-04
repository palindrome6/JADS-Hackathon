import spacy
from collections import Counter
import re

def get_entity(text,number_tokens,language):

	text = re.sub('[^a-zA-Z]', ' ', text )  
	text = re.sub(r'\s+', ' ', text) 

	if(language=='dutch'):
		nlp = spacy.load("nl_core_news_sm")
	
	else:
		nlp = spacy.load("en_core_web_sm")

	doc = nlp(text)
	array_ent = []
	for entity in doc.ents:
		array_ent.append({'text':entity.text, 'label':entity.label_})
	return array_ent
