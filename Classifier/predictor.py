# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 23:28:26 2019

Description: The Classifier class will load count vector and naive bayes models previously trained and saved by "naive_bayes_testing.py".
             The Classsfier.predict(Query) function will gove the probabilty prediction for the given query(s). 
             Classes = ["Business","Technology","Entertainment","Medical"]

@author: Allen Biju Thomas
"""

import pickle
import os

class Classifier:
    # will load the count vector model and the naive bayes model from the previously saved models
    # Warning: loading models takes time therefore , cdeclared as static variables
    print("Initialising Model...")
    naive_bayes = pickle.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'naive_bayes_model.sav'),'rb'))
    count_vector = pickle.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'count_vector_model.sav'),'rb'))
    print("Model Initialised.")
    
    # Function will take query(s) in the form of ["Publisher1,Article1 title","Publisher2,Article2 title"]
    # Function will return dictionary of predicted porbabilities of each class for each query in the form
    # {"Query1":{"Class1":prob,"Class2":prob,"class3":prob},
    #   "Query 2":{"Class1":prob,"Class2":prob,"class3":prob}}
    @staticmethod
    def predict(query):
        test_query = Classifier.count_vector.transform(query)
        # pred = Classifier.naive_bayes.predict(test_query)
        prob = Classifier.naive_bayes.predict_proba(test_query)
        all_query_probability_dictionary = {}
        result = ["Business","Technology","Entertainment","Medical"]

        for i,j in zip(query,prob):
            probability_dictionary = {}
            for k,l in zip(j,result):
                probability_dictionary.update({l:k})
            all_query_probability_dictionary.update({i:probability_dictionary})
        # print(all_query_probability_dictionary)
        return all_query_probability_dictionary




# testing the class
# query = ["TechCrunch, What is Andela, the Africa temch talent accelerator?",
#     "Livemint, Mint50: Hand-picked mutual funds to build your portfolio",
#     "Los Angeles Times, Why Tom Hanks’ portrayal of Mister Rogers is more than just one nice guy playing another",
#     "All new VR movie Experiance"
#     ]


# for i in range(0,3):
#     k = i%3
#     print('\nQuery '+str(i)+'\n')
#     x = Classifier.predict([query[k]])
#     for j in x:
#         print(j+" :\n"+str(x[j]))


    


# print('\nQuery2\n')
# x = Classifier.predict(query2)
# for i in x:
#     print(i+" :\n"+str(x[i]))

# print('\nQuery3\n')
# x = Classifier.predict(query3)
# for i in x:
#     print(i+" :\n"+str(x[i]))





# import pickle

# naive_bayes = pickle.load(open('C://Users//Allen Biju Thomas//Desktop//TheBlink Project//TheBlink//Classifier//naive_bayes_model.sav','rb'))
# count_vector = pickle.load(open('C://Users//Allen Biju Thomas//Desktop//Test//count_vector_model.sav ','rb'))

# query = input("Enter Title:")

# test_query = count_vector.transform(query)
# pred = naive_bayes.predict(test_query)
# prob = naive_bayes.predict_proba(test_query)
# print(prob)
# result = {1:"Business",2:"Technology",3:"Entertainment",4:"Medical"}
# for i,j in zip(pred,range(len(query))):
#     print(result[int(i)]+" : "+ query[j])
# query = ["digitalistmag, Computer Vision: An Artificial Eye To Blind People"]
# Classifier.predict(query)