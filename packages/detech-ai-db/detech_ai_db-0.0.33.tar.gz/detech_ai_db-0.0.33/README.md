# Database access package for detech.ai

This is detech.ai's package to access Dynamodb & Timestream programatically.

# Imports
```python
import detech_query_pkg

###############    DynamoDB Package    ##############################
from detech_query_pkg.dynamodb_pkg import dynamodb_queries as db_queries

from detech_query_pkg.dynamodb_pkg.utils import dynamodb_utils as db_utils

#Start DynamoDB Client
db_utils.create_dynamodb_client(aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)

###############    Timestream Package    ##############################
from detech_query_pkg.timestream_pkg import ts_queries

from detech_query_pkg.timestream_pkg.utils import ts_utils

from detech_query_pkg.timestream_pkg.models import metrics_model
from detech_query_pkg.timestream_pkg.models import metrics_creator_utils
```

# Initialize Client
```python
def create_dynamodb_client(aws_access_key_id,aws_secret_access_key, region_name)

def create_timestream_session(aws_access_key_id, aws_secret_access_key)
```

# Functions
## timestream_pkg (ts_queries.py)
<details>
  <summary>insert_metrics_from_metric_list</summary>

  ```python
  def insert_metrics_from_metric_list(metric_list, session)

  #Inserts metrics in batch to timestream

  #metric_list must have the following fields
  metric_list = [
    {'org_id', 'region_name', 'namespace', 'component_id', 'period', 'agent', 'metric_alignment', 'unit', 'description' , 'metric_id', 'metric_name', 'value', 'timestamp'},
    {'org_id', 'region_name', 'namespace', 'component_id', 'period', 'agent', 'metric_alignment', 'unit', 'description' , 'metric_id', 'metric_name', 'value', 'timestamp'},
    ...
  ]
  ```
</details>

<details>
  <summary>query_metrics</summary>

  ```python
  def query_metrics(sql_query, session)

  #Performs an SQL query to timestream and transforms the output to a more desirable format

  #Output
  query_response = {
    'metric_id': 'qgrdy1bXGeKSmAtW58CD',
    'agent': 'AWS.CloudWatch',
    'component_id': 'AWS/ApplicationELB.app/component',
    'period': '60',
    'unit': 'None',
    'org_id': 'Organization',
    'metric_alignment': 'Sum',
    'namespace': 'AWS/ApplicationELB',
    'description': 'The total number of concurrent TCP connections active from clients to the load balancer and from the load balancer to targets.',
    'region_name': 'eu-west-1',
    'value': '64.0',
    'metric_name': 'ActiveConnectionCount',
    'timestamp': '2020-10-12 14:28:00.000000000'
  }
  ```
</details>


## timestream_pkg.utils (ts_utils.py)
<details>
  <summary>prepare_metric_records</summary>

  ```python
  def prepare_metric_records(measure_name, measure_value, timestamp, dimensions)

  #Creates the metrics records necessary to use the write_to_timestream function

  #The dimensions that need to be passed must be in the following format
  dimensions = [
    {'Name':'org_id', 'Value': str(metric['org_id'])},
    {'Name':'region_name', 'Value':str(metric['region_name'])},
    {'Name':'namespace', 'Value':str(metric['namespace'])},
    {'Name':'component_id', 'Value':str(metric['component_id'])},
    {'Name':'period', 'Value': str(metric['period'])},
    {'Name':'agent', 'Value':str(metric['agent'])},
    {'Name':'metric_alignment', 'Value':str(metric['metric_alignment'])},
    {'Name':'unit', 'Value':str(metric['unit'])},
    {'Name': 'description', 'Value': str(metric['description'])},
    {'Name': 'metric_id', 'Value':str(metric['metric_id'])}
  ]

  ```
</details>

<details>
  <summary>write_to_timestream</summary>

  ```python
  def write_to_timestream(records, database_name, table_name, ts_session)

  #Inserts metrics to timestream after they are in the correct format

  ```
</details>

<details>
  <summary>query_from_timestream</summary>

  ```python
  def query_from_timestream(sql_query, database_name, table_name,ts_session)

  #Queries metrics from timestream with a given sql_query

  ```
</details>

## timestream_pkg.models (metric_creator_utils.py & metrics_model.py)
<details>
  <summary>build_metric_model</summary>

  ```python
  #from metric_creator_utils.py
  def build_metric_model(metric_id, metric_name, org_id, component_id,
    namespace, metric_alignment, agent, dimensions, region_name=None,
    is_default=False, description=None, period=60,unit=None, samples=[])

  #Queries metrics from timestream with a given sql_query

  ```
