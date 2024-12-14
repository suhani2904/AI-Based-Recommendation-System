# app.py
# Flask Backend Application
# Description:
# This script initializes the Flask server, defines routes, and serves HTML templates
# for a freelancer-job recommendation system.


# Import necessary libraries
from flask import Flask
from flask import render_template , request
import string
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np


# Initialize Flask Application
app = Flask(__name__ , template_folder="../templates" , static_folder= "../static")

## Home Page Route
@app.route('/')
def home_page():
    return render_template('Home.html')

##Freelancer Page
@app.route('/freelancer')
def freelancer():
    return render_template('form_freelancer.html')


##Jobs Page
@app.route('/jobs')
def jobs():
    return render_template('form_jobs.html')

##Create Account for Freelancer
@app.route('/login_1', methods = ['POST' , 'GET'])
def login_1():
    tags_1 = ""
    if request.method == 'GET':
        name = request.args.get('freelancer', '').strip()
        skills = request.args.get('skills', '')
        hourly_rate = request.args.get('hourly', '')
        country = request.args.get('country', '')
        experience = request.args.get('experience', '')
        job_success = request.args.get('job success', '')
        title = request.args.get('title', '')
        description = request.args.get('description', '')
        password = request.args.get('password' , '').strip()
        rating = request.args.get('rate' , '')
        total_hours = request.args.get('total_hours' , '')
        skills_for_recommend = ' '.join(skill.strip().replace(" ", "") for skill in skills.split(',')) 
        title_for_recommend = ' '.join(t.strip().replace(" ", "") for t in title.split(','))
        tags_1 =  skills_for_recommend + " " + title_for_recommend + " " + country   + " " +  total_hours + " " + hourly_rate + " "  + experience + " " +  rating + " " + job_success
        details_1 = preprocessing(tags_1)
        add_data_to_2_cols([name , details_1] , 'Data/freelancer_2.pkl')
        add_data([country , description, hourly_rate , job_success, name , skills , title , total_hours ,  experience , password , rating] , 'Data/update_free.pkl')
        recommend = vectorization(details_1 , 'free')
        lists = info(recommend , 'Data/update_jobs.pkl')
        return render_template('recommendations.html' , lists = lists)

##Create Account for company
@app.route('/login_2' , methods = ['POST' , 'GET'])
def login_2():
    tags_2 = ""
    if request.method == 'POST':
        name = request.form['name'].strip()
        skills = request.form['skills']
        hourly_rate = request.form['hourly']
        country = request.form['country']
        experience = request.form['experience']
        job_success = request.form['job success']
        title = request.form['title']
        description = request.form['description']
        password = request.form['password'].strip()
        rating = request.form['rate']
        total_hours = request.form['total_hours']
        skills_for_recommend = ' '.join(skill.strip().replace(" ", "") for skill in skills.split(','))
        tags_2 =    skills_for_recommend + " " + title + " " + country  + " " + total_hours + " " + hourly_rate + " " + experience + " " +  rating+ " "  + job_success
        details_2 = preprocessing(tags_2)
        add_data_to_2_cols([name, details_2] , 'Data/jobs_2.pkl')
        add_data([country , description, hourly_rate , job_success, name , skills , title , total_hours ,  experience , password , rating] , 'Data/update_jobs.pkl')
        recommend = vectorization(details_2 , 'company')
        lists = info(recommend , 'Data/update_free.pkl')
        return render_template('recommendations.html' , lists = lists)
    return  render_template('recommendations.html' , recommend = recommend)
    
##Have an account for freelancer
@app.route('/submit1' , methods = ['GET'])
def submit1():
    return render_template('login_freelancer.html')

##Have an account for company
@app.route('/submit2' , methods = ['GET'])
def submit2():
    return render_template('login_jobs.html')


@app.route('/signin_1' , methods = ['POST'])
def signin_1():
    if request.method == 'POST':
        name = request.form['name'].strip()
        password = request.form['password'].strip()
        recommend = get_info(name , password , 'Data/update_free.pkl' , 'free')
        if (recommend == "you don't have account") or recommend == "Alert: Not found":
            return "You don't have account"
        lists = info(recommend , 'Data/update_jobs.pkl')
        return render_template('recommendations.html' , lists = lists)


@app.route('/signin_2' , methods = ['POST' , 'GET'])
def signin_2():
    if request.method == 'GET':
        name = request.args.get('name' , '').strip()
        password = request.args.get('password' , '').strip()
        recommend = get_info(name , password , 'Data/update_jobs.pkl' , 'company')
        if (recommend == "you don't have account") or recommend == "Alert: Not found":
            return "You don't have account"
        lists = info(recommend , 'Data/update_free.pkl')
        return render_template('recommendations.html' , lists = lists)
    
    else:
        return "none"



def preprocessing(text):
    tags= ""
# lowering the text
    text = text.lower()
    
# Remove punctuation using str.translate() and string.punctuation
    text =  text.translate(str.maketrans("", "", string.punctuation))

    return text 


def add_data_to_2_cols(text , filepath):
    #loading the dataset
    existing_df = pd.read_pickle(filepath)
    # create a dataframe
    new_df = pd.DataFrame({
        existing_df.columns[0] : [text[0]],
        existing_df.columns[1] : [text[1]]
    })
    # concating with existing dataset
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    # check for duplicates
    updated_df = updated_df.drop_duplicates()
    # save data permanently
    updated_df.to_pickle(filepath)


