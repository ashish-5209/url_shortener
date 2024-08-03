from prometheus_client import Counter, Histogram

# Metrics for tracking URLs shortened and redirected
URLS_SHORTENED = Counter('urls_shortened', 'Number of URLs shortened')
URLS_REDIRECTED = Counter('urls_redirected', 'Number of URL redirects')
REQUEST_TIME = Histogram('request_duration_seconds', 'Request duration in seconds', ['method', 'endpoint'])
