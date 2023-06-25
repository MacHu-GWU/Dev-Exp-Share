"""
本模块是一个封装了 airflow API 的 wrapper, 用于调用各种 MWAA 所管理的 airflow 的 API.

原生 Airflow 有两种 API: 用 CLI 调用的 API 和用 HTTP Request 调用的 Rest API. 但
 根据我跟 AWS 的客服确认, MWAA 只支持用 Request API 调用 CLI, 有一点点别扭. 相当于用
 Rest API submit 一个 CLI command 的远程命令到 MWAA 的服务器上远程执行.

- `Using a Python script <https://docs.aws.amazon.com/mwaa/latest/userguide/call-mwaa-apis-cli.html#create-cli-token-python>`_:
    这段代码原本出自于这个 AWS 官方文档的例子. 我将它优化了, 更容易理解, 方便扩展.
- `Airflow CLI Reference <https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html>`_:
    这是 airflow 的 CLI 文档, 里面有各种命令的语法.
- `Airflow API Reference <https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#section/Overview>`_:
    这是 airflow 的 Rest API 文档.
"""

import typing as T
import boto3
import json
import requests
import base64


def get_airflow_cli_token(
    mwaa_client,
    mwaa_env_name: str,
) -> T.Tuple[str, str]:
    """
    调用 boto3 API 获得 Airflow 的 CLI token.
    """
    res = mwaa_client.create_cli_token(Name=mwaa_env_name)
    cli_token = res["CliToken"]
    webserver_hostname = res["WebServerHostname"]
    return cli_token, webserver_hostname


def run_cli(
    cli_token: str,
    webserver_hostname: str,
    cmd_and_arg: str,
) -> T.Tuple[str, str]:
    """
    将 airflow ... 的 CLI 命令提交到 MWAA 的服务器上远程执行, 并返回执行结果.
    """
    mwaa_auth_token = f"Bearer {cli_token}"
    endpoint = f"https://{webserver_hostname}/aws_mwaa/cli"
    mwaa_response = requests.post(
        endpoint,
        headers={"Authorization": mwaa_auth_token, "Content-Type": "text/plain"},
        data=cmd_and_arg,
    )
    # print(mwaa_response.text)
    response_json = mwaa_response.json()
    mwaa_stderr_message = base64.b64decode(response_json["stderr"]).decode("utf8")
    mwaa_stdout_message = base64.b64decode(response_json["stdout"]).decode("utf8")
    return mwaa_stderr_message, mwaa_stdout_message


if __name__ == "__main__":
    mwaa_env_name = "MyAirflowEnvironment"
    aws_profile = "awshsh_app_dev_us_east_1"
    mwaa_client = boto3.session.Session(profile_name=aws_profile).client("mwaa")
    cli_token, webserver_hostname = get_airflow_cli_token(mwaa_client, mwaa_env_name)

    # 把 Airflow CLI 的命令放在这里, 具体命令可以参考
    # https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#section/Overview

    # cmd_and_arg = "dags list -o json"
    cmd_and_arg = "dags trigger dag1"

    mwaa_stderr_message, mwaa_stdout_message = run_cli(
        cli_token, webserver_hostname, cmd_and_arg
    )
    print("--- stderr ---")
    print(mwaa_stderr_message)
    print("--- stdout ---")
    print(mwaa_stdout_message)
