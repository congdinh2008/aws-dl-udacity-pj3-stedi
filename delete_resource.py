from botocore.exceptions import ClientError
import time
import configparser
from create_resource import create_clients

def delete_s3_bucket(s3, S3_BUCKET_NAME):
    """
    Delete an S3 object and wait for the deletion to be completed.

    :param s3: client
    :param S3_BUCKET_NAME: string
    :return: True if the referenced object was deleted, otherwise False
    """

    try:
        bucket = s3.Bucket(S3_BUCKET_NAME)
        # Delete all objects in the bucket
        bucket.objects.all().delete()

        # Delete the bucket
        bucket.delete()
        print(f'Successfully deleted S3 bucket: {S3_BUCKET_NAME}')
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketNotEmpty':
            print(f'S3 bucket {S3_BUCKET_NAME} is not empty. Deleting all objects inside the bucket...')
            
            s3.objects.all().delete()
            s3.delete_bucket(Bucket=S3_BUCKET_NAME)
            print(f'Successfully deleted S3 bucket: {S3_BUCKET_NAME}')
        elif e.response['Error']['Code'] == 'NoSuchBucket':
            print(f'S3 bucket {S3_BUCKET_NAME} does not exist')
        else:
            print(f'Error deleting S3 bucket {S3_BUCKET_NAME}: {e}')
            return False

    # Wait for the bucket to be deleted
    while True:
        try:
            s3.meta.client.head_bucket(Bucket=S3_BUCKET_NAME)
            time.sleep(10)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                print(f'S3 bucket {S3_BUCKET_NAME} successfully deleted')
                break
            else:
                print(f'Error waiting for S3 bucket {S3_BUCKET_NAME} to be deleted: {e}')
                return False

    return True

def main():
    config = configparser.ConfigParser()
    config.read('aws.cfg')

    AWS_REGION = config.get('AWS', 'AWS_REGION')
    AWS_ACCESS_KEY = config.get('AWS', 'AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = config.get('AWS', 'AWS_SECRET_ACCESS_KEY')
    S3_BUCKET_NAME = config.get('S3', 'S3_BUCKET_NAME')

    ec2, s3, iam, glue = create_clients(
        AWS_REGION, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)

    delete_s3_bucket(s3, S3_BUCKET_NAME)

if __name__ == '__main__':
    main()