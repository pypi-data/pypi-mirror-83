import argparse
import os

from tasq_cli import settings
from tasq_cli.upload import do_upload

from django.utils.text import slugify

from datetime import datetime

def main():
    parser = argparse.ArgumentParser(prog='tasq')
    parser.add_argument('-V', '--version', action='version', version=f'Tasq CLI {settings.VERSION}')
    parser.add_argument('-d', '--dataset-name', action='store', help='set current dataset name')
    parser.add_argument('-c', '--client-id', action='store', help='override client id')
    parser.add_argument('-b', '--bucket-name', action='store', help='override bucket name')

    # NOTE
    # in Python 3.8 you can pass an additional argument to add_subparsers
    # required=True
    subparsers = parser.add_subparsers(dest='action', metavar='action', help='action to run')
    images_parser = subparsers.add_parser('upload', help='upload files')
    images_parser.add_argument('-p', '--path', default=False, help='path to directory with images')
    images_parser.add_argument('-e', '--exclude', help='File extensions to exclude.', action='append', nargs='*')
    images_parser.add_argument('--dry', help='create upload file but dont actually upload anything', action='store_true')

    args = parser.parse_args()
    logger = settings.get_logger()

    logger.info(f'Tasq CLI {settings.VERSION}')

    if not args.path:
        logger.error('Path to upload is required.')
        exit(1)

    # override client id if flag is present
    if args.client_id:
        settings.CLIENT_ID = args.client_id
        logger.info(f'Overriding client id with {settings.CLIENT_ID}')

    # override bucket name if flag is present
    if args.bucket_name:
        if args.bucket_name == 'tasq':
            logger.info('Setting default bucket name gits-active-storage')
            settings.BUCKET = 'gits-active-storage'
        else:
            settings.BUCKET = args.bucket_name
            logger.info(f'Overriding bucket name with {settings.BUCKET}')

    dataset_timestamp = datetime.now().strftime("%Y-%m-%d")
    if args.dataset_name:
        DATASET_NAME = slugify(f'{args.dataset_name}-{dataset_timestamp}')
    else:
        # NOTE
        # This could be set as a default on line 13, but this way we get to
        # inform the user what is happening.
        logger.warning(f'Dataset name required. Setting dataset name to {dataset_timestamp}')
        DATASET_NAME = dataset_timestamp

    if args.action == 'upload':
        settings.dry = args.dry
        do_upload(DATASET_NAME, args.path, args.exclude, settings)
