import traceback

import googleapiclient.discovery

from .log import init_logger


class CloudML:

    logger = init_logger(__name__, testing_mode=False)
    service = googleapiclient.discovery.build('ml', 'v1')

    def __init__(self):
        pass

    @staticmethod
    def train():
        training_inputs = {'scaleTier': 'CUSTOM',
                           'masterType': 'complex_model_m',
                           'workerType': 'complex_model_m',
                           'parameterServerType': 'large_model',
                           'workerCount': 9,
                           'parameterServerCount': 3,
                           'packageUris': ['gs://my/trainer/path/package-0.0.0.tar.gz'],
                           'pythonModule': 'trainer.task',
                           'args': ['--arg1', 'value1', '--arg2', 'value2'],
                           'region': 'us-central1',
                           'jobDir': 'gs://my/training/job/directory',
                           'runtimeVersion': '1.12',
                           'pythonVersion': '3.5'}

    @staticmethod
    def list_models(project):
        parent = 'projects/{}'.format(project)
        try:
            response = CloudML.service.projects().models().list(
                parent=parent
            ).execute()

            if 'error' in response:
                logger.error(response['error'])

            return response['models']
        except:
            logger.error(traceback.format_exc())

    @staticmethod
    def predict_json(project, model, instances, version=None):
        """Send json data to a deployed model for prediction.
        Args:
            project (str): project where the Cloud ML Engine Model is deployed.
            model (str): model name.
            instances ([[float]]): List of input instances, where each input
            instance is a list of floats.
            version: str, version of the model to target.
        Returns:
            Mapping[str: any]: dictionary of prediction results defined by the
                model.
        """
        name = 'projects/{}/models/{}'.format(project, model)

        if version is not None:
            name += '/versions/{}'.format(version)

        # TODO: ROBO-147
        try:
            response = CloudML.service.projects().predict(
                name=name,
                body={'instances': instances}
            ).execute()

            if 'error' in response:
                logger.warn(response['error'])
                return [0] * len(instances)

            return response['predictions']
        except:
            logger.warn(traceback.format_exc())
            return [0] * len(instances)
