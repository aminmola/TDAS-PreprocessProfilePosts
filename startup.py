import os

# import etl.extract as extract
import etl.load as load
import etl.transform as transform
from utils.logger import Logger

# log = Logger("preprocessing")
# os.environ['TZ'] = 'UTC'


def run(data):
    """
    Extract, transform and load Data
    """
    if data:
        parsed_data = transform.run(data)
        load.run(data=parsed_data)




    # else:
    #     log.error(f"Extract data failed")

#
# if __name__ == '__main__':
#     # data = extract.run()
#     if data:
#         run(data)
