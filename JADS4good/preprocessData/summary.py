import re
import nltk
import heapq 

def get_summary(text,no_sentences,language):

    article_text = re.sub(r'\[[0-9]*\]', ' ', text)  
    article_text = re.sub(r'\s+', ' ', text)  

    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )  
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)  

    sentence_list = nltk.sent_tokenize(article_text)  


    '''
    Find Weighted Frequency of Occurrence
    '''

    stopwords = nltk.corpus.stopwords.words(language)

    word_frequencies = {}  
    for word in nltk.word_tokenize(formatted_article_text):  
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1


    '''
    Next, we loop through all the sentences and then corresponding words to first check if they are stop words. 
    If not, we proceed to check whether the words exist in word_frequency dictionary i.e. word_frequencies, or not. 
    If the word is encountered for the first time, it is added to the dictionary as a key and its value is set to 1. 
    Otherwise, if the word previously exists in the dictionary, its value is simply updated by 1.

    Finally, to find the weighted frequency, we can simply divide the number of occurances of all the words 
    by the frequency of the most occurring word
    '''

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)


    '''
    Calculating Sentence Scores
    We have now calculated the weighted frequencies for all the words. 
    Now is the time to calculate the scores for each sentence by adding weighted frequencies of the words 
    that occur in that particular sentence. The following script calculates sentence scores:
    '''

    sentence_scores = {}  
    for sent in sentence_list:  
        sent = re.sub('[^a-zA-Z]', '', sent )  
        sent = re.sub(r'\s+', '', sent)  
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]


    '''
    Getting the Summary
    Now we have the sentence_scores dictionary that contains sentences with their corresponding score. 
    To summarize the article, we can take top N sentences with the highest scores. 
    The following script retrieves top 5 sentences and prints them on the screen.
    '''

    summary_sentences = heapq.nlargest(no_sentences, sentence_scores, key=sentence_scores.get)
    return (summary_sentences) 