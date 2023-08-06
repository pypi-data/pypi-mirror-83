import boto3

class SSM:
    def __init__(self,profile_name):
        self.client = self.get_client(profile_name)

    def get_client(self,profile_name):
        boto3.setup_default_session(profile_name=profile_name)
        return boto3.client("ssm")

    def get_parameter(self, parameter_name, is_secret=False):
        response = self.client.get_parameter(
            Name=parameter_name,
            WithDecryption=is_secret
        )
        return self.parse_response(response)


    def parse_response(self, response):
        if response["Parameter"]["Type"] == "StringList":
            return response["Parameter"]["Value"].split(",")
        return response["Parameter"]["Value"]
