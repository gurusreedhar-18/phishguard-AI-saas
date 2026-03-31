import re
from urllib.parse import urlparse

def extract_features(url):
    features = []

    # Length of URL
    features.append(len(url))

    # Count of special characters
    features.append(url.count('.'))
    features.append(url.count('-'))
    features.append(url.count('@'))
    features.append(url.count('?'))
    features.append(url.count('%'))
    features.append(url.count('='))

    # Has IP address
    ip_pattern = re.compile(
        r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
        r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
    )
    features.append(1 if ip_pattern.search(url) else 0)

    # HTTPS or not
    features.append(1 if url.startswith("https") else 0)

    # Length of domain
    domain = urlparse(url).netloc
    features.append(len(domain))

    return features