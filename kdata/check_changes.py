#!/home/neri/.virtualenvs/kdata/bin/python
import os
from datetime import datetime, timedelta
from multiprocessing.pool import ThreadPool
from os.path import isfile, join

import boto
import boto.s3.connection


access_key = 'secret'
secret_key = 'secret'
my_folder = 'imagetm'
bucket_name = "marks"
change_folder = []


conn = boto.connect_s3(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    host='objects.dreamhost.com',
    calling_format=boto.s3.connection.OrdinaryCallingFormat(),
    )


bucket = conn.get_bucket(bucket_name)


def _get_filenames(root_folder):
    folders = os.listdir(root_folder)
    for folder in folders:
        if isfile(join(root_folder, folder)):
            yield join(root_folder, folder)
        else:
            date_change = datetime.fromtimestamp(os.path.getmtime(join(root_folder, folder)))
            with open('check.log', 'a') as log_file:
                log_file.write(folder)
                log_file.write(str(date_change))
            if date_change + timedelta(minutes=30) > datetime.now():
                change_folder.append(join(root_folder, folder))
                for filename in _get_filenames(join(root_folder, folder)):
                    yield filename


def _set_file(filename):
    key_name = filename.replace(my_folder, '')
    try:
        bucket_key = bucket.new_key(key_name)
        with open(filename, 'rb') as image_file:
            bucket_key.set_contents_from_file(image_file)
        bucket_key.set_canned_acl('public-read')
    except Exception as e:
        print("{} for {}".format(e, filename))


def main():
    with open('check.log', 'a') as log_file:
        log_file.write(str(datetime.now()))
    results = []
    pool = ThreadPool(processes=32)
    for filename in _get_filenames(my_folder):
        with open('check.log', 'a') as log_file:
            log_file.write(filename)
        if all(filename.replace(my_folder, '') != key for key in bucket.list()):
            results.append(pool.apply_async(_set_file, (filename,)))
    while not(all(a_thread.ready() for a_thread in results)):
        pass
    for folder in change_folder:
        for key in bucket.list():
            if key.name.startswith(folder.replace(my_folder, '')[1:]):
                if not any(key.name.endswith(filename) for filename in os.listdir(folder)):
                    print("Delete: ", key.name)
                    bucket.delete_key(key.name)
    with open('check.log', 'a') as log_file:
        log_file.write('\n')


if __name__ == "__main__":
    main()

