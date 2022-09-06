## Coding Challenge

## We've got a lot of data on our carers, but we want to give clients our top carers first!
## The aim of this challenge is to design a carer scoring system in Python based on the data in order to serve the **best carers** first in our search results. The best carers are the ones most likely for a client to click on them!
## You can use as many fields as you like from the data but should try to design the best scoring algorithm you can think of. You might want to include their average review score or maybe weight the review score lower if they have image problems. 
## It's up to you, but think about how the various fields can be combined into a single score representing the best carer we should show our clients.
## We've provided a list of 600 carers and their fields that you can use. 
## Feel free to search / learn as much as you like, the task is meant to simulate a real world problem.

# Tasks
##- Ingest the CSV to your script
##- Score each carer based on your own system
##- Sort the carers by highest score first
##- Upload your code and results to a GitHub repository

# Bonus

##- Comment your code thoroughly, explaining why you chose your scoring system.
##- Make your code meet pep8 linting standards
##- Write some tests for your code
##- Spot the error in the data (numerical impossibility) - 
   # 93 rows all started caring before the age of 18, 10 rows at less than age 10
   # 152 rows have a >0 review score but zero review count
   # 249 rows have >0 num_reviews but zero previous clients
   # all avg-review is between expected 0.01-4.99
   # all img_problems is between expected 0-8
   # all age is between working ages 18-65



# Fields
##- **id** - A unique ID for this carer
##- **first_name** - The carers first name
##- **last_name** -  The carers last name
##- **num_reviews** - The number of reviews they have
##- **avg_review** - The average score they got across their reviews out of 5. e.g. 5* + 4* = 4.5*
##- **img_problems** - We track 8 problems with carers images e.g. "Not Smiling", "Blurry", "Too small" etc. The higher the number, the more problems there are and the worse the picture is.
##- **type** - We have three types of carer, "basic", "advanced", "expert". An expert carer has more skills than an advanced carer and an advanced carer has more skills than a basic carer.
##- **num_previous_clients** - How many clients the carer had had via PrimeCarers.
##- **days_since_login** - How many days ago the carer last logged in.
##- **age** - The age of the carer
##- **years_experience** - The years experience that the carer has in the field.

import csv # for csv file handling

### Local variables
carer_data_file_path = "data.csv" # current path to data file
carer_export_file_path = "export.csv" # current path to data file


def carer_score(carer): # function to score the carers
    #Scoring based as the following
        # avg_review  ##  as the base line of the carers work
        # - 5% for each img_problems  ##  to promote better images 
        # - 1% for each days_since_login  ##  to promote active site users
        # + 2% for each years_experience  ##  to promote experienced carers
    
    try: # scored on avg_review
        score = float(carer.get('avg_review'))
    except ValueError as ve:
        print("Error in avg_review data for id ", carer.get('id'), ve)
        score = 0

    try: # weighted - 5% for each img_problems (0-8)
        score = score - (score * (( float(carer.get('img_problems')) + 1.0 ) * 0.05 ))
    except ValueError as ve:
        print("Error in img_problems data for id ", carer.get('id'), ve)
        score = 0

    try: # weighted - 1% for each day not logged in to promote active site users
        score = score - (score * (( float(carer.get('days_since_login')) + 1.0 ) *0.01 ))
    except ValueError as ve:
        print("Error in days_since_login data for id ", carer.get('id'), ve)
        score = 0
    
    try: # weighted + 2% for year of experience to show more experienced carers first
        score = score + (score * (( float(carer.get('years_experience')) + 1.0 ) *0.02 ))
    except ValueError as ve:
        print("Error in years_experience data for id ", carer.get('id'), ve)
        score = 0
    
    score = int(score*1000)/1000

    return score

## Main 

# open csv file and copy into carer_list[] with headers as indices
try: 
    with open(carer_data_file_path, 'r', encoding='utf-8') as file:
        csv_file = csv.DictReader(file)
        carer_list = []
        for row in csv_file:
            carer_list.append(dict(row))

finally: # close file on error
    file.close()



# add the score field to each row in the list
for i in range(len(carer_list)): 
    carer_list[i]['score'] = carer_score(carer_list[i])



# sort the list with the highest scores first
carer_list.sort(key=lambda x: x.get('score'), reverse=True) 



# open csv file and export carer_list[] with headers 
try: 
    with open(carer_export_file_path, 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['id',
                      'first_name',
                      'last_name',
                      'num_reviews',
                      'avg_review',
                      'img_problems',
                      'type',
                      'num_previous_clients',
                      'days_since_login',
                      'age',
                      'years_experience',
                      'score']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(carer_list)


finally: # close file on error
    file.close()
