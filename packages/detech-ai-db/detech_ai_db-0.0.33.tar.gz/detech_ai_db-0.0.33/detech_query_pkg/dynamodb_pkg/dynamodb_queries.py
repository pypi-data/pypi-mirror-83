import decimal
import json
from datetime import datetime

from boto3.dynamodb.conditions import Attr, Key

from .utils.dynamodb_utils import (batch_insert, get_item, get_item_and_retrieve_specific_attributes, put_item,
                                   query_by_key, query_by_key_min_max, scan_table, update_item)

ALERTS_CONFIGS_TABLE = 'alerts.config'
ALERTS_TABLE = 'alerts.items'
ANOMALIES_TABLE = 'anomalies.items'
ATOMIC_COUNTER_TABLE = 'atomic.counter'
COMPONENTS_TABLE = 'component.info'
METRICS_DETAILS_TABLE = 'metric.details'

LOGS_API_REQUEST_TABLE = 'logs.api_request'
LOGS_METRICS_FETCHING_TABLE = 'logs.cloud_metric_fetching'
LOGS_ANOMALIES_WEBHOOK = 'logs.anomalies_webhook'

DEV_ANOMALIES_TABLE = 'dev.anomalies.items'
DEV_LOGS_ANOMALIES_WEBHOOK = 'dev.logs.anomalies_webhook'


def prepare_decimal(item):
  return json.loads(json.dumps(item), parse_float=decimal.Decimal)


# ########### ATOMIC COUNTER ###################
def increment_atomic_counter(counter_type, n_values, dynamodb):
  '''
  Increments atomic counter for the specified counter type
  Returns the updated atomic counter as an int
  '''
  key_dict = {"name": counter_type}
  update_expression = "set val = val + :v"
  expression_attribute_values = {':v': decimal.Decimal(n_values)}
  table_name = ATOMIC_COUNTER_TABLE
  response = update_item(key_dict, update_expression, expression_attribute_values, table_name, dynamodb)
  if response['ResponseMetadata']['HTTPStatusCode'] == 200:
    return int(response['Attributes']['val'])
  else:
    raise Exception('Error with {} status code, in update of {} atomic counter.'.format(
      str(response['ResponseMetadata']['HTTPStatusCode']), counter_type))


# ########### ALERTS ###########################
def insert_alert(alert_id, metric_id, org_id, app_id, team_id, assigned_to, start_time, end_time, alert_description,
                 is_acknowledged, anomalies_dict, related_prev_anomalies, service_graph, significance_score, dynamodb):
  """
  insert_alert(alert_id = "256828", metric_id = 123, org_id = 'org_id', app_id = 'app_id', team_id = 'team_id',
  assigned_to = 'Jorge', start_time = '2020-09-03 12:00:00', end_time = '2020-09-03 12:20:00',
  alert_description = 'Spike in costs', is_acknowledged = 'True', anomalies_dict = {}, related_prev_anomalies = {},
  service_graph = {}, significance_score = '34.3')
  """
  alert_dict = {
    'alert_id': alert_id,
    'metric_id': metric_id,
    'org_id': org_id,
    'app_id': app_id,
    'team_id': team_id,
    'assigned_to': assigned_to,
    'start_time': start_time,
    'end_time': end_time,
    'alert_description': alert_description,
    'is_acknowledged': is_acknowledged,
    'anomalies_dict': anomalies_dict,
    'related_prev_anomalies': related_prev_anomalies,
    'service_graph': service_graph,
    'significance_score': significance_score
  }
  response = put_item(alert_dict, ALERTS_TABLE, dynamodb)
  return response


def get_alert_item_by_key(anom_id, dynamodb):
  key_dict = {
    "alert_id": anom_id,
  }
  alert_item = get_item(key_dict, ALERTS_TABLE, dynamodb)
  return alert_item


def update_alert_with_related_anomalies(alert_id, start_time, corr_anoms_dict, related_prev_anomalies, dynamodb):
  # https://stackoverflow.com/questions/52367094/how-to-update-dynamodb-table-with-dict-data-type-boto3
  # TODO add similar alerts
  update_expression = "set anomalies_dict=:a, related_prev_anomalies=:r"
  expression_attr_values = {
    ':a': corr_anoms_dict,
    ':r': related_prev_anomalies,
  }
  key_dict = {
    'alert_id': alert_id,
    'start_time': start_time,
  }

  update_item(key_dict, update_expression, expression_attr_values, ALERTS_TABLE, dynamodb)

  return True


def terminate_alert(alert_id, start_time, end_timestamp, dynamodb):
  update_expression = "set end_timestamp=:e"
  expression_attr_values = {':e': end_timestamp}
  key_dict = {
    'alert_id': alert_id,
    'start_time': start_time,
  }

  update_item(key_dict, update_expression, expression_attr_values, ALERTS_TABLE, dynamodb)

  return True


