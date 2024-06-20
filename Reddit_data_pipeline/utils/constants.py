import configparser
import os

parser = configparser.ConfigParser()                                                # Create a ConfigParser object
parser.read(os.path.join(os.path.dirname(__file__), '../config/config.conf'))       # Read the configuration file

CLIENT_SECRET = parser.get('api_keys', 'reddit_secret_key')                         # Get the client secret from the configuration file
CLIENT_ID = parser.get('api_keys', 'reddit_client_id')                              # Get the client id from the configuration file

DATABASE_HOST =  parser.get('database', 'database_host')                            # Get the database host from the configuration file 
DATABASE_NAME =  parser.get('database', 'database_name')                            # Get the database name from the configuration file 
DATABASE_PORT =  parser.get('database', 'database_port')                            # Get the database port from the configuration file
DATABASE_USER =  parser.get('database', 'database_username')                        # Get the database username from the configuration file
DATABASE_PASSWORD =  parser.get('database', 'database_password')                    # Get the database password from the configuration file

#AWS
AWS_ACCESS_KEY_ID = parser.get('aws', 'aws_access_key_id')                          # Get the AWS access key id from the configuration file
AWS_ACCESS_KEY = parser.get('aws', 'aws_secret_access_key')                         # Get the AWS secret access key from the configuration file 
AWS_REGION = parser.get('aws', 'aws_region')                                        # Get the AWS region from the configuration file
AWS_BUCKET_NAME = parser.get('aws', 'aws_bucket_name')                              # Get the AWS bucket name from the configuration file

INPUT_PATH = parser.get('file_paths', 'input_path')                                  # Get the input path from the configuration file
OUTPUT_PATH = parser.get('file_paths', 'output_path')                                # Get the output path from the configuration file

POST_FIELDS = (                                                                     # Define the fields to extract from the Reddit posts          
    'id',
    'title',
    'score',
    'num_comments',
    'author',
    'created_utc',
    'url',
    'over_18',
    'edited',
    'spoiler',
    'stickied'
)