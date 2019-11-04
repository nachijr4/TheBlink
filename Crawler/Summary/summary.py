import bs4 as bs
import re
from nltk.tokenize import sent_tokenize, word_tokenize
import heapq
from nltk.corpus import stopwords


class Summary:
    def __init__(self, article_text):
        self.article_text = article_text

    def get_summary(self):
        # Removing special characters and digits
        try:
            formatted_article_text = re.sub('[^a-zA-Z]', ' ', self.article_text )
            formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
            sentence_list = sent_tokenize(self.article_text)
            list_of_stopwords = stopwords.words('english')
            word_frequencies = {}
            for word in word_tokenize(formatted_article_text):
                if word not in list_of_stopwords:
                    if word not in word_frequencies.keys():
                        word_frequencies[word] = 1
                    else:
                        word_frequencies[word] += 1

            maximum_frequncy = max(word_frequencies.values())
            for word in word_frequencies.keys():
                word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

            sentence_scores = {}
            for sent in sentence_list:
                for word in word_tokenize(sent.lower()):
                    if word in word_frequencies.keys():
                        if len(sent.split(' ')) < 30:
                            if sent not in sentence_scores.keys():
                                sentence_scores[sent] = word_frequencies[word]
                            else:
                                sentence_scores[sent] += word_frequencies[word]
            summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

            summary = ' '.join(summary_sentences)
            return summary
        
        except:
            return None