from minio import Minio
from config.config import Config
# from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
#                          BucketAlreadyExists)
import logging
log = logging.getLogger(__name__)


class MinioBase(object):
    user_profile_bucket = ''
    banner_profile_bucket = ''
    connection_name = ''
    def __init__(self):
        self.config = Config()
        username = self.config.get(self.connection_name, 'username')
        password = self.config.get(self.connection_name, 'password')
        host = self.config.get(self.connection_name,'host')
        if host is not None:
            if password is not None:
                if username is not None:        
                    self.cli = Minio(host,
                                access_key=username,
                                secret_key=password,
                                secure=True)
    def check_and_make_bucket(self,bucket_name):
        try:
            found = self.cli.bucket_exists(bucket_name)
            if not found:
                self.cli.make_bucket(bucket_name)
            return 
        except Exception as e: 
            log.error('somthing in check bucket went wrong!\n',e)


    def put_image(self,raw_image,bucket_name,object_name):
        # object_name = object_name.split('/')[0] + '/test.jpg'
        while True:
            try:
                result = self.cli.put_object(bucket_name=bucket_name, object_name=object_name, 
                                     data=raw_image, length=raw_image.getbuffer().nbytes)
                break
            except  : 
                username = self.config.get(self.connection_name, 'username')
                password = self.config.get(self.connection_name, 'password')
                host = self.config.get(self.connection_name,'host')
                if host is not None:
                    if password is not None:
                        if username is not None:        
                            self.cli = Minio(host,
                                        access_key=username,
                                        secret_key=password,
                                        secure=True)
                
    def get_image(self,bucket_name,object_name):
        try:
            response = self.cli.get_object(bucket_name, object_name)
            # Read data from response.
        finally:
            response.close()
            response.release_conn()    
            return response

