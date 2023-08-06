# Basic Web Scraper

## Project Description
This package can be used for simple automated web surfing / scraping.

Additionally, the included BasicSpider class is meant to be extended by inheritance.

---

### Usage Example
```python
from basic_web_scraper.BasicSpider import BasicSpider

class CustomSpider(BasicSpider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def custom_operation(self, threshold):
        """
        Scroll to predefined threshold.
        If past threshold, scroll back up.
        """
        if self.get_page_y_offset() < threshold:
            self.mousewheel_vscroll(number_of_scrolls=2)

        else:
            y_difference = self.get_page_y_offset() - threshold
            self.smooth_vscroll_up_by(y_difference)


```

---

## Details about files

### __geckodriver.exe | geckodriver__

Keep this file in local directory when using scraper on windows. If you're using a linux system, make sure to include geckodriver in PATH variable. Downloaded from [here](https://github.com/mozilla/geckodriver/releases)

Note: geckodriver.exe is for windows, and geckodriver (no extension) is for Linux

### [__BasicSpider.py__](https://github.com/aziznal/basic-web-scraper/blob/master/BasicSpider.py)

Use this as the superclass for your own project's spider

This Spider can do basic things like goto a url, scroll down the page in different ways, refresh the page, etc..

It acts as an interface to _**selenium.webdriver**_ to make setting up a project easier

### __custom_exceptions.py__

Copy alongside BasicSpider.py, add any custom exceptions to this file.

### __package.json__ | package-lock.json
used to install dependencies related to testing and its related workflows. not needed for the spider to function.

### __start_local_server.py__
used for testing. optional.

### __tests.py__
this is where all the tests for the scraper are done. optional.

### __mock_webpage__
used for testing. optional. can be used as a simple demo.
