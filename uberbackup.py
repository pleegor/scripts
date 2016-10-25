import boto3
import datetime
import shutil
import os
import argparse

# Creates archive of jenkins home and pushed archive into s3

today = datetime.date.today()
parser = argparse.ArgumentParser(description='This script will create '
                                             'an archive and will push '
                                             'it into S3 bucket')
parser.add_argument('-destination', type=str,
                    help='enter path where new archive will be stored')
parser.add_argument('-target', type=str,
                    help='enter location of the directory '
                         'that will be archived')
# parser.add_argument('-bucket-name', type=str,
#                     help='enter S3 bucket name where archive will '
#                          'be pushed to')
args = parser.parse_args()



def build_archive(name):

    """
     This function will create an archive of Jenkins's home directory
    :param name:  name of the archive
    :param directory: location of Jenkins home directory
    :return: archived
    '''
    """

    archive_name = name + str(today)
    archived_location = args.destination
    #print(archive_name)
    archiving_dir = args.target
    print('Starting archiving Jenkins home located at:'  + " " +
       archiving_dir)
    archived = shutil.make_archive(archived_location + archive_name,
                            'tar', archiving_dir)
    print("Archive has been built in:" + " " + archive_name)
    return archived


def push_to_s3(archive, bucket_name):

    """
    :param bucket_name: Name of the bucket where archive is uploaded
    :return:
    """
    print('Starting upload to S3')
    s3 = boto3.resource('s3')
    file_name = 'uberjenkins' + str(today) + '.tar'
    uploaded = s3.Bucket(bucket_name).upload_file(
        archive,
        file_name
    )
    print('File' + " " + file_name + " " + 'has been uploaded')
    return uploaded


def remove_old_archive(file_name):
    '''
    This function enforces only one archive to be stored in /tmp
    :param file_name:
    :return:
    '''
    path = args.destination
    item_list = os.listdir(path)
    for file in item_list:
        if file != file_name + str(today) + '.tar':
            os.chdir(path)
            os.remove(file)
            print(file + " " + 'has been deleted')
        else:
            print('latest present backup is' + " "  + file)
    return file


archive = build_archive('uberjenkins')
upload = push_to_s3(archive, 'cbit-logging')
delete = remove_old_archive('uberjenkins')