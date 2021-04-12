import sys
from lighthouse import GooglePageAnalysis
import logging

logging.basicConfig(
    format="{asctime} {levelname:<8} {message}",
    style="{",
    level=logging.DEBUG,
    stream=sys.stdout,
)

if __name__ == '__main__':
    print("Input URL (with http/https): ")
    url_input = input()
    lighthouse = GooglePageAnalysis(url_input)
    lighthouse.get_report()
    logging.info("Exiting program..")
