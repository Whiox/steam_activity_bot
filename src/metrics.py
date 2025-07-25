from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import os


USE_PROMETHEUS = os.getenv("USE_PROMETHEUS", False)


PUSHGW = os.getenv("PUSHGATEWAY_URL", "http://pushgateway:9091")


registry = CollectorRegistry()
requests_count = Gauge(
    'requests_count',
    'Request count',
    ['command'],
    registry=registry
)

parsing_count = Gauge(
    'parsing_count',
    'Parsing count',
    ['status'],
    registry=registry
)
