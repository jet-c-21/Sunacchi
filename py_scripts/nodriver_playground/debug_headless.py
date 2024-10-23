# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/23/24
"""
import nodriver as uc
from pprint import pp


async def main(args):
    config = uc.Config(
        headless=True,
        browser_executable_path='/bin/google-chrome',
        lang='zh-TW',
        browser_args=[
            '--disable-2d-canvas-clip-aa',
            '--disable-3d-apis',
            '--disable-animations',
            '--disable-app-info-dialog-mac',
            '--disable-background-networking',
            '--disable-backgrounding-occluded-windows',
            '--disable-bookmark-reordering',
            '--disable-boot-animation',
            '--disable-breakpad',
            '--disable-canvas-aa',
            '--disable-client-side-phishing-detection',
            '--disable-cloud-import',
            '--disable-component-cloud-policy',
            '--disable-component-update',
            '--disable-composited-antialiasing',
            '--disable-default-apps',
            '--disable-dev-shm-usage',
            '--disable-device-discovery-notifications',
            '--disable-dinosaur-easter-egg',
            '--disable-domain-reliability',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-infobars',
            '--disable-logging',
            '--disable-login-animations',
            '--disable-login-screen-apps',
            '--disable-notifications',
            '--disable-office-editing-component-extension',
            '--disable-password-generation',
            '--disable-popup-blocking',
            '--disable-renderer-backgrounding',
            '--disable-search-engine-choice-screen',
            '--disable-session-crashed-bubble',
            '--disable-smooth-scrolling',
            '--disable-suggestions-ui',
            '--disable-sync',
            '--disable-translate',
            '--hide-crash-restore-bubble',
            '--homepage=about:blank',
            '--lang=zh-TW',
            '--no-default-browser-check',
            '--no-first-run',
            '--no-pings',
            '--no-sandbox',
            '--no-service-autorun',
            '--password-store=basic',
            '--remote-allow-origins=*',
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        ],
    )

    pp(config)

    driver = await uc.start(config)
    # driver = await uc.start(config, browser_args=['--headless=new'])
    # Rest of your code
    # test_url = 'https://www.cityline.com/'
    test_url = 'https://www.youtube.com/'
    page = await driver.get(test_url)
    await page.save_screenshot()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    # Add your arguments here
    args = parser.parse_args()
    uc.loop().run_until_complete(main(args))