</details>

<details>
  <summary>MetricModel</summary>

  ```python
  #from metrics_model.py
  class MetricModel(object):
    def __init__(self,
               id,
               name,
               org_id,
               component_id,
               namespace,
               alignment,
               region_name,
               data_center_id,
               agent,
               dimension_name=None,
               dimension_value=None,
               is_active=False,
               description=None,
               unit=None)

    def to_dict(self)

  #Queries metrics from timestream with a given sql_query

  ```
</details>


## dynamodb_pkg

<details>
  <summary>insert_alert</summary>

  ```python
  def insert_alert(alert_id, metric_id, org_id, app_id, team_id, assigned_to, start_time, end_time, alert_description, is_acknowledged, anomalies_dict, related_prev_anomalies,  service_graph, significance_score, dynamodb)

  #Example
  insert_alert(alert_id = "256828", metric_id = 123, org_id = 'org_id', app_id = 'app_id', team_id = 'team_id', assigned_to = 'Jorge', \
  start_time = '2020-09-03 12:00:00', end_time = '2020-09-03 12:20:00', alert_description = 'Spike in costs',\
  is_acknowledged = 'True', anomalies_dict = {}, related_prev_anomalies = {},
  service_graph = {}, significance_score = '34.3')
  ```
</details>

<details>
  <summary>get_alert_item_by_key</summary>

  ```python
  def get_alert_item_by_key(anom_id, dynamodb)
  ```
</details>

<details>
  <summary>update_alert_with_related_anomalies</summary>

  ```python
  def update_alert_with_related_anomalies(alert_id,start_time, corr_anoms_dict, related_prev_anomalies, dynamodb)
  ```
</details>

<details>
  <summary>terminate_alert</summary>

  ```python
  def terminate_alert(alert_id,start_time, end_timestamp, dynamodb)
  ```
</details>

<details>
  <summary>create_metric</summary>

  ```python
  def create_metric(metric_id, date_bucket, metric_name, provider, namespace,
  agent, org_id, app_id, alignment, groupby, dimensions, data_points_list, dynamodb)

  #Example
  create_metric(
    metric_id = "test1", date_bucket = "2020-10-02", metric_name = "error_rate",
    provider = "aws", namespace = "dynamodb", agent = "CloudWatch", org_id = "test",
    app_id = "app1", alignment = "Sum",
    dimensions = [{"Name": "TableName", "Value": "alerts.config"}],
    last = 1535530432, data_points_list = [
      { 'val': 55, 'time' : 1535530430},
      { 'val': 56, 'time': 1535530432}], dynamodb=dynamodb
  )
  ```
</details>

<details>
  <summary>batch_insert_metric_objects</summary>

  ```python
  def batch_insert_metric_details_objects(list_of_metric_objects, dynamodb)
  #Inserts list of metrics objects in batch into Dynamodb
  ```
</details>

<details>
  <summary>batch_insert_metric_objects</summary>

  ```python
  def batch_insert_metric_details_objects(list_of_metric_objects, dynamodb)
  #Inserts list of metrics objects in batch into Dynamodb
  ```
</details>

<details>
  <summary>batch_insert_metric_objects</summary>

  ```python
  def batch_insert_component_info_objects(list_of_component_objects, dynamodb)
  #Inserts list of component objects in batch into Dynamodb
  ```
</details>


<details>
  <summary>get_metric_details</summary>

  ```python
  def get_metric_details(metric_id, dynamodb)
  #Fetches all the details for a specific metric_id
  ```
</details>

<details>
  <summary>get_metric_item_by_key</summary>

  ```python
  def get_metric_item_by_key(metric_id, curr_date, dynamodb)
  ```
</details>

<details>
  <summary>scan_metrics_by_encrypted_id</summary>

  ```python
  def scan_metrics_by_encrypted_id(anom_alarm_id, dynamodb)
  ```
</details>

<details>
  <summary>query_alerts_configs_by_key</summary>

  ```python
  def query_alerts_configs_by_key(metric_id, dynamodb)
  ```
</details>

