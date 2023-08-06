import boto3

class LOGS:
    def __init__(self,profile_name):
        self.client = self.get_client(profile_name)

    def get_client(self,profile_name):
        boto3.setup_default_session(profile_name=profile_name)
        return boto3.client("logs")

    def printLogs(self, next_token,log_group_name,log_stream_name):
    
        if next_token: 
            response = self.client.get_log_events(
                logStreamName=log_stream_name,
                logGroupName=log_group_name,
                nextToken = next_token
            )
        else:
            response = self.client.get_log_events(
                logStreamName=log_stream_name,
                logGroupName=log_group_name
            )
        
        if not next_token and not response["events"]:
                return None

        if response["nextForwardToken"] is not next_token:
            for log in response["events"]:
                print(log["message"])
     
        return response["nextForwardToken"]

