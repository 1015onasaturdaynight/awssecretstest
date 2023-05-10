try:
    import boto3
    import json
    import os
    import sys
except Exception as e:
    raise ("some modules are missing :{} ".format(e))

# global AWS_ACCESS_KEY
# global AWS_SECRET_KEY
# global AWS_REGION_NAME

AWS_ACCESS_KEY = "XXXX"
AWS_SECRET_KEY = "XXXX"
AWS_REGION_NAME = "us-east-1"

class AwsSecretManager(object):
    __slots__ = ["_session", "client"]

    def __init__(self):
        self._session = boto3.session.Session()
        self.client = self._session.client(
            service_name='secretsmanager',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION_NAME
        )

    def get_secrets(self, secret_name=''):
        try:
            if secret_name == '': raise Exception("secret name cannot be null")
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
        except Exception as secret_exception:
            print(str(secret_exception))
            sys.exit(-1)
        else:
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
                secret = json.loads(secret)
                for key, value in secret.items(): os.environ[key] = value

                return {
                    "status": 200,
                    "error": {},
                    "data": {
                        "message": True
                    }
                }

secrets_name = "XXXX"
secret_manager = AwsSecretManager()
response_secrets = secret_manager.get_secrets(secret_name=secrets_name)
print("secret : ", os.getenv("name"))
# print(response_secrets)
