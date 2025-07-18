from databricks.sdk import WorkspaceClient
from databricks.sdk.service import workspace
from pyspark.dbutils import DBUtils
from pyspark.sql import SparkSession
import base64
import json
import boto3
import uuid

def get_workspace_client():

    w = WorkspaceClient()

    return w

def decode_notebook(w:WorkspaceClient, path):
    notebook_content = w.workspace.export(
        path= path,
        format=workspace.ExportFormat.JUPYTER
    )

    decoded_bytes = base64.b64decode(notebook_content.content)

    decoded_string = decoded_bytes.decode('utf-8')

    notebook_dict = json.loads(decoded_string)
    
    return notebook_dict

def encode_notebook(w:WorkspaceClient, path, notebook_dict):
    out_str = json.dumps(notebook_dict)

    out_utf8 = out_str.encode('utf-8')

    encoded_bytes = base64.b64encode(out_utf8).decode('utf-8')

    w.workspace.import_(
        path=path
        , content=encoded_bytes,
        overwrite=True,
        format=workspace.ExportFormat.JUPYTER
    )

def create_notebook(name:str):
    return {
        "cells": [],
        "metadata": {
            "application/vnd.databricks.v1+notebook": {
                "computePreferences": "null",
                "dashboards": [],
                "environmentMetadata": {
                    "base_environment": "",
                    "environment_version": "2"
                },
                "inputWidgetPreferences": "null",
                "language": "python",
                "notebookMetadata": {
                    "pythonIndentUnit": 4
                },
                "notebookName": name,
                "widgets": {}
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }

def create_cell(code:str):
    return {
            "cell_type": "code",
            "execution_count": 0,
            "metadata": {
                "application/vnd.databricks.v1+cell": {
                    "cellMetadata": {},
                    "inputWidgets": {},
                    "nuid": str(uuid.uuid4()),
                    "showTitle": "false",
                    "tableResultSettingsMap": {},
                    "title": ""
                }
            },
            "outputs": [],
            "source": [code]
        }
    


def get_notebook_path():
    dbutils = DBUtils(SparkSession.builder.getOrCreate())
    return dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()