import boto3
import random

AWS_REGION = "us-east-2"

client = boto3.client('cloudwatch', region_name = 'us-east-2', aws_access_key_id = 'AKIAXPCCGXHHET6LYOPI', aws_secret_access_key = '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')


for i in range(100):
    response = client.put_metric_data(
        Namespace='Web Metric',
        MetricData=[
            {
                'MetricName': 'Number of visits',
                'Dimensions': [
                    {
                        'Name': 'Device',
                        'Value': 'Android'
                    }, {
                        'Name': 'page',
                        'Value': 'index.html'
                    }
                ],
                'Value': random.randint(10000, 100000),
                'Unit': 'Count'
            },
        ]
    )

    print(response)