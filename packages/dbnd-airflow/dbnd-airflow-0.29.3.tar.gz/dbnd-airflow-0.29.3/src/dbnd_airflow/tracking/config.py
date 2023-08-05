from typing import List

from dbnd import parameter
from dbnd._core.task import Config


class AirflowTrackingConfig(Config):
    _conf__task_family = "airflow_tracking"

    spark_submit_dbnd_java_agent = parameter(
        default=None,
        description="A dbnd java agent jar which used to track a java application, located on the local machine",
    )[str]

    databricks_dbnd_java_agent = parameter(
        default=None,
        description="A dbnd java agent jar which used to track a java application, located on remote machine",
    )[str]
