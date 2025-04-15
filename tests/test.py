import requests
import json
from datetime import datetime

# Test case list
test_cases = [
    {
        "description": "✅ Basic Amazon login + search + add to cart",
        "prompt": "Login to Amazon and search for Logitech K380 keyboard and add it to cart"
    },
    {
        "description": "✅ Basic eBay search only",
        "prompt": "Search for iPhone 13 cases on eBay"
    },
    {
        "description": "⚠️ No match_keyword fallback (search item = match), Also early exit after searching as not logged in",
        "prompt": "Search for USB-C charging cable on Amazon and add it to cart"
    },
    {
        "description": "⚠️ Product not found, trigger fallback to first result",
        "prompt": "Search for Banana Printer on eBay and add it to cart"
    },
    {
        "description": "❌ Missing site",
        "prompt": "Search for gaming chair and add to cart"
    },
    {
        "description": "❌ Unsupported action",
        "prompt": "Search for headphones on Amazon and leave a review"
    },
    {
        "description": "🧠 Complex language (LLM test)",
        "prompt": "Go to Amazon, log in with my credentials, then search for wireless mouse and add the one that’s cheapest to the cart"
    },
    {
        "description": "⚠️ Partial command (missing search)",
        "prompt": "Add to cart on Amazon"
    }
]

# Output log file
log_file = "test_results.log"

# API endpoint
url = "http://localhost:8000/interact"

def log_to_file(entry):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

# Start testing
log_to_file(f"\n--- Test Run @ {datetime.now()} ---\n")

for i, test in enumerate(test_cases, start=1):
    description = test["description"]
    prompt = test["prompt"]

    print(f"[{i}] Running: {description}")

    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"text": prompt})
        )

        result = response.text
        log_entry = f"""
[Test {i}] {description}
Prompt: {prompt}
Response: {result}
{"="*60}
"""
        log_to_file(log_entry)

    except Exception as e:
        error_log = f"""
[Test {i}] {description}
Prompt: {prompt}
Error: {str(e)}
{"="*60}
"""
        log_to_file(error_log)

print(f"\n✅ All test cases completed. Check '{log_file}' for results.")
