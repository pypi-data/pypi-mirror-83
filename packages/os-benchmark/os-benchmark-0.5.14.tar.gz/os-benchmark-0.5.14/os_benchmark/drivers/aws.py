"""
.. note::
  This driver requires `boto3`_.

Configuration
~~~~~~~~~~~~~

.. code-block:: yaml

  ---
  aws:
    driver: aws
    aws_access_key_id: <your_ak>
    aws_secret_access_key: <your_sk>
    endpoint_url: https://s3.<region_id>.amazonaws.com
    region_name: <region_id>

.. _boto3: https://github.com/boto/boto3
"""
from os_benchmark.drivers import s3


class Driver(s3.Driver):
    """AWS S3 Driver"""
    id = 'aws'

    def _get_create_request_params(self, name, acl, **kwargs):
        params = super()._get_create_request_params(name, acl, **kwargs)
        params['CreateBucketConfiguration'] = {
            'LocationConstraint': self.kwargs['region_name']
        }
        return params

    def get_url(self, bucket_id, name, **kwargs):
        url = '%s/%s/%s' % (self.kwargs['endpoint_url'], bucket_id, name)
        return url

    def sql_select(self, bucket_id, name, expression, **kwargs):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.select_object_content
        """
        params = {
            'Bucket': bucket_id,
            'Key': name,
            'Expression': expression,
            'ExpressionType': 'SQL',
            'InputSerialization': {
                'CSV': {
                    'FileHeaderInfo': 'USE',
                    'CompressionType': 'None',
                }
            },
            'OutputSerialization': {
                'CSV': {
                }
            }
        }
        response = self.s3.select_object_content(**params)
        import ipdb; ipdb.set_trace()
