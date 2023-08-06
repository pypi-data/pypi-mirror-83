import traceback

from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from tqdm import tqdm

from .log import init_logger


class BigQueryClient:
    def __init__(self, project_id):
        self.logger = init_logger(__name__, testing_mode=False)
        self.client = bigquery.Client(project_id)

    def run_query(self, QUERY, as_dataframe=False, legacy_sql=True):
        job_config = bigquery.QueryJobConfig()
        job_config.use_legacy_sql = legacy_sql
        query_job = self.client.query(QUERY, job_config=job_config)
        result = query_job.result()
        assert query_job.state == 'DONE'
        if as_dataframe:
            return result.to_dataframe()
        return result

    def table_exists(self, table_name, dataset_name):
        dataset_ref = self.client.dataset(dataset_name)
        table_ref = dataset_ref.table(table_name)
        try:
            table = self.client.get_table(table_ref)
            return table
        except NotFound:
            self.logger.warn('{} does not exist in {}'.format(
                table_name, dataset_name))
            return False

    def dataset_exists(self, dataset_name):
        dataset_ref = self.client.dataset(dataset_name)
        try:
            dataset = self.client.get_dataset(dataset_ref)
            return dataset
        except NotFound:
            self.logger.warn(
                '{} does not exist in this project'.format(dataset_name))
            return False

    def list_datasets(self):
        return [dataset.dataset_id for dataset in self.client.list_datasets()]

    def list_tables(self, dataset_id):
        return [table.table_id for table in self.client.list_tables(dataset_id)]

    def get_table(self, table_name, dataset_name):
        return self.table_exists(table_name, dataset_name)

    def get_dataset(self, dataset_name):
        return self.dataset_exists(dataset_name)

    def create_table(self, table_name, dataset_name, schema):
        dataset_ref = self.client.dataset(dataset_name)
        table_ref = dataset_ref.table(table_name)
        table = bigquery.Table(table_ref, schema=[bigquery.SchemaField(*schema_entry)
                                                  for schema_entry in schema])
        return self.client.create_table(table)

    def create_dataset(self, dataset_name, description=''):
        dataset_ref = self.client.dataset(dataset_name)
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = 'EU'
        dataset.description = description
        dataset = self.client.create_dataset(dataset)

    def delete_table(self, table_name, dataset_name):
        dataset_ref = self.client.dataset(dataset_name)
        table_ref = dataset_ref.table(table_name)
        self.client.delete_table(table_ref)

    def insert_rows(self, table_name, dataset_name, data, chunk_size=1, descr=None):
        for i in tqdm(range(0, len(data), chunk_size), desc=descr):
            chunk = data[i:i + chunk_size]
            try:
                errors = self.client.insert_rows_json(
                    self.get_table(table_name, dataset_name), chunk)
                assert errors == []
            except AssertionError as e:
                self.logger.error(traceback.format_exc())
                self.logger.error("Failed data: {}".format(chunk))


class BQUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_query(florist, record_type, datum, start, end):
        return """
                        SELECT
                            *
                        FROM
                            [{}.{}]
                        WHERE
                            DATE({}) >= "{}"
                            AND DATE({}) <= "{}"
        """.format(florist, record_type, datum, start, datum, end)
