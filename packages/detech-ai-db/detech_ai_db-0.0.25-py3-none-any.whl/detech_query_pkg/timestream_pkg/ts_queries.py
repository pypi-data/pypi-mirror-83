# sys.path.insert(1, '/home/jvelez/Documents/detech/Data_Pipelines/detech_query_pkg/timestream_pkg')
from .utils.ts_utils import prepare_metric_records, write_to_timestream, query_from_timestream

DATABASE_NAME = 'detech.ai'
TABLE_NAME = 'DevOpsMetrics'
TABLE_NAME_TESTING = 'DevOpsMetricsTest'


def insert_metrics_from_metric_list(metric_list, session, is_test=False):
  '''
  Receives a list of metric dicts and inserts them into timestream
  '''
  records = []
  for metric in metric_list:
    dimensions = [
        {
            'Name': 'org_id',
            'Value': str(metric['org_id'])
        },
        {
            'Name': 'provider',
            'Value': str(metric['provider'])
        },
        {
            'Name': 'region_name',
            'Value': str(metric['region_name'])
        },
        {
            'Name': 'namespace',
            'Value': str(metric['namespace'])
        },
        {
            'Name': 'component_id',
            'Value': str(metric['component_id'])
        },
        {
            'Name': 'agent',
            'Value': str(metric['agent'])
        },
        {
            'Name': 'alignment',
            'Value': str(metric['alignment'])
        },
        # {'Name':'unit', 'Value':str(metric['unit'])},
        {
            'Name': 'id',
            'Value': str(metric['id'])
        },
        {
            'Name': 'dimension_name',
            'Value': str(metric['dimension_name'])
        },
        {
            'Name': 'dimension_value',
            'Value': str(metric['dimension_value'])
        }
    ]
    records.append(prepare_metric_records(metric['name'], str(metric['value']), metric['timestamp'], dimensions))
  write_to_timestream(records, DATABASE_NAME, TABLE_NAME if not is_test else TABLE_NAME_TESTING, session)


def query_metrics(sql_query, session):
  '''
  Performs a query to timestream, and formats the response in a list of MetricModel objects
  '''
  """SELECT metric_id, agent, component_id, period, unit, org_id, metric_alignment, namespace,
  description, region_name, measure_value::double as value, measure_name as metric_name, BIN(time, 1m) as timestamp
  FROM "detech.ai"."DevOpsMetrics"
  GROUP BY metric_id, agent, component_id, period, unit, org_id, metric_alignment, namespace,
  description, region_name, measure_value::double, measure_name , BIN(time, 1m)
  ORDER BY metric_id, BIN(time, 1m) DESC"""
  query_response = query_from_timestream(sql_query, DATABASE_NAME, TABLE_NAME, session)
  metric_obj_list = []
  if query_response['ResponseMetadata']['HTTPStatusCode'] == 200:
    if len(query_response['Rows']) == 0:  # empty request
      print('Empty request')
    else:
      for metric in query_response['Rows']:
        # Each metric returned
        curr_metric = {}
        for idx, attr in enumerate(metric['Data']):
          curr_metric[query_response['ColumnInfo'][idx]['Name']] = attr['ScalarValue']
        metric_obj_list.append(curr_metric)
  else:
    raise Exception('Error in requesting query: Status Code: {}'.format(
        str(query_response['ResponseMetadata']['HTTPStatusCode'])))
  return metric_obj_list
