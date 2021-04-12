import csv
from json import JSONDecodeError
import logging
import random
import requests
import typing
import validators

from constants import FIELDS, GOOGLE_API
from exceptions import URLValidationError


def generate_random_number():
    return random.randint(1000000, 9999999)


class GooglePageAnalysis:
    def __init__(self, url):
        self.url: typing.Optional[str] = url
        self.report: typing.Optional[dict] = None
        self._validate_url()

    def _validate_url(self):
        if not validators.url(self.url):
            raise URLValidationError("URL is not correct")

    def _write_to_csv(self):
        filename = f'output/output_{generate_random_number()}.csv'
        with open(filename, 'w+', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['URL'] + [title for title in self.report])
            writer.writerow([self.url] + [self.report[key] for key in self.report])
        return filename

    def _get_page_google_analysis(self):
        logging.info(f"Sending GET request to {GOOGLE_API}...")
        try:
            response = requests.get(
                url=GOOGLE_API,
                params=
                {
                    'url': self.url,
                }
            ).json()
        except JSONDecodeError as err:
            logging.warning(f"Error raised while Google API request: {err}")
            return

        logging.info(f"Successfully received response: {str(response)[:10]}")

        output = {}
        try:
            audits = response['lighthouseResult']['audits']

            for field in FIELDS:
                output[field] = round(audits[field]['numericValue'], 3)

        except (KeyError, TypeError) as err:
            logging.warning(f"Possible timeout! Error raised while getting fields from Lighthouse Result: {err}")

        return output

    def get_report(self):
        logging.info("Getting report...")
        self.report = self._get_page_google_analysis()
        if self.report is not {}:
            filename = self._write_to_csv()
            logging.info(f"Report saved to ./{filename}")
        else:
            logging.info("Report failed to be created!")
