# The url: http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv
import argparse
import csv
from datetime import datetime
import re
import sys
from urllib.request import urlopen


def downloadData(url):
    """Pulls down web log file """

    response = urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]  # decoding and putting lines from file into a list
    return lines


def processData(lines):
    img_index = 0
    total_index = 0

    data = csv.reader(lines)  # feeding output from downloadData() into a reader object

    for row in data:
        total_index += 1
        x = re.search("PNG|JPG|GIF$", row[0], re.IGNORECASE)
        if bool(x) == True:
            img_index += 1

    percent_of_img = int(round(img_index / total_index * 100))
    message = "Image requests account for {}% of all requests".format(percent_of_img)

    print(message)


def browserChecker(lines):
    data = csv.reader(lines)

    browser_dict = {
        "Chrome": 0,
        "Firefox": 0,
        "Internet Explorer": 0,
        "Safari": 0
    }

    for row in data:
        c = re.search("Chrome/*.*$", row[2], re.IGNORECASE)
        f = re.search("Firefox/*.*$", row[2], re.IGNORECASE)
        i = re.search("MSIE|Trident", row[2], re.IGNORECASE)
        s = re.search("Safari/*.*$", row[2], re.IGNORECASE)

        if bool(c) == True:
            browser_dict["Chrome"] += 1
        elif bool(f) == True:
            browser_dict["Firefox"] += 1
        elif bool(i) == True:
            browser_dict["Internet Explorer"] += 1
        elif bool(s) == True:
            browser_dict["Safari"] += 1

    maximum = max(browser_dict, key=browser_dict.get)

    for key, value in browser_dict.items():
        print(key, value)
        if key == maximum:
            hits = value

    print(f"The most popular browser used today was: {maximum} ({hits})")


# extra credit
def hourGetter(lines):
    print("------------------------ Extra Credit ------------------------")

    data = csv.reader(lines)

    hour_dict = {
        "one": 0,
        "two": 0,
        "three": 0,
        "four": 0,
        "five": 0
    }

    for row in data:

        try:
            x = re.split(r'\s', row[1])
            dt_obj = datetime.strptime(x[1], '%I:%M:%S').time()
            if dt_obj.hour == 1:
                hour_dict["one"] += 1
            elif dt_obj.hour == 2:
                hour_dict["two"] += 1
            elif dt_obj.hour == 3:
                hour_dict["three"] += 1
            elif dt_obj.hour == 4:
                hour_dict["four"] += 1
            if dt_obj.hour == 5:
                hour_dict["five"] += 1

        except Exception as error:
            pass

    for key, value in hour_dict.items():
        print(f'Hour {key} has {value} hits')


def main(url):
    print(f"Running main with URL = {url}...")

    processData(downloadData(url))
    browserChecker(downloadData(url))
    hourGetter(downloadData(url))


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)