import boto3
import datetime
import shutil
import os

# Creates archive of jenkins home and pushes archive into s3

today = datetime.date.today()



def build_archive(name):

    """
     This function will create an archive of Jenkins's home directory
    :param name:  name of the archive
    :return: archived
    '''
    """

    archive_name = name + str(today)
    archived_location = <Path>
    #archived_location is path where archive will be stored
    archiving_dir = <path>
    #archived_dir is path where archiving file is currently located
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
    file_name = <name> + str(today) + '.tar'
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
    #provide path where archoves are locally stored
    path = <path>
    item_list = os.listdir(path)
    for file in item_list:
        if file != file_name + str(today) + '.tar':
            os.chdir(path)
            os.remove(file)
            print(file + " " + 'has been deleted')
        else:
            print('latest present backup is' + " "  + file)
    return file


archive = build_archive(<name>)
upload = push_to_s3(archive, <bucket name>)
delete = remove_old_archive(<name>)