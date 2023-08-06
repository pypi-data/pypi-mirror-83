import boto3
from botocore.config import Config


def get_stack_output(region_name: str, stack_name: str, output_key: str) -> str:
    client = boto3.client('cloudformation', config=Config(region_name=region_name))
    outputs = client.describe_stacks(StackName=stack_name)[0]['Outputs']
    output = next(filter(lambda x: x['OutputKey'] == output_key, outputs), None)
    if not output:
        raise 'Output with key "%s" not found in stack "%s"' % (output_key, stack_name)
    return output['OutputValue']
