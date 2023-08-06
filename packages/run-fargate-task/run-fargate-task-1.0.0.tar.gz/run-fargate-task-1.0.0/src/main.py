import sys, argparse
from configManager import load_configs
from task import run_tasks
from ssm import SSM

def parse_args():
    parser = argparse.ArgumentParser(description='RUN FARGATE TASK')
    parser.add_argument(
        '-c',
        '--config',
        type=str,
        help='config directory or file',
        required=True
    )
    return parser.parse_args()

def main():
    args = parse_args()
    configs = load_configs(args.config)
    run_tasks(configs)


if __name__ == "__main__":
    main()