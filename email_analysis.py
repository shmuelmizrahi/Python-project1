import requests
import re
from bs4 import BeautifulSoup
import datetime
import logging

# Configure logging
logging.basicConfig(filename='sim.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_emails(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        email_regex = r"[\w\.-]+@[\w\.-]+"
        emails = re.findall(email_regex, soup.get_text())
        return emails
    else:
        logging.error(f"Failed to fetch emails from {url}: Status code {response.status_code}")
        return []


def analyze_emails(emails):
    suspicious_emails = []
    for email in emails:
        if "admin" in email or "support" in email:
            suspicious_emails.append(email)
    return suspicious_emails


def check_ddos_traffic(requests_per_minute):
    threshold = 100  # Example threshold for requests per minute
    if requests_per_minute > threshold:
        logging.warning("Possible DDoS attack detected!")


def is_suspicious_login(attempts, last_login_time):
    current_time = datetime.datetime.now()
    midnight = datetime.datetime.combine(current_time.date(), datetime.time.min)
    if last_login_time > midnight:
        logging.warning("Suspicious login detected: User logged in after midnight.")

    if attempts > 3:
        logging.warning("Suspicious login detected: User failed to login more than 3 times.")


def main():
    urls = ["https://example1.com", "https://example2.com", "https://example3.com"]
    all_emails = []
    for url in urls:
        emails = fetch_emails(url)
        all_emails.extend(emails)

    suspicious_emails = analyze_emails(all_emails)
    if suspicious_emails:
        logging.info("Suspicious emails found:")
        for email in suspicious_emails:
            logging.info(email)

    # Example data for login attempts
    login_attempts = 4
    last_login = datetime.datetime.now() - datetime.timedelta(hours=2)  # Example: 2 hours ago
    is_suspicious_login(login_attempts, last_login)

    # Example data for DDoS traffic check
    requests_per_minute = 120  # Example: 120 requests per minute
    check_ddos_traffic(requests_per_minute)

    logging.info("Script execution completed.")


if __name__ == "__main__":
    main()

