# coding: utf-8
"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 10/20/24
"""
import pathlib
import sys

# add project directory to path
THIS_FILE_PATH = pathlib.Path(__file__).absolute()
THIS_FILE_PARENT_DIR = THIS_FILE_PATH.parent
PROJECT_DIR = THIS_FILE_PARENT_DIR.parent.parent
sys.path.append(str(PROJECT_DIR))
print(f"[INFO] - append directory to path: {PROJECT_DIR}")

import asyncio
import nodriver as uc
from nodriver.core.config import Config
from sunacchi.utils.log_tool import create_logger


async def main(headless=False, logger=None):
    """
    enable headless mode for me
    """
    if logger:
        logger.info(f"Starting main with headless mode: {headless}")

    if headless:
        browser_args = ['--headless=new']
        config = Config(headless=True)
    else:
        browser_args = None
        config = Config()

    browser = await uc.start(config, browser_args=browser_args)
    if logger:
        logger.info("Browser started successfully")

    first_test_url = 'https://www.cityline.com/'
    # first_test_url = 'https://youtube.com/'
    if logger:
        logger.info(f"Opening URL: {first_test_url}")

    page = await browser.get(first_test_url)
    logger.info(f"accessed {first_test_url} successfully")

    await page.save_screenshot()
    if logger:
        logger.info("Saved screenshot of the page")

    await page.get_content()
    await page.scroll_down(150)
    if logger:
        logger.info("Scrolled down 150 units")

    elems = await page.select_all('*[src]')
    if logger:
        logger.info(f"Found {len(elems)} elements with 'src' attribute")

    logger.info("Flashing elements with 'src' attribute ...")
    for elem in elems:
        await elem.flash()
        if logger:
            # logger.info(f"Flashing element: {elem}")
            pass
    logger.info("Flashing completed")

    page2 = await browser.get('https://twitter.com', new_tab=True)
    if logger:
        logger.info("Opened Twitter in a new tab")

    page3 = await browser.get('https://github.com/ultrafunkamsterdam/nodriver', new_window=True)
    if logger:
        logger.info("Opened GitHub nodriver page in a new window")

    for p in (page, page2, page3):
        await p.bring_to_front()
        if logger:
            logger.info("Brought page to front")

        await p.scroll_down(200)
        if logger:
            logger.info("Scrolled down 200 units")

        await p.reload()
        if logger:
            logger.info("Reloaded page")

        if p != page3:
            await p.close()
            if logger:
                logger.info("Closed the page")


if __name__ == '__main__':
    # since asyncio.run never worked (for me)

    logger_name = f"{THIS_FILE_PATH.stem}"
    log_path = THIS_FILE_PARENT_DIR / f"{logger_name}.log"
    logger = create_logger(logger_name, log_path=log_path)

    use_headless = True

    uc.loop().run_until_complete(main(headless=use_headless, logger=logger))
    logger.info("Script completed")
