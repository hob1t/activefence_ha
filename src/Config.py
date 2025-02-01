import os

import yaml


print(f" current path {os.getcwd()}")

with open(f"{os.getcwd()}/src/config.yml", 'r') as file:
    config_service = yaml.safe_load(file)


def get_free_plan_window() -> int:
    """
    Gets a free plan window size
    :return: int
    """
    return config_service['free']['plan']['window']


def get_free_plan_requests() -> int:
    """
    Gets a free plan requests allowed amount per window
    :return: int
    """
    return config_service['free']['plan']['requests']


def get_free_plan_daily_limit() -> int:
    """
    Gets a free plan daily limit
    :return: int
    """
    return config_service['free']['plan']['daily']['limit']


def get_pro_plan_window() -> int:
    """
    Gets a pro-plan window size
    :return: int
    """
    return config_service['pro']['plan']['window']


def get_pro_plan_requests() -> int:
    """
    Gets a pro-plan requests allowed amount per window
    :return: int
    """
    return config_service['pro']['plan']['requests']


def get_pro_plan_daily_limit() -> int:
    """
    Gets a pro-plan daily limit
    :return: int
    """
    return config_service['pro']['plan']['daily']['limit']


#### enterprise-plan-window
def get_enterprise_plan_window() -> int:
    """
    Gets enterprise-plan window size
    :return: int
    """
    return config_service['enterprise']['plan']['window']


def get_enterprise_plan_requests() -> int:
    """
    Gets a enterprise-plan requests allowed amount per window
    :return: int
    """
    return config_service['enterprise']['plan']['requests']


def get_enterprise_plan_daily_limit() -> int:
    """
    Gets a enterprise-plan daily limit
    :return: int
    """
    return config_service['enterprise']['plan']['daily']['limit']