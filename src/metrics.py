from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import os

PUSHGW = os.getenv("PUSHGATEWAY_URL", "http://pushgateway:9091")


registry = CollectorRegistry()
requests_count = Gauge(
    'requests_count',
    'Request count',
    ['command'],
    registry=registry
)
