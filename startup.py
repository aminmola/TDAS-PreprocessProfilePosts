import etl.load as load
import etl.transform as transform


def run(data):
    """
    Extract, transform and load Data
    """
    if data:
        parsed_data, account = transform.run(data)
        b = load.run(data=parsed_data, account=account)
        return b
