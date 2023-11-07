import re
from urllib.parse import urlparse
import tldextract
import math
from collections import Counter

def calculate_entropy(string):
    """Calculate entropy of a given string."""
    # Probabilities of each character
    p, lns = Counter(string), float(len(string))
    # Calculate the entropy
    return -sum(count/lns * math.log(count/lns, 2) for count in p.values())

def extract_url_features(url):
    """
    Extract features from a single URL.
    :param url: The URL to extract features from.
    :return: A dictionary containing features of the URL.
    """
    parsed_url = urlparse(url)
    extracted_url = tldextract.extract(url)
    features = {
        'length': len(url),
        'is_https': parsed_url.scheme == 'https',
        'domain': extracted_url.domain,
        'num_subdomains': len(extracted_url.subdomain.split('.')) if extracted_url.subdomain else 0,
        'path_length': len(parsed_url.path),
        'num_query_components': len(parsed_url.query.split('&')) if parsed_url.query else 0,
        'entropy': calculate_entropy(url),
        'contains_ip': bool(re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", url)),
        'uses_shortening_service': 'bit.ly' in url or 'goo.gl' in url or 'tinyurl.com' in url,
        'suspicious_words_count': sum(map(url.lower().count, ["confirm", "account", "banking", "secure", "update"])),
        'url_depth': url.count('/'),
        'tld_count': url.count('.'),
        'special_char_count': len(re.findall(r'\W', url)),
    }
    return features