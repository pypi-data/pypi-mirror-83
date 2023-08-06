from ecs import ECS
from cloudwatch import LOGS
import time

def run_tasks(configs):
    task_arns = []
    for config in configs: 
        
        ecs = ECS(config["AWS_PROFILE"])
        latest_task_arn = ecs.get_last_task_definition_arn(config["TASK_FAMILY"])
        cluster_arn = ecs.get_cluster_arn(config["CLUSTER_NAME"])
        running_task_arn = ecs.run_task(latest_task_arn,cluster_arn,config["TASK_SUBNETS"],config["TASK_SECURITY_GROUPS"],config["COMMAND"],config["TASK_FAMILY"])
    
        print("Waiting task {} to start in {} ...".format(config["TASK_FAMILY"],config["ENV"]))
        ecs.wait("tasks_running",running_task_arn,cluster_arn)
        print("Task runnning")

        
        logs = LOGS(config["AWS_PROFILE"])
        log_group = config["TASK_FAMILY"]
        log_stream_name = ecs.get_log_stream_name(log_group, running_task_arn)
        
        nextToken = None
        print("Fetching logs")
        while ecs.task_is_running(running_task_arn,cluster_arn):
            newToken = logs.printLogs(nextToken, log_group, log_stream_name)
            nextToken = newToken
            time.sleep(1)
        task_arns.append(running_task_arn)
        print("TASK {} FINISHED".format(running_task_arn))
    return task_arns
        
       


    
