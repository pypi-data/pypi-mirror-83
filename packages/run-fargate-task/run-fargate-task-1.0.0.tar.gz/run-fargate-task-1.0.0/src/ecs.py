import boto3
import os

class ECS:
    def __init__(self,profile_name):
        self.client = self.get_client(profile_name)

    def get_client(self,profile_name):
        boto3.setup_default_session(profile_name=profile_name)
        return boto3.client("ecs")

    def get_task_definition_arns(self,family):
        return self.client.list_task_definitions(familyPrefix=family)["taskDefinitionArns"]

    def get_last_task_definition_arn(self,family):
        return self.get_task_definition_arns(family)[-1]

    def run_task(self,task_definition_arn,cluster_arn,subnets,securityGroups,command,container):
        response = self.client.run_task(
            taskDefinition = task_definition_arn,
            cluster = cluster_arn,
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': subnets,
                    'securityGroups': securityGroups,
                    'assignPublicIp': 'DISABLED'
                }
            },
            overrides={
                'containerOverrides': [
                    {
                        'name': container,
                        'command': eval(command)
                    }
                ]
            },
            launchType = "FARGATE"
        )
        return response["tasks"][0]["taskArn"]

    def get_task_status(self,task_definition_arn,cluster_arn):
        response = self.client.describe_tasks(
            cluster=cluster_arn,
            tasks=[
                task_definition_arn
            ]
        )
        return response['tasks'][0]['lastStatus']

    def task_is_running(self,task_definition_arn,cluster_arn):
        return self.get_task_status(task_definition_arn,cluster_arn) == "RUNNING"

    def wait(self,condition,task_arn,cluster_arn):
        waiter = self.client.get_waiter(condition)

        waiter.wait(
            cluster=cluster_arn, 
            tasks=[task_arn],
            WaiterConfig = {
                "Delay": 3
            }
        )

    def get_cluster_arn(self,cluster_name):
        return self.client.describe_clusters(
            clusters=[
                cluster_name
            ]
        )['clusters'][0]['clusterArn']
    
    def get_log_stream_name(self,task_family,task_arn):
        task_id = task_arn.split("/")[-1]
        return "aws-fargate//{}/{}".format(task_family,task_id)