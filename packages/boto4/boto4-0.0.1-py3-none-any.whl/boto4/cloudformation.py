import boto3


def get_stack_output(stack_name: str, output_key: str) -> str:
    cfn = boto3.resource('cloudformation')
    stack = cfn.Stack(stack_name)
    output = next(filter(lambda x: x['OutputKey'] == output_key, stack.outputs), None)
    if not output:
        raise 'Output with key "%s" not found in stack "%s"' % (output_key, stack_name)
    return output['OutputValue']