<details>
  <summary>insert_alert_config</summary>

  ```python
  def insert_alert_config(metric_id, alert_title, severity, alert_type, alert_direction, description, duration, duration_unit, rule_dict, recipients_list, owner_dict, dynamodb)

  #Example
  insert_alert_config(
    metric_id = "metric1245", alert_title = "Anomaly by Cluster", severity = "critical",
    alert_type = "anomaly", alert_direction = "spikes/drops", description = "Relevant to Play Store billing user journey",
    duration= 12, duration_unit = "hours", rule_dict = {}, recipients_list = [{
      "channel" : "webhook",
      "contact" : "j.velez2210@gmail.com"
      },{
        "channel" : "slack",
        "contact" : "j.velez2210@gmail.com"
      }
    ],
    owner_dict = {
      "user_id" : "user12341",
      "user_name" : "João Tótó",
    }
  )
  ```
</details>

<details>
  <summary>query_most_recent_metric_fetching_log</summary>

  ```python
  def query_most_recent_metric_fetching_log(component_id, dynamodb)
  #Fetches the log with the highest timestamp, from all the logs between start & end ts
  ```
</details>

<details>
  <summary>insert_api_request_log</summary>

  ```python
  def insert_api_request_log(api_name, request_timestamp, response_status_code, request, response, dynamodb)
  # Example
  insert_api_request_log(api_name='anomalarm_metrics', request_timestamp=1603466177, response_status_code='202',
                         request={'key': 'value'}, response={'key': 'value'}, dynamodb=dynamodb)
  ```
</details>

<details>
  <summary>insert_new_anomaly</summary>

  ```python
  def insert_new_anomaly(id, timestamp, metric_id, value, dynamodb, is_dev_env=False):
  # Example
  insert_new_anomaly(id="125123", timestamp=1599563224, metric_id="m412", value=123.44, dynamodb=dynamodb)
  ```
</details>

<details>
  <summary>update_anomaly_relations</summary>

  ```python
  def update_anomaly_relations(id, timestamp, cross_correlations, possible_related_anomalies, possible_related_matches,
                               dynamodb, is_dev_env=False):
  # Example
  update_anomaly_relations(id="125123",
                           timestamp=1599563224,
                           cross_correlations={
                             "web-server-1.cpu0.iowait": {
                               "coefficient": 0.95752,
                               "shifted": 0,
                               "shifted_coefficient": 0.95752
                             },
                           },
                           possible_related_anomalies={
                             "256826": {
                               "metric_id": "web-server-1.mysql.counters.handlerRead_key",
                               "timestamp": 1599563164
                             },
                           },
                           possible_related_matches={
                             "169560": {
                               "timestamp": 1599563230,
                               "fp id": 8821,
                               "layer id": "None",
                               "metric_id": "web-server-2.mariadb.localhost:3306.mysql.bytes_sent"
                             }
                           },
                           dynamodb=dynamodb)
  ```
</details>

<details>
  <summary>insert_anomalies_webhook_log</summary>

  ```python
  def insert_anomalies_webhook_log(timestamp, event_type, anomaly_id, anomaly_timestamp, metric_id, request, dynamodb, is_dev_env=False):
  # Example
  insert_anomalies_webhook_log(timestamp=1603466177, event_type='NEW', anomaly_id='256828',
                               anomaly_timestamp=1599563224, metric_id='m4123',
                               request={
                                 'data': {
                                   'anomaly': {
                                     'id': '256828',
                                     'metric': 'web-server-1.mysql.counters.m4123.handlerRead_rnd',
                                     'timestamp': 1599563224,
                                     'value': 143.544444
                                   }
                                 },
                                 'status': {}
                               },
                               dynamodb=dynamodb)
  ```
</details>

<details>
  <summary>terminate_anomaly</summary>

  ```python
  def terminate_anomaly(id, timestamp, end_timestamp, dynamodb, is_dev_env=False):
  # Example
  terminate_anomaly(id="125123", timestamp=1599563224, end_timestamp=1599663224, dynamodb=dynamodb)
  ```
</details>

## dynamodb_pkg.utils
<details>
  <summary>put_item</summary>

  ```python
  def put_item(item_dict, table_name, dynamodb)
  #Inserts json item into DynamoDB table

  #Example
  item_dict = {
    "attr" : "value",
    "attr2" : "value2"
  }
  table_name = "alerts"
  ```
</details>


<details>
  <summary>batch_insert</summary>

  ```python
  def batch_insert(list_of_item_dicts, table_name, dynamodb)
  #Inserts a list of item_dicts in batch to dynamodb
  ```
</details>


