"""
Quick Demo: Hello World
Tests the connection between the script and NST Browser
Opens a tab in NST Browser and types "Hello world" using keyboard automation
"""

import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()

async def main():
    """Demo function to test NST Browser connection"""
    print("🚀 Starting Hello World Demo...")
    
    nst_browser_url = os.getenv('NST_BROWSER_URL', 'ws://localhost:3000')
    dev_mode = os.getenv('DEV_MODE', 'false').lower() == 'true'
    
    playwright = await async_playwright().start()
    
    try:
        # Try to connect to NST Browser
        if nst_browser_url:
            try:
                print(f"🔌 Attempting to connect to NST Browser at {nst_browser_url}...")
                browser = await playwright.chromium.connect_over_cdp(nst_browser_url)
                print("✅ Connected to NST Browser!")
            except Exception as e:
                print(f"⚠️  Could not connect to NST Browser: {e}")
                print("🔄 Falling back to local browser...")
                browser = await playwright.chromium.launch(headless=not dev_mode)
        else:
            browser = await playwright.chromium.launch(headless=not dev_mode)
            print("✅ Local browser launched")
        
        # Create a new context and page
        context = await browser.new_context()
        page = await context.new_page()
        
        # Navigate to a simple page
        print("📄 Opening page...")
        await page.goto('https://www.google.com')
        await page.wait_for_load_state('networkidle')
        
        # Find the search box and type "Hello world"
        print("⌨️  Typing 'Hello world'...")
        search_box = page.locator('textarea[name="q"], input[name="q"]')
        await search_box.fill('Hello world')
        
        print("✅ Demo completed successfully!")
        print("💡 If you see 'Hello world' in the search box, the automation is working!")
        
        # Keep browser open for a few seconds if in dev mode
        if dev_mode:
            print("⏳ Keeping browser open for 5 seconds (DEV_MODE=true)...")
            await asyncio.sleep(5)
        else:
            await asyncio.sleep(2)
        
        # Cleanup
        await context.close()
        await browser.close()
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await playwright.stop()
        print("✅ Demo finished")

if __name__ == "__main__":
    asyncio.run(main())

