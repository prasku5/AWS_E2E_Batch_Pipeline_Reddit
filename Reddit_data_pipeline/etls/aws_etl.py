import s3fs
from utils.constants import AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY

def connect_to_s3():                                     # Connect to the s3 bucket
    try:                                                 # Try to connect to the s3 bucket
        s3 = s3fs.S3FileSystem(anon=False,               # Set anon to False to connect to the s3 bucket using the access key and secret key
                               key= AWS_ACCESS_KEY_ID,
                               secret=AWS_ACCESS_KEY)
        return s3                                        # Return the s3 object using the access key and secret key provided
    except Exception as e:                               # If there is an exception, print the exception              
        print(e)

def create_bucket_if_not_exist(s3: s3fs.S3FileSystem, bucket:str):      # Create a bucket if it does not exist
    try:
        if not s3.exists(bucket):                        # Check if the bucket exists
            s3.mkdir(bucket)                             # If the bucket does not exist, create the bucket
            print("Bucket created")                      # Print a message that the bucket is created
        else :
            print("Bucket already exists")               # If the bucket exists, print a message that the bucket already exists
    except Exception as e:                               # If there is an exception, print the exception
        print(e)


def upload_to_s3(s3: s3fs.S3FileSystem, file_path: str, bucket:str, s3_file_name: str): # Upload the file to the s3 bucket with the given name and path
    try:
        s3.put(file_path, bucket+'/raw/'+ s3_file_name)   # Upload the file to the s3 bucket
        print('File uploaded to s3')                      # Print a message that the file is uploaded to the s3 bucket
    except FileNotFoundError:
        print('The file was not found')                  # If the file is not found, print a message that the file was not found