<details>
  <summary>get_item</summary>

  ```python

  def get_item(key_dict, table_name, dynamodb)
  #Retrieves item from DynamoDB table

  #Example
  key_dict = {
    "prim_key" = "value",
    "sort_key" = "value"
  }
  ```
</details>

<details>
  <summary>get_item_and_retrieve_specific_attributes</summary>

  ```python

  def get_item_and_retrieve_specific_attributes(key_dict, attr_list, table_name, dynamodb)
  #Retrieves item from DynamoDB table and retrieve specific attributes

  #Example
  key_dict = {
    "prim_key" :"value",
    "sort_key" : "value"
  }
  attr_list = ['attr1', 'attr2']
  ```
</details>


<details>
  <summary>update_item</summary>

  ```python
  def update_item(key_dict, update_expression, expression_attr_values, table_name, dynamodb)
  #Retrieves item from DynamoDB table

  #Example
  key_dict = {
    "prim_key" = "value",
    "sort_key" = "value"
  }
  update_expression = "set service_graph=:i, metric_list=:l, significance_score=:s"
  expression_attr_values = {
    ':i': {'s1':['s2', 's3']},
    ':l': ['124','123'],
    ':s': Decimal(35.5)
  }
  #example to append to list
  UpdateExpression="SET some_attr = list_append(if_not_exists(some_attr, :empty_list), :i)",
  ExpressionAttributeValues={
    ':i': [some_value],
    "empty_list" : []
  }

  ```
</details>

<details>
  <summary>update_item_conditionally</summary>

  ```python
  def update_item_conditionally(key_dict, condition_expression, update_expression, expression_attr_values, table_name, dynamodb)
  #Retrieves item from DynamoDB table

  #Example
  key_dict = {
    "prim_key" = "value",
    "sort_key" = "value"
  }
  update_expression = "set service_graph=:i, metric_list=:l, significance_score=:s"
  expression_attr_values = {
    ':i': {'s1':['s2', 's3']},
    ':l': ['124','123'],
    ':s': Decimal(35.5)
  }
  condition_expression = "significance_score <= :val"

  ```
</details>

<details>
  <summary>delete_item_conditionally</summary>

  ```python
  def delete_item_conditionally(key_dict, condition_expression, expression_attr_values, table_name, dynamodb)

  #Example
  condition_expression = "significance_score <= :val"
  expression_attr_values = {
    ":val": Decimal(50)
  }
  key_dict = {
    'org_id': 'Aptoide',
    'start_time': '2020-09-03 12:00:00'
  }
  '''
  ```
</details>

<details>
  <summary>query_by_key</summary>

  ```python
  def query_by_key(key_condition, table_name, dynamodb)
  #Queries from DynamoDB table by key condition

  #Example
  key_condition = Key('org_id').eq('Aptoide')

  ```
</details>

<details>
  <summary>query_and_project_by_key_condition</summary>

  ```python
  def query_and_project_by_key_condition(projection_expr, expr_attr_names, key_condition, table_name, dynamodb)
  #Queries from DynamoDB table by key condition and only returns some attrs

  #Example
  key_condition = Key('year').eq(year) & Key('title').between(title_range[0], title_range[1])
  projection_expr = "#yr, title, info.genres, info.actors[0]"
  expr_attr_names = {"#yr": "year"}
  ```
</details>

<details>
  <summary>scan_table</summary>

  ```python
  def scan_table(scan_kwargs, table_name, dynamodb)
  #Scans entire table looking for items that match the filter expression

  #Example
  scan_kwargs = {
    'FilterExpression': Key('year').between(*year_range),
    'ProjectionExpression': "#yr, title, info.rating",
    'ExpressionAttributeNames': {"#yr": "year"}
  }

  ```
</details>

<details>
  <summary>query_by_key_min_max</summary>

  ```python
  def query_by_key_min_max(key_condition, table_name, is_min, dynamodb)
  #Queries from DynamoDB table by key condition

  #Example
  key_condition = Key('part_id').eq(partId) & Key('range_key').between(start, end)
  #or
  key_condition = Key('part_id').eq(partId)

  ```
</details>

<details>
  <summary>get_all_items_in_table</summary>

  ```python
  def get_all_items_in_table(table_name, dynamodb)
  ```
</details>


 <details>
  <summary>increment_atomic_counter</summary>

  ```python
  def increment_atomic_counter(counter_type, number_of_values, dynamodb)
  #Increments a counter and makes sure it is done atomically
  #Available counter types:
  #org_id
  #component_id
  #metric_id
  ```
</details>
