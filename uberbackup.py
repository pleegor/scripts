import boto3
import datetime
import shutil
import os
import argparse

# Creates archive of jenkins home and pushed archive into s3

today = datetime.date.today()
parser = argparse.ArgumentParser(description='This script will create '
                                             'an archive that will be '
                                             'pushed into S3 bucket. '
                                             'In order to make '
                                             'everything work, you will '
                                             'need to have '
                                             'awscli and boto3 libraries'
                                             ' installed and configured.'
                                             ' ')
parser.add_argument('-destination', type=str,
                    help='provide path where new archive will be stored')
parser.add_argument('-target', type=str,
                    help='provide location of the directory '
                         'that will be archived')
parser.add_argument('-bucket', type=str, help='provide S3 bucket name')
args = parser.parse_args()



def build_archive(name, archived_location, archiving_dir):

    """
     This function will create an archive of Jenkins's home directory
    :param name:  name of the archive
    :param directory: location of Jenkins home directory
    :return: archived
    '''
    """

    archive_name = name + str(today)
    #print(archive_name)
    print('Starting archiving Jenkins home located at:'  + " " +
       archiving_dir)
    archived = shutil.make_archive(archived_location + archive_name,
                            'gztar', archiving_dir)
    print("Archive has been built in:" + " " + archive_name)
    return archived


def push_to_s3(archive, bucket_name):

    """
    :param bucket_name: Name of the bucket where archive is uploaded
    :return:
    """
    print('Starting upload to S3')
    s3 = boto3.resource('s3')
    file_name = 'uberjenkins' + str(today) + '.tar.gz'
    uploaded = s3.Bucket(bucket_name).upload_file(
        archive,
        file_name
    )
    print('File' + " " + file_name + " " + 'has been uploaded')
    return uploaded


def remove_old_archive(file_name, path):
    '''
    This function enforces only one archive to be stored in /tmp
    :param file_name:
    :return:
    '''
    item_list = os.listdir(path)
    for item in item_list:
        if item != file_name + str(today) + '.tar.gz':
            os.chdir(path)
            os.remove(item)
            print(item + " " + 'has been deleted')
        else:
            print('latest present backup is' + " "  + item)
    return item


archive = build_archive('uberjenkins', args.destination, args.target)
upload = push_to_s3(archive, args.bucket)
delete = remove_old_archive('uberjenkins', args.destination)
