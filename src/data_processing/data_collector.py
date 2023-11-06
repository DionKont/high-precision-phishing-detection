import logging

# Configure logging
logging.basicConfig(filename='data_collection.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

from phishing_collector import PhishingCollector
from legitimate_collector import LegitimateCollector


def main():
    # URLs for phishing and legitimate URL feeds
    phishing_feed_url = 'https://openphish.com/feed.txt'
    legitimate_feed_url = 'https://tranco-list.eu/top-1m.csv.zip'  # Tranco list in a zip file

    # Initialize collectors
    phishing_collector = PhishingCollector(phishing_feed_url)
    legitimate_collector = LegitimateCollector(legitimate_feed_url, limit=500)

    # Collect phishing URLs
    phishing_urls = phishing_collector.collect_urls()
    phishing_collector.save_urls(phishing_urls, 'phishing_urls.txt')

    # Collect legitimate URLs
    legitimate_urls = legitimate_collector.collect_urls()
    legitimate_collector.save_urls(legitimate_urls, 'legitimate_urls.txt')

if __name__ == "__main__":
    main()

