# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 23:28:26 2019

@author: Allen Biju Thomas
"""

#Query

import pickle
count_vector = pickle.load(open('count_vector_model.sav','rb'))
naive_bayes = pickle.load(open('naive_bayes_model.sav','rb'))

#query = input("Enter Title:")
query = ["TechCrunch, What is Andela, the Africa temch talent accelerator?" ,
"Livemint, Mint50: Hand-picked mutual funds to build your portfolio",
"Los Angeles Times, Why Tom Hanks’ portrayal of Mister Rogers is more than just one nice guy playing another",
"Proclinical, Top 10 new medical technologies of 2019"
]
#query.append(input("enter quer: "))
test_query = count_vector.transform(query)
pred = naive_bayes.predict(test_query)
prob = naive_bayes.predict_proba(test_query)
print(prob)
result = {1:"Business",2:"Technology",3:"Entertainment",4:"Medical"}
for i,j in zip(pred,range(len(query))):
    print(result[int(i)]+" : "+ query[j])