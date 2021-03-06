""" This script updates the gitalb job results to respective job readme.md """

# import sys to get command line arguments
import sys
# import re to find regular expression
import re
# import github to use github api 
from github import Github 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--job_id",
       help="github job id to create gitlab job_url")
parser.add_argument("--stage",
       help="github jobs stage")
parser.add_argument("--test_desc",
       help="gitlab job description")
parser.add_argument("--test_result",
       help=" github job result: PASS or FAIL")
parser.add_argument("--time_stamp",
       help="time of gitlab job run")
parser.add_argument("--token",
       help="github authentication token")
parser.add_argument("--test_name",
       help="test name")
parser.add_argument("--job_name",
       help="job name")
parser.add_argument("--platform",
       help="platform")


args = parser.parse_args()
job_id = args.job_id
stage = args.stage
test_desc = args.test_desc
test_result = args.test_result
time_stamp = args.time_stamp
token = args.token
test_name = args.test_name
job_name = args.job_name
platform = args.platform

github_token = Github(token)
repo = github_token.get_repo("mayadata-io/oep-e2e-results")
contents = repo.get_contents(job_name+"/README.md")
file = repo.get_contents(contents.path)
file_path = contents.path
file_content=str(file.decoded_content)
content_list = file_content.split('\n')

# Number of retries 
file_update_retries = 5

# github job log url using job_id
job_url ="<a href= \"https://gitlab.mayadata.io/oep/oep-e2e-gcp/-/jobs/{0}\">{0}</a>".format(job_id)

def fetch_file_content():
    # fetching file contents of github file_path readme.md
    file = repo.get_contents(file_path)
    file_content=str(file.decoded_content, 'utf-8')
    content_list = file_content.split('\n')

    # updating result's table if the table is already there
    if file_content.find('|')>0:
        new_job = '|     {}           |  {}           | {}  | {} | {} |'.format(job_url,test_desc,time_stamp,platform,test_result)
        index = content_list.index('| Job ID |   Test Description         | Execution Time | Platform |Test Result   |')
        content_list.insert(index+2,new_job)
        updated_file_content = ('\n').join(content_list)
        
    # creating result's table for first job result entry 
    else:
        updated_file_content =  '| Job ID |   Test Description         | Execution Time | Platform |Test Result   |\n'
        updated_file_content = updated_file_content + (' |---------|---------------------------| --------------| -------- |--------|\n')
        updated_file_content = updated_file_content + (' |    {}   |  {}           |  {}     |{}  |{}  |\n'.format(job_url,test_desc,time_stamp,platform,test_result))
        index = len(content_list)
        content_list.insert(index, updated_file_content)
        updated_file_content = ('\n').join(content_list)
    return file, updated_file_content

file, updated_file_content = fetch_file_content()

# github commit message 
commit_message = "new job result update"
exception = ''
# file update retry iterator
loop_itr = 0
# file update try count
try_count = 5

# github exception handling
print("Trying to update readme.md file at path: {}".format(file_path))
try:
    print("README.md content update try: {}".format(try_count))
    try_count += 1
    repo.update_file(file_path, commit_message, updated_file_content, file.sha)
    print("Readme.md updated successfully")
except github.GithubException as e:
    exception = e
    print("Error message:{}".format(exception.data['message']))
    # retryng updating readme.md after refetching the file contents
    while loop_itr < file_update_retries:
     # 409 is github exception status in case of conflict
     # retry committing to respective job's readme.md in case of conflict by refetching readme.md file contents
     if exception.status == 409:
      # exception handling for github exception status: 409
      try:
       print("README.md content update try: {}".format(try_count))
       # refetch github readme.md file content
       file,updated_file_content = fetch_file_content()
       try_count += 1
       # retry committing readme.md file 
       repo.update_file(file_path, commit_message, updated_file_content, file.sha)
       print("Readme.md updated successfully")
       # exit the loop as file updated successfully
       break
      except github.GithubException as e:
       exception = e
       print("Error message:{}".format(exception.data['message']))
       loop_itr = loop_itr + 1
     # exit the loop if github exception is not 409
     else:
       print("Readme.md updation failed")
       break
