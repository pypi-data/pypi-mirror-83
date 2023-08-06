import json
from typing import Dict

import boto3


def get_secret(secret_name: str, region: str) -> Dict[str, str]:
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region
    )
    secret_string = client.get_secret_value(
        SecretId=secret_name
    )['SecretString']
    return json.loads(secret_string)
