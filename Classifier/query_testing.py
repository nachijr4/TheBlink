# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 23:28:26 2019

Description: The Classifier class will load count vector and naive bayes models previously trained and saved by "naive_bayes_testing.py".
             The Classsfier.predict(Query) function will gove the probabilty prediction for the given query(s). 
             Classes = ["Business","Technology","Entertainment","Medical"]

@author: Allen Biju Thomas
"""


class Classifier:

    # will load the count vector model and the naive bayes model from the previously saved models
    # Warning: loading models takes time therefore , class object must be created beforehand
    def __init__(self):
        import pickle
        print("Initialising Model...")
        self.naive_bayes = pickle.load(open('C://Users//Allen Biju Thomas//Desktop//TheBlink Project//TheBlink//Classifier//naive_bayes_model.sav','rb'))
        self.count_vector = pickle.load(open('C://Users//Allen Biju Thomas//Desktop//TheBlink Project//TheBlink//Classifier//count_vector_model.sav','rb'))
        print("Model Initialised.")
    

    # Function will take query(s) in the form of ["Publisher1,Article1 title","Publisher2,Article2 title"]
    # Function will return dictionary of predicted porbabilities of each class for each query in the form
    # {"Query1":{"Class1":prob,"Class2":prob,"class3":prob},
    #   "Query 2":{"Class1":prob,"Class2":prob,"class3":prob}}
    def predict(self,query):
        test_query = self.count_vector.transform(query)
        pred = self.naive_bayes.predict(test_query)
        prob = self.naive_bayes.predict_proba(test_query)
        all_query_probability_dictionary = {}
        result = ["Business","Technology","Entertainment","Medical"]

        for i,j in zip(query,prob):
            probability_dictionary = {}
            for k,l in zip(j,result):
                probability_dictionary.update({l:k})
            all_query_probability_dictionary.update({i:probability_dictionary})

        return all_query_probability_dictionary




# testing the class
query = ["TechCrunch, What is Andela, the Africa temch talent accelerator?" ,
"Livemint, Mint50: Hand-picked mutual funds to build your portfolio",
"Los Angeles Times, Why Tom Hanks’ portrayal of Mister Rogers is more than just one nice guy playing another",
"All new VR movie Experiance"
]

classifier = Classifier()
x = classifier.predict(query)

for i in x:
    print(i+" :\n"+str(x[i]))





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
