from playwright.sync_api import sync_playwright


def take_screenshot_from_url(url, session_data):
    # Context manager to wrap the Playwright code
    with sync_playwright() as playwright:
        # create and launch a headless WebKit browser
        webkit = playwright.webkit
        browser = webkit.launch()
        # new context for the browser named browser_context.
        # Set the device_scale_factor to 2. Increasing the scale factor
        # will make sure that the picture you take isn’t pixelated.
        browser_context = browser.new_context(device_scale_factor=2)
        # adds the session info to browser_context with .add_cookies()
        browser_context.add_cookies([session_data])
        # opens a new browser window in your browser_context.
        page = browser_context.new_page()
        # visits the target URL
        page.goto(url)
        # takes a screenshot of the element with a code class.
        screenshot_bytes = page.locator(".code").screenshot()
        # closes the browser
        browser.close()
        # returns the image buffer
        return screenshot_bytes
