class MetricModel(object):
  """
  MetricModel record
  Args:
    metric (Metric, mandatory): The metric to return, including the metric name, namespace, and dimensions
    period (int, mandatory): The granularity, in seconds, of the returned data points
    stat (str, mandatory): The statistic to return
    unit (str): If you specify a unit, the operation returns only data that was collected with that unit specified
  """
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
               unit=None):
    self.id = id
    self.name = name
    self.org_id = org_id
    self.region_name = region_name
    self.data_center_id = data_center_id
    self.namespace = namespace
    self.component_id = component_id
    self.agent = agent
    self.alignment = alignment
    self.unit = unit
    self.description = description
    self.is_active = is_active
    self.dimension_name = dimension_name
    self.dimension_value = dimension_value

  # TODO: #50 replace attr getters for <object.attr>

  def get_metric_name(self):
    return self.metric_name

  def get_region_name(self):
    return self.region_name

  def get_dimension_name(self):
    return self.dimension_name

  def get_component_id(self):
    return self.component_id

  def update_is_active(self, is_active_value):
    self.is_active = is_active_value

  def update_component_id(self, component_id):
    self.component_id = component_id

  def to_dict(self):
    """
    Returns a dict representation of a MetricModel instance for serialization.
    Returns:
      dict: Dict populated with self attributes to be serialized
    """
    dictionary = dict(id=self.id,
                      name=self.name,
                      org_id=self.org_id,
                      region_name=self.region_name,
                      data_center_id=self.data_center_id,
                      namespace=self.namespace,
                      component_id=self.component_id,
                      agent=self.agent,
                      dimension_name=self.dimension_name,
                      dimension_value=self.dimension_value,
                      description=self.description,
                      alignment=self.alignment,
                      is_active=self.is_active)

    if self.description is not None:
      dictionary.update(description=self.description)
    if self.unit is not None:
      dictionary.update(unit=self.unit)
    return dictionary
