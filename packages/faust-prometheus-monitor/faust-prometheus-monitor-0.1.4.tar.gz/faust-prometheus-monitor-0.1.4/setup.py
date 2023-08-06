# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faust_prometheus_monitor']

package_data = \
{'': ['*']}

install_requires = \
['faust>=1.10.4,<2.0.0', 'prometheus-client>=0,<1']

setup_kwargs = {
    'name': 'faust-prometheus-monitor',
    'version': '0.1.4',
    'description': 'prometheus monitor for faust',
    'long_description': '# Faust Prometheus Monitor\nPrometheus Monitor for Faust applications\n\n## Usage\n\n```python\nimport faust\nfrom faust_prometheus_monitor import expose_metrics_http_response, PrometheusMonitor\n\nAPP_NAME = "app"\napp = faust.App(APP_NAME, monitor=PrometheusMonitor(APP_NAME))\n\n@app.page("/metrics")\nasync def expose_metrics(self, request):\n    return expose_metrics_http_response(request)\n```\n\n## Metrics collected\n| Metric | Type | Labels | Description |\n| --- | --- | --- | --- |\n| faust_message_in | Counter | app, topic, partition | Message received by consumer |\n| faust_message_out | Counter | app, topic, partition | All streams finished processing message |\n| faust_stream_event_in | Counter | app, topic, stream | Message sent to a stream as an event |\n| faust_stream_event_out | Counter | app, topic, stream | Event was acknowledged by stream |\n| faust_stream_event_latency | Histogram | app, topic, stream | How long the event took to process\n| faust_topic_buffer_full | Counter | app, topic | Topic buffer full so conductor had to wait |\n| faust_table_operations | Counter | app, table, operation | Operations of faust tables (get, set, delete) |\n| faust_commit_latency | Histogram | app | Latency of consumer committing topic offset |\n| faust_send_initialized | Counter | app, topic | About to send a message |\n| faust_send_handled | Counter | app, status | Total number of messages sent regardless of success or failure |\n| faust_send_latency | Histogram | app | Latency of sending messages |\n| faust_topic_commit | Gauge | app, topic, partition | Gauge for what offset in topic partition is committed |\n| faust_topic_end_offset | Gauge | app, topic, partition | Track new topic partition end offset for monitoring lags |\n| faust_topic_read_offset | Gauge | app, topic, partition | topic partition read offset that consumer is on |\n| faust_assignment_latency | Histogram | app, status | Partition assignor completion latency regardless success or error |\n| faust_rebalance_time | Histogram | app, status | Cluster rebalance latency |\n| faust_rebalance_status | Gauge | app | Cluster rebalance status. 0: rebalance fully completed (including recovery); 1: rebalance started; 2: Consumer replied assignment is done to broker |\n| faust_web_request_status_codes | Counter | app, status_code | Status code counters on faust web views |\n| faust_web_request_latency | Histogram | app | Request latency on faust web views |\n',
    'author': 'Hamzah Qudsi',
    'author_email': 'hamzah.qudsi@kensho.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
