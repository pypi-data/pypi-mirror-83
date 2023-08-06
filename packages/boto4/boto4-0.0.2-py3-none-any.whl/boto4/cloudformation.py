import boto3


def get_stack_output(stack_name: str, output_key: str) -> str:
    outputs = boto3.client('cloudformation').describe_stacks(StackName=stack_name)[0]['Outputs']
    output = next(filter(lambda x: x['OutputKey'] == output_key, outputs), None)
    if not output:
        raise 'Output with key "%s" not found in stack "%s"' % (output_key, stack_name)
    return output['OutputValue']