# ########### METRICS ##########################
# create new metric_timeseries item for current day
# TODO add unit to create metric
def create_metric(id, name, provider, namespace, region_name, data_center_id, agent, org_id, component_id, alignment,
                  dimension_name, dimension_value, description, is_active, dynamodb):
  """
  create_metric(
    id = "test1", name = "error_rate",
    provider = "aws", namespace = "dynamodb", agent = "CloudWatch", org_id = "test",
    app_id = None, alignment = "Sum",
    dimensions = [{"name": "TableName", "value": "alerts.config"}],
    description = "bla bla", is_active = True, period = 60
  )
  """
  metric_dict = {
    "id": id,
    "name": name,
    "provider": provider,
    "namespace": namespace,
    "region_name": region_name,
    "data_center_id": data_center_id,
    "agent": agent,
    "org_id": org_id,
    "component_id": component_id,
    "alignment": alignment,
    "dimension_value": dimension_value,
    "dimension_name": dimension_name,
    "description": description,
    "is_active": is_active
  }
  response = put_item(metric_dict, METRICS_DETAILS_TABLE, dynamodb)
  return response


# batch insert metrics
def chunks(lst, n):
  """Yield successive n-sized chunks from lst."""
  for i in range(0, len(lst), n):
    yield lst[i:i + n]


# deprecated
def batch_insert_metric_objects(list_of_metric_objects, dynamodb):
  # convert list of metric objects into list of metric dicts

  # print('Size of {}:'.format(metric_object.get_metric_name()))
  # print(sys.getsizeof(json.dumps(metric_object.to_dict())))
  date = datetime.today()
  date = str(date).split(' ')[0]
  batch_insert_list = chunks(list_of_metric_objects, 25)
  for chunk_list in batch_insert_list:
    metric_list = []
    for metric_obj in chunk_list:
      curr_metric = metric_obj.to_dict()
      curr_metric['date_bucket'] = date
      metric_list.append(curr_metric)
    batch_insert(metric_list, METRICS_DETAILS_TABLE, dynamodb)


def batch_insert_metric_details_objects(list_of_metric_objects, dynamodb):
  # convert list of metric objects into list of metric dicts
  batch_insert_list = chunks(list_of_metric_objects, 25)
  for chunk_list in batch_insert_list:
    metric_list = []
    for metric_obj in chunk_list:
      curr_metric = metric_obj.to_dict()
      # decide which are going to be the key attrs
      metric_list.append(curr_metric)
    batch_insert(metric_list, METRICS_DETAILS_TABLE, dynamodb)


def get_metric_details(metric_id, dynamodb):
  key_dict = {"id": metric_id}

  attr_list = [
    'id', 'name', 'namespace', 'alignment', 'region_name', 'data_center_id', 'dimension_name', 'dimension_value',
    'org_id', 'is_active'
  ]
  metric_details = get_item_and_retrieve_specific_attributes(key_dict, attr_list, METRICS_DETAILS_TABLE, dynamodb)
  return metric_details


# query metrics info by metric_id key
def get_metric_item_by_key(metric_id, curr_date, dynamodb):
  # get_metric_item_by_key(123, '2020-09-10')
  key_dict = {"metric_id": metric_id, "date_bucket": str(curr_date)}

  metric_item = get_item(key_dict, 'metric.ts', dynamodb)
  return metric_item


def scan_metrics_by_encrypted_id(anom_alarm_id, dynamodb):
  scan_kwargs = {
    'FilterExpression': Attr('encrypted_id').eq(anom_alarm_id),
  }
  metric_list = scan_table(scan_kwargs, 'metric.ts', dynamodb)
  metric_item = metric_list[0]
  return metric_item


# ############# COMPONENTS ###################
def batch_insert_component_info_objects(list_of_component_objects, dynamodb):
  # convert list of metric objects into list of metric dicts
  batch_insert_list = chunks(list_of_component_objects, 25)
  for chunk_list in batch_insert_list:
    component_list = []
    for component in chunk_list:
      # decide which are going to be the key attrs
      component_list.append(component)
    batch_insert(component_list, COMPONENTS_TABLE, dynamodb)


def update_component_last_fetched_ts(component_id, last_fetched_ts, dynamodb):
  key_dict = {'id': decimal.Decimal(component_id)}
  update_expression = 'set last_fetched_ts=:ts'
  expression_attribute_values = {':ts': last_fetched_ts}
  return update_item(key_dict, update_expression, expression_attribute_values, COMPONENTS_TABLE, dynamodb)


# ############# ALERT CONFIGS ################
def query_alerts_configs_by_key(metric_id, dynamodb):
  key_condition = Key('metric_id').eq(metric_id)
  alerts_configs_list = query_by_key(key_condition, ALERTS_CONFIGS_TABLE, dynamodb)
  return alerts_configs_list


