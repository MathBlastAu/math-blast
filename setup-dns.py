#!/usr/bin/env python3
"""
Set up DNS for math-blast.com.au on VentraIP to point to GitHub Pages.
GitHub Pages A records:
  185.199.108.153
  185.199.109.153
  185.199.110.153
  185.199.111.153
CNAME for www: mathblastau.github.io
"""

from playwright.sync_api import sync_playwright
import time

EMAIL = "bethany.hiemstra@gmail.com"
PASSWORD = "ZSTLiving2026GO!"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Navigating to VentraIP login...")
        page.goto("https://vip.ventraip.com.au/login", wait_until="networkidle", timeout=30000)
        page.screenshot(path="/tmp/ventraip-1-login.png")
        print("Screenshot 1 taken")

        # Fill login form
        page.fill('input[type="email"], input[name="email"], input[id="email"]', EMAIL)
        page.fill('input[type="password"], input[name="password"], input[id="password"]', PASSWORD)
        page.screenshot(path="/tmp/ventraip-2-filled.png")
        print("Screenshot 2 taken (form filled)")

        page.click('button[type="submit"], input[type="submit"]')
        page.wait_for_load_state("networkidle", timeout=15000)
        page.screenshot(path="/tmp/ventraip-3-after-login.png")
        print(f"After login URL: {page.url}")
        print("Screenshot 3 taken")

        # Look for domains section
        print(f"Page title: {page.title()}")
        print(f"Current URL: {page.url}")

        # Navigate to domains
        page.goto("https://vip.ventraip.com.au/domains", wait_until="networkidle", timeout=30000)
        page.screenshot(path="/tmp/ventraip-4-domains.png")
        print(f"Domains page: {page.url}")

        # Extract domain list
        content = page.content()
        print("Page content snippet:", content[:2000])

        browser.close()

if __name__ == "__main__":
    run()
