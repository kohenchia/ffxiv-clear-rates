import sys
from ffxiv_clear_rates.main import run


def lambda_handler(event, context):
    sys.argv = [
        'main.py',
        'fc_roster',
        '-pg',
        '--prod'
    ]
    run()

    return {
        'statusCode': 200,
        'body': 'Success'
    }