def insert_alert_config(metric_id, alert_title, severity, alert_type, alert_direction, description, duration,
                        duration_unit, rule_dict, recipients_list, owner_dict, dynamodb):
  """
  insert_alert_config(
    metric_id = "metric1245", alert_title = "Anomaly by Cluster", severity = "critical",
    alert_type = "anomaly", alert_direction = "spikes/drops",
    description = "Relevant to Play Store billing user journey", duration= 12, duration_unit = "hours", rule_dict = {},
    recipients_list = [{
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
  """
  alert_dict = {
    "metric_id": metric_id,
    "alert_title": alert_title,
    "severity": severity,
    "alert_type": alert_type,
    "alert_direction": alert_direction,
    "description": description,
    "duration": duration,
    "duration_unit": duration_unit,
    "rule_dict": rule_dict,
    "recipients": recipients_list,
    "owner": owner_dict
  }
  response = put_item(alert_dict, 'alerts.config')
  return response


# ############# LOGS #########################
def query_most_recent_metric_fetching_log(component_id, dynamodb):
  """
  Fetches the log with the highest timestamp, from all the logs between start & end ts
  """
  # TODO Insert a greater than last_fetched_ts condition to prevent the query to go too far in time
  # & Key('last_fetched_ts').between(start_ts, end_ts)
  key_condition = Key('component_id').eq(component_id)
  logs_list = query_by_key_min_max(key_condition, LOGS_METRICS_FETCHING_TABLE, False, dynamodb)
  if len(logs_list) > 0:
    return logs_list[0]['last_fetched_ts']
  else:
    return None


def insert_api_request_log(api_name, request_timestamp, response_status_code, request, response, dynamodb):
  """
  insert_api_request_log(api_name='anomalarm_metrics', request_timestamp=1603466177, response_status_code='202',
                         request={'key': 'value'}, response={'key': 'value'}, dynamodb)
  """
  item = {
    'api_name': api_name,
    'request_timestamp': request_timestamp,
    'response_status_code': response_status_code,
    'request': request,
    'response': response
  }
  response = put_item(item, LOGS_API_REQUEST_TABLE, dynamodb)
  return response


def insert_anomalies_webhook_log(timestamp,
                                 event_type,
                                 anomaly_id,
                                 anomaly_timestamp,
                                 metric_id,
                                 request,
                                 dynamodb,
                                 is_dev_env=False):
  """
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
  """
  item = {
    'timestamp': decimal.Decimal(timestamp),
    'event_type': event_type,
    'anomaly_id': anomaly_id,
    'anomaly_timestamp': decimal.Decimal(anomaly_timestamp),
    'metric_id': metric_id,
    'request': prepare_decimal(request)
  }
  table_name = LOGS_ANOMALIES_WEBHOOK if not is_dev_env else DEV_LOGS_ANOMALIES_WEBHOOK
  response = put_item(item, table_name, dynamodb)
  return response


# ############# ANOMALIES ####################
def insert_new_anomaly(id, timestamp, metric_id, value, dynamodb, is_dev_env=False):
  """
  insert_new_anomaly(id="125123", timestamp=1599563224, metric_id="m412", value=123.44, dynamodb=dynamodb)
  """
  item = {'id': id, 'timestamp': decimal.Decimal(timestamp), 'metric_id': metric_id, 'value': decimal.Decimal(value)}
  table_name = ANOMALIES_TABLE if not is_dev_env else DEV_ANOMALIES_TABLE
  return put_item(item, table_name, dynamodb)


def update_anomaly_relations(id,
                             timestamp,
                             cross_correlations,
                             possible_related_anomalies,
                             possible_related_matches,
                             dynamodb,
                             is_dev_env=False):
  """
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
  """
  key_dict = {'id': id, 'timestamp': decimal.Decimal(timestamp)}
  update_expression = 'set cross_correlations=:cc, possible_related_anomalies=:pra, possible_related_matches=:prm'
  expression_attribute_values = prepare_decimal({
    ':cc': cross_correlations,
    ':pra': possible_related_anomalies,
    ':prm': possible_related_matches
  })
  table_name = ANOMALIES_TABLE if not is_dev_env else DEV_ANOMALIES_TABLE
  return update_item(key_dict, update_expression, expression_attribute_values, table_name, dynamodb)


def terminate_anomaly(id, timestamp, end_timestamp, dynamodb, is_dev_env=False):
  """
  terminate_anomaly(id="125123", timestamp=1599563224, end_timestamp=1599663224, dynamodb=dynamodb)
  """
  key_dict = {'id': id, 'timestamp': decimal.Decimal(timestamp)}
  update_expression = 'set end_timestamp=:ts'
  expression_attribute_values = {':ts': decimal.Decimal(end_timestamp)}
  table_name = ANOMALIES_TABLE if not is_dev_env else DEV_ANOMALIES_TABLE
  return update_item(key_dict, update_expression, expression_attribute_values, table_name, dynamodb)


# ############# EXAMPLES #####################
def update_values_in_dict_attr():
  """
  dynamo = boto3.resource('dynamodb')
    tbl = dynamo.Table('<TableName>')

    result = tbl.update_item(
        Key={
            "game_id": game_id
        },
        UpdateExpression="SET players.#player_id.score = :score_val",
        ExpressionAttributeNames={
            "#player_id": player_id
        },
        ExpressionAttributeValues={
            ":score_val": score_val
        }
    )
  """
  return True
