import os
import sys
from datetime import datetime

from airflow import DAG # Import the DAG class from the airflow module. This is the base class for all the other operators. here operators are tasks
                                                        # hierarchy of operators: DAG -> Task -> Operator
from airflow.operators.python import PythonOperator 

# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Here insert(0) is used to insert the path at the beginning of the list so that the path is searched first. This will be the base path 
# for the python interpreter to search for the modules.

from pipelines.reddit_pipeline import reddit_pipeline # Import the function reddit_pipeline from the reddit_pipeline module
from pipelines.aws_s3_pipeline import upload_s3_pipeline # Import the function upload_s3_pipeline from the aws_s3_pipeline module

default_args = { # Define the default arguments for the DAG
    'owner': 'prasanna kumar kommuri',      
    'start_date': datetime(2024, 6, 18) 
}

file_postfix = datetime.now().strftime("%Y%m%d") # Get the current date in the format YYYYMMDD

dag = DAG( # Define the DAG object with the following arguments
    dag_id='etl_reddit_pipeline', # Unique identifier for the DAG
    default_args=default_args,    # Default arguments for the DAG
    schedule_interval='@daily',  # Defines the interval at which the DAG should run. Here it is set to daily
    catchup=False,           # If set to False, the scheduler will only create a DAG run for the most recent interval
                            # If set to True, the scheduler will create a DAG run for all the intervals that were missed while the DAG
                            # was paused or inactive. for example if the DAG was paused for 2 days, then the scheduler will create 2 DAG runs
    tags=['reddit', 'etl', 'pipeline']  # Tags to categorize the DAG. This is useful when there are multiple DAGs in the system
                                        # and you want to group them based on some criteria like the type of data they process.
                                        # Later you can filter the DAGs based on these tags. This will help in monitoring and debugging
)

# extraction from reddit 

extract = PythonOperator(            # Define a PythonOperator task with the following arguments
    task_id='reddit_extraction',     # Unique identifier for the task
    python_callable=reddit_pipeline, # The function to be called by the task
    op_kwargs={                      # The arguments to be passed to the function
        'filename': f'reddit_{file_postfix}', # The filename for the output file
        'subreddit': 'dataengineering', # The subreddit from which the data has to be extracted
        'time_filter': 'day',        # The time filter to be applied to the posts
        'limit': 100                 # The maximum number of posts to be extracted    
    },
    dag=dag                          # The DAG object to which the task has to be added     DAG <-- Task <-- Operator
)

# upload to s3                      # Define a PythonOperator task with the following arguments
upload_s3 = PythonOperator(         # Unique identifier for the task
    task_id='s3_upload',            # The function to be called by the task
    python_callable=upload_s3_pipeline, # The arguments to be passed to the function
    dag=dag                         # The DAG object to which the task has to be added       DAG <-- Task <-- Operator
)

extract >> upload_s3                # Set the task dependencies. Here the upload_s3 task is dependent on the extract task.