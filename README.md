# AI-Based-Recommendation-System

Objective: This project is an AI-powered recommendation system for freelancers and companies. It matches freelancers with jobs and vice versa using similarity metrics on their respective skills, titles, and other parameters. Built using **Flask**, **scikit-learn**, and **pandas**.

## Features

- **Freelancer Recommendations:** Suggests jobs for freelancers based on their skills and other attributes.
- **Job Recommendations:** Matches companies with the most suitable freelancers for their projects.
- **User Authentication:** Allows freelancers and companies to log in securely.
- **Data Storage:** Stores and updates user and job data in `.pkl` files.


|File             	| Description                                     |
|-------------------|----------------------------------------------   |
|freelancer_2.pkl	  |  Stores freelancer names and preprocessed tags. |
|jobs_2.pkl	        |  Stores job project IDs and preprocessed tags.  |
|update_free.pkl	  |  Detailed freelancer information.               |
|update_jobs.pkl    |  Detailed job information.                      |


## Project Structure

AI-recommendation/
|
├── backend/                 # Backend folder
│   ├── app.py               # Main Flask app
|   ├── AI_freelancer.ipynb  # Jupyter Notebook for analysis
│   └── Data/                # Data storage folder
│       ├── freelancer_2.pkl
│       ├── jobs_2.pkl
│       ├── update_free.pkl
│       └── update_jobs.pkl
|
├── static/                 # Static assets
│   ├── Scripts/
│   │   └── Home.js         # JavaScript for frontend
│   └── Styles/             # CSS for styling
│       ├── form.css
│       ├── index.css
│       └── recommend.css
|
├── templates/              # HTML templates
│   ├── form_freelancer.html
│   ├── form_jobs.html
│   ├── Home.html
│   ├── login_freelancer.html
│   ├── login_jobs.html
│   └── recommendations.html
|
└── README.md               # Documentation (this file)


| **Technology**    | **Purpose**                   |
|-------------------|-------------------------------|
| Flask             | Backend Web Framework         |
| Pandas            | Data Manipulation             |
| Scikit-learn      | Vectorization & Similarity    |
| HTML/CSS/JS       | Frontend                      |
| Pickle            | Data Storage                  |

## Routes
|Route	Method	             |  Description                                  |
|---------------------------|---------------------------------------------- |
|/	GET	                     |  Renders the homepage.                        |
|/freelancer	GET	           |  Renders freelancer form.                     |
|/jobs	GET	                 |  Renders job form.                            |
|/login_1 GET	             |  Processes freelancer login and recommendations.|
|/login_2	POST/GET	       |  Processes job login and recommendations.      |
|/submit1 / /submit2	GET    |  Redirects to login pages.                     |
|/signin_1 / /signin_2	POST |	Validates login credentials.                  |