def add_data(text , filepath):
    #loading the dataset
    existing_df = pd.read_pickle(filepath)
    # create a dataframe 
    new_df = pd.DataFrame({
        'country' : [text[0]],
        'description' :[text[1]],
        'hourlyRate' : [text[2]],
        'jobSuccess' : [text[3]],
        'name' : [text[4]],
        'skills' : [text[5]],
        'title' : [text[6]],
        'totalHours' : [text[7]],
        'experience' : [text[8]],
        'pass' : [text[9]],
        'rating' : [text[10]],

    })
    existing_df = existing_df.applymap(lambda x: str(x) if isinstance(x, list) else x)
    new_df = new_df.applymap(lambda x: str(x) if isinstance(x, list) else x)
    # concating with existing dataset
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    # check for duplicates
    updated_df = updated_df.drop_duplicates()
    # save data permanently
    updated_df.to_pickle(filepath)


def vectorization(tags , what):

    df_free = pd.read_pickle('Data/freelancer_2.pkl')
    df_jobs = pd.read_pickle('Data/jobs_2.pkl')
    ##Count Vectorizer
    cv =   TfidfVectorizer(max_features=6000, stop_words='english')
    combined_data = df_jobs['tags_1'].tolist() + df_free['tags_2'].tolist()
    cv.fit(combined_data)
    vector_1 = cv.transform(df_jobs['tags_1']).toarray()
    vector_2 = cv.transform(df_free['tags_2']).toarray()
    ##Find Similarity for finding jobs 
    similarity_finding_jobs = cosine_similarity(vector_2 , vector_1)
    ##Find Similarity for finding freelancer
    similarity_finding_free = cosine_similarity(vector_1 , vector_2)
    if what == 'company':
        return recommend_1(tags , similarity_finding_free)
    else:
        return recommend_2(tags ,similarity_finding_jobs)


def recommend_1(tags , similarity_scores):
    # Load the job and freelancer datasets 
    df_jobs = pd.read_pickle('Data/jobs_2.pkl')
    df_free = pd.read_pickle('Data/freelancer_2.pkl')
    # Check if the tags exist in the job dataset
    if tags not in df_jobs['tags_1'].values:
        return "Alert: Tags not found in the job dataset. Please provide valid tags."
    index = df_jobs[df_jobs['tags_1'] == tags ].index[0]
    distances = sorted(list(enumerate(similarity_scores[index])),reverse=True,key = lambda x: x[1])
    best= []
    for key , value in distances:
      if(value >=0.25):
        best.append(key)

    recommend = []
    for i in best:
        recommend.append(df_free['name'].iloc[i])

    return recommend


def recommend_2(tags , similarity_scores):
    # Load the job and freelancer datasets
    df_jobs = pd.read_pickle('Data/jobs_2.pkl')
    df_free = pd.read_pickle('Data/freelancer_2.pkl')
    # Check if the tags exist in the freelancer dataset
    if tags not in df_free['tags_2'].values:
        return "Alert: Tags not found in the freelancer dataset. Please provide valid tags."
    # finding the index
    index = df_free[df_free['tags_2'] == tags ].index[0]
    # check the similarity score for this index 
    distances = sorted(list(enumerate(similarity_scores[index])),reverse=True,key = lambda x: x[1])
    best= []
    for key , value in distances:
      if(value >=0.25):
          best.append(key)
    
    recommend = []
    for i in best:
        recommend.append((df_jobs['projectId'].iloc[i]))

    return recommend


def get_info(name , password , filepath , what):
    # loading the dataset 
    df = pd.read_pickle(filepath)
    #checking name and password are in the dataset or not
    if (name not in df['name'].values) or (password not in df['pass'].values):
        return "you don't have account"
    # finding name in the dataset
    index_1 = df[df['name'] == name ].index[0]
    # getting the password at index_1
    pass_at_index_1 = df['pass'][index_1]
    # finding the password in the dataset
    index_2 = df[df['pass'] == password].index[0]
    # getting the name at index_2
    name_at_index_2 = df['name'][index_2]
    # checking the password matches with pass_at_index_1
    if pass_at_index_1 == password:
       if what == 'free':
           df = pd.read_pickle('Data/freelancer_2.pkl')
           return vectorization(df['tags_2'][index_1] , what)
       else:
           df = pd.read_pickle('Data/jobs_2.pkl')
           return vectorization(df['tags_1'][index_1] , what)
    # checking the name matches with name_at_index_2
    if name_at_index_2 == name :
       if what == 'free':
           df = pd.read_pickle('Data/freelancer_2.pkl')
           return vectorization(df['tags_2'][index_1] , what)
       else:
           df = pd.read_pickle('Data/jobs_2.pkl')
           return vectorization(df['tags_1'][index_1] , what)
    else :
        return "you don't have account"


def info(recommend , filepath):
    lists = []
    # loading the dataset
    df = pd.read_pickle(filepath)
    for re in recommend:
        index = df[df['name'] == re].index[0]
        # adding the data in the list
        data = {
            'projectId' : [(df['name'][index])],
            'skills' : [df['skills'][index]],
            'title' : [df['title'][index]],
            'country' : [df['country'][index]],
            'hourly' : [(df['hourlyRate'][index])],
            'total_hours' : [(df['totalHours'][index])],
            'rating' : [(df['rating'][index])],
            'experience' :[df['experience'][index]],
            }
        lists.append(data)

    return lists 


if __name__ == '__main__':
    app.run(debug = True)