from dis import dis
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from utils import mysqlselect
import random

interactions=mysqlselect("select user_id,question_id from `eam_brb`.CHATBOT_INTERACTIONS")
interactions=dict(Counter(interactions))

questions_dataset=[]
questions=mysqlselect("select id,pattern from `eam_brb`.QUESTION")
for i in questions:
    questions_dataset.append(list(i))


dataset=[]
for i in interactions:
    temp=list(i)
    temp.append(interactions[i])
    dataset.append(temp)

ratings = pd.DataFrame(dataset, columns =["user_id","question_id","count"])

final_dataset = ratings.pivot(index='question_id',columns='user_id',values='count')
final_dataset.fillna(0,inplace=True)
# print(final_dataset.head())


#To qualify a question, a minimum of 3 users should have visited a question.
#To qualify a user, a minimum of 5 question should have visited by the user.
m,n=3,5

no_user_visited = ratings.groupby('question_id')['count'].agg('count')
# print(no_user_visited)
no_questions_visited = ratings.groupby('user_id')['count'].agg('count')
f,ax = plt.subplots(1,1,figsize=(16,4))
# ratings['rating'].plot(kind='hist')
plt.scatter(no_user_visited.index,no_user_visited,color='mediumseagreen')
plt.axhline(y=m,color='r')
plt.xlabel('questionId')
plt.ylabel('No. of users visited')
# plt.show()
final_dataset = final_dataset.loc[no_user_visited[no_user_visited > m].index,:]
# print(final_dataset)

f,ax = plt.subplots(1,1,figsize=(16,4))
plt.scatter(no_questions_visited.index,no_questions_visited,color='mediumseagreen')
plt.axhline(y=n,color='r')
plt.xlabel('UserId')
plt.ylabel('No. of visits by user')
# plt.show()

final_dataset=final_dataset.loc[:,no_questions_visited[no_questions_visited > n].index]
# print(final_dataset)

#We are using only a small dataset but for the original large dataset of question lens which has more than 100000 features, our system may run out of computational resources when that is feed to the model. To reduce the sparsity we use the csr_matrix function from the scipy library.
#find and keep only non zero values
csr_data = csr_matrix(final_dataset.values)
# print(csr_data)

final_dataset.reset_index(inplace=True)

knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10, n_jobs=-1)
knn.fit(csr_data)

def get_question_recommendation(question_idx):
    n_questions_to_reccomend = 5
    question_idx = final_dataset[final_dataset['question_id'] == question_idx].index[0]
    distances , indices = knn.kneighbors(csr_data[question_idx],n_neighbors=n_questions_to_reccomend+1)  
    # print(distances,indices)  
    rec_question_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
    recommended_questions=[]
    for val in rec_question_indices:
        question_idx = int(final_dataset.iloc[val[0]]['question_id'])
        recommended_question=mysqlselect("select pattern from `eam_brb`.QUESTION where id={}".format(question_idx))        
        recommended_question= eval(recommended_question[0][0])
        recommended_question= recommended_question[random.randint(0,len(recommended_question)-1)]
        # print(recommended_question)
        recommended_questions.append(recommended_question)
    return recommended_questions

reco= get_question_recommendation(1)
print(reco)