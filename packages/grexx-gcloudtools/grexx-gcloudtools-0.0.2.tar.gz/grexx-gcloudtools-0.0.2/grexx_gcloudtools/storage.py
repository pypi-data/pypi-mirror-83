from google.cloud import storage

from .log import init_logger


class StorageClient:

    def __init__(self):
        self.logger = init_logger(__name__, testing_mode=False)
        self.client = storage.Client()

    def lookup_bucket(self, bucket_name):
        return self.client.lookup_bucket(bucket_name)

    def upload_file(self, bucket_name, file_name, file_path):
        bucket = self.lookup_bucket(bucket_name)
        if bucket is not None:
            blob = bucket.blob(file_name)

            blob.upload_from_filename(file_path)

            self.logger.info('File {} uploaded to {}.'.format(
                file_path,
                file_name))
        else:
            self.logger.warn("Bucket not found!")

    def download_file(self, bucket_name, file_name, file_path):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)

        blob.download_to_filename(file_path)

        self.logger.info('Blob {} downloaded to {}.'.format(
            file_name,
            file_path))
