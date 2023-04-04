# Create clients for IAM, EC2, S3 and Redshift¶
import boto3
import configparser
from time import sleep


def create_clients(AWS_REGION, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY):
    print("Creating clients for IAM, EC2, S3 and Glue")
    s3 = boto3.resource('s3',
                        region_name=AWS_REGION,
                        aws_access_key_id=AWS_ACCESS_KEY,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                        )
    return s3


def create_s3(s3, S3_BUCKET_NAME, AWS_REGION):
    print("Creating AWS S3")
    try:
        s3.create_bucket(Bucket=S3_BUCKET_NAME, CreateBucketConfiguration={
            'LocationConstraint': AWS_REGION
        })
    except Exception as e:
        if 'BucketAlreadyOwnedByYou' in str(e):
            print(f"Bucket '{S3_BUCKET_NAME}' already exists.")
            return
    # wait until bucket is created
    while True:
        response = [bucket.name for bucket in s3.buckets.all()]
        for bucket in response:
            if bucket == S3_BUCKET_NAME:
                print(f"Bucket '{S3_BUCKET_NAME}' has been created.")
                return
        print("Waiting for S3 bucket to be created...")
        sleep(10)


def create_s3_directories(s3, S3_BUCKET_NAME, directories):
    for directory in directories:
        bucket = s3.Bucket(S3_BUCKET_NAME)
        s3_key = directory + '/'
        try:
            bucket.Object(s3_key).load()
            print(
                f'S3 directory s3://{S3_BUCKET_NAME}/{s3_key} already exists.')
        except:
            print(f'Creating S3 directory s3://{S3_BUCKET_NAME}/{s3_key}')
            bucket.put_object(Key=s3_key)
            # Wait for the directory to be created
            while True:
                try:
                    bucket.Object(s3_key).load()
                    print(
                        f'S3 directory s3://{S3_BUCKET_NAME}/{s3_key} created successfully.')
                    break
                except:
                    print(
                        f'Waiting for S3 directory s3://{S3_BUCKET_NAME}/{s3_key} to be created...')
                    sleep(5)


def main():
    config = configparser.ConfigParser()
    config.read('aws.cfg')

    AWS_REGION = config.get('AWS', 'AWS_REGION')
    AWS_ACCESS_KEY = config.get('AWS', 'AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = config.get('AWS', 'AWS_SECRET_ACCESS_KEY')
    S3_BUCKET_NAME = config.get('S3', 'S3_BUCKET_NAME')

    s3 = create_clients(
        AWS_REGION, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)

    create_s3(s3, S3_BUCKET_NAME, AWS_REGION)
    directories = ['customer',
                   'step_trainer', 'accelerometer']
    create_s3_directories(s3, S3_BUCKET_NAME, directories)


if __name__ == '__main__':
    main()
