#!/usr/bin/env python3
"""
Test feedback form submission to debug the error
"""

from playwright.sync_api import sync_playwright
import json

def test_feedback_submission():
    """Test the feedback form submission and capture the error"""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Capture console messages and network requests
        page = context.new_page()

        console_messages = []
        network_responses = []

        # Listen to console
        page.on('console', lambda msg: console_messages.append({
            'type': msg.type,
            'text': msg.text
        }))

        # Listen to network responses
        def handle_response(response):
            if 'github.com/repos' in response.url:
                network_responses.append({
                    'url': response.url,
                    'status': response.status,
                    'statusText': response.status_text,
                    'body': response.text() if response.status != 200 else 'Success'
                })

        page.on('response', handle_response)

        # Navigate to page
        print("🌐 Navigating to permit page...")
        page.goto('https://permitindex.com/california/contractor-license/')
        page.wait_for_load_state('networkidle')

        # Find and fill the form
        print("\n📝 Filling out feedback form...")

        # Select feedback type
        page.select_option('#feedback-type', 'tip')
        print("  ✓ Selected feedback type: tip")

        # Fill feedback text
        page.fill('#feedback-text', 'Test feedback from automated test')
        print("  ✓ Filled feedback text")

        # Submit form
        print("\n🚀 Submitting form...")
        page.click('#submit-btn')

        # Wait for response (max 10 seconds)
        try:
            page.wait_for_selector('#feedback-message:not(.hidden)', timeout=10000)
            message = page.locator('#feedback-message').inner_text()
            print(f"\n📨 Form Response:\n{message}")
        except:
            print("\n⏱️  Timeout waiting for response")

        # Print network responses
        print("\n🌐 Network Responses:")
        for response in network_responses:
            print(f"\nURL: {response['url']}")
            print(f"Status: {response['status']} {response['statusText']}")
            print(f"Body: {response['body']}")

        # Print console messages
        print("\n💬 Console Messages:")
        for msg in console_messages:
            print(f"[{msg['type']}] {msg['text']}")

        # Keep browser open for inspection
        input("\n\nPress Enter to close browser...")
        browser.close()

if __name__ == '__main__':
    test_feedback_submission()
