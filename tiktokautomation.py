import os
import sys
import json
import time
import random
import tkinter as tk
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'tiktok_config.json')
VIDEO_FOLDER = 'tiktok_upload_videos'

class TikTokManager:
    def __init__(self):
        self.driver = None
        self.config = self.load_config()
        self.service = Service(ChromeDriverManager().install())

    def load_config(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            return {'registered': False, 'cookies': []}
        except Exception as e:
            print(f"config error: {e}")
            return {'registered': False, 'cookies': []}

    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)

    def init_browser(self, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--log-level=3")
        options.add_argument("--lang=en-US")
        options.add_argument("--disable-webrtc")

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        options.add_argument(f"user-agent={user_agent}")

        return webdriver.Chrome(service=self.service, options=options)

    def register_user(self):
        try:
            self.driver = self.init_browser(headless=False)
            self.driver.get("https://www.tiktok.com/login/")

            print("please log in your tiktok account")
            WebDriverWait(self.driver, 300).until(EC.url_contains("https://www.tiktok.com/@"))

            self.config['cookies'] = self.driver.get_cookies()
            self.config['registered'] = True
            self.save_config()

            print("registration completed!")
            return True
        except Exception as e:
            print(f"error with registration: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()

    def type_description_with_hashtags(self, desc_field, description):
        actions = ActionChains(self.driver)
        actions.move_to_element(desc_field)
        actions.click()
        actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
        actions.send_keys(Keys.DELETE)
        actions.perform()
        time.sleep(0.5)

        i = 0
        while i < len(description):
            if description[i] == '#':
                actions.send_keys('#')
                actions.perform()
                time.sleep(random.uniform(0.2, 0.3))
                i += 1
                while i < len(description) and not description[i].isspace():
                    actions.send_keys(description[i])
                    actions.perform()
                    time.sleep(random.uniform(0.2, 0.3))
                    i += 1
                time.sleep(1.5)
                actions.send_keys(Keys.ARROW_DOWN)
                actions.send_keys(Keys.ENTER)
                actions.perform()
                if i < len(description) and description[i].isspace():
                    actions.send_keys(" ")
                    actions.perform()
                    i += 1
            else:
                actions.send_keys(description[i])
                actions.perform()
                time.sleep(random.uniform(0.2, 0.3))
                i += 1

        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", desc_field
        )
        time.sleep(random.uniform(1, 2))

    def upload_video(self, video_path, description):
        try:
            self.driver = self.init_browser(headless=True)
            self.driver.get("https://www.tiktok.com/")
            time.sleep(2)

            self.driver.delete_all_cookies()
            for cookie in self.config['cookies']:
                if 'expiry' in cookie:
                    del cookie['expiry']
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    print(f"error cookie download: {e}")

            self.driver.refresh()
            time.sleep(3)

            self.driver.get("https://www.tiktok.com/upload")
            time.sleep(2)

            upload_input = WebDriverWait(self.driver, 45).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
            )
            upload_input.send_keys(os.path.abspath(video_path))

            WebDriverWait(self.driver, 120).until(
                EC.invisibility_of_element_located((By.XPATH, '//div[contains(@class,"progress-container")]'))
            )

            desc_xpath = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]'
            desc_field = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, desc_xpath))
            )
            self.type_description_with_hashtags(desc_field, description)

            publish_btn = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div/button[1]'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", publish_btn)
            time.sleep(1)
            publish_btn.click()

            WebDriverWait(self.driver, 90).until(lambda d: "upload" not in d.current_url.lower())
            print("✅ video succesfully published!")

            os.remove(video_path)
            print(f"🗑 file {video_path} deleted")

            os._exit(0)

        except Exception as e:
            print(f"🚨 publish error: {e}")
            self.driver.save_screenshot('error.png')

        finally:
            if self.driver:
                self.driver.quit()

class VideoWatcher(FileSystemEventHandler):
    def __init__(self, uploader):
        self.uploader = uploader

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.mp4', '.mov', '.avi')):
            root = tk.Tk()
            root.withdraw()
            description = simpledialog.askstring("Description: ", "Enter description with hastags:")
            root.destroy()

            if description:
                print(f"🚀 download started: {event.src_path}")
                self.uploader.upload_video(event.src_path, description)

def main():
    if not os.path.exists(VIDEO_FOLDER):
        os.makedirs(VIDEO_FOLDER)

    manager = TikTokManager()
    if not manager.config.get('registered', False):
        if not manager.register_user():
            return
    print("Waiting for new videos...")
    observer = Observer()
    handler = VideoWatcher(manager)
    observer.schedule(handler, VIDEO_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
