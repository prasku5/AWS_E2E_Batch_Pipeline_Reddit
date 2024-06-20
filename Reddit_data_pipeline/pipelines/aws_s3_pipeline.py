from etls.aws_etl import connect_to_s3, create_bucket_if_not_exist, upload_to_s3
from utils.constants import AWS_BUCKET_NAME


def upload_s3_pipeline(ti): # ti is the task instance which is passed by the airflow to the function. This is used to pull the data from the previous task

    file_path = ti.xcom_pull(task_ids='reddit_extraction', key='return_value') # we are pulling the file path from the previous task

    s3 = connect_to_s3()                                                       # connecting to s3. This is a core function which we defined as part of the ETL process.
    create_bucket_if_not_exist(s3, AWS_BUCKET_NAME)               # creating bucket if not exists. This is a core function which we defined as part of the ETL process.
    upload_to_s3(s3, file_path, AWS_BUCKET_NAME, file_path.split('/')[-1])     # uploading the file to s3.