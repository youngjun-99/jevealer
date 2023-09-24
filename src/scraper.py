from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

class SummonerInfoScraper:
    def __init__(self) -> None:
        self.caps = DesiredCapabilities().CHROME
        self.caps["pageLoadStrategy"] = "none"
        self.options = Options()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_argument('headless')
        self.options.add_argument('window-size=2560,1440')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get('https://www.op.gg/multisearch/kr?summoners=')

    def get_image(self) :
        info = wait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'multi-list')))
        return info.screenshot_as_png