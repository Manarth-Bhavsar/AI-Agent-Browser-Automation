# Loom Link 

https://www.loom.com/share/7928653350f942f79de4e60cd6afab7f?sid=d48efac8-1f58-46b9-b707-4020c4efeef1

# 🤖 AI-Powered Browser Automation Agent (Lvl 1)

An intelligent, API-driven agent built that allows natural language commands to control native browser workflows (like Amazon or eBay), using GPT-based parsing and Selenium automation.

## 🚀 Project Overview
It takes natural language commands like:
> "Login to Amazon and search for Logitech MX Master 3 and add it to cart"

...and performs the following steps:
- Interprets the command using GPT
- Logs into the site (Amazon/eBay)
- Searches for the specified product
- Clicks on the best matching result or falls back to first product
- Adds the product to the cart

## 📁 Project Structure
```
project/
├── main.py                  # FastAPI app entry
├── api/                     # API routing layer
│   ├── routes.py            # /interact endpoint
│   └── models.py            # Pydantic schemas
├── agent/                   # GPT command parser
│   └── interpreter.py       # Uses OpenAI to parse commands
├── browser/
│   ├── driver.py            # Selenium browser setup
│   ├── actions.py           # Unified action logic for all sites
│   └── logins.py            # Site-specific login logic (Amazon, eBay)
├── config/                  # config placeholder (For Future use)
├── utils/                   # for edge cases (Future use)
├── tests/                   # For testing purposes
│   ├── test.py              # Testing different edge cases, output in test_results.log
├── test_results.log         # Logs the test results
├── requirements.txt        
└── README.md               

```

---

## ⚙️ How It Works
### 🧠 Natural Language → Parsed Command
We use OpenAI's GPT to extract structured data from a plain-text command:

**Input:**
```json
{
  "text": "Login to Amazon and search for Logitech MX Master 3 and add it to cart"
}
```

**Output from interpreter:**
```json
{
  "site": "amazon",
  "action": ["login", "search", "interact_element", "add_to_cart"],
  "search_item": "Logitech MX Master 3",
  "match_keyword": "MX Master 3"
}
```

---

### 🕹️ Actions Supported
- `login`: Signs into supported sites
- `search`: Enters the search term and submits
- `interact_element`: Finds and clicks best matching result
- `add_to_cart`: Adds the clicked item to the cart

These actions are dynamically dispatched from one function using a unified structure.

---

## ✅ How to Run

### 1. Clone the Repo
```bash
git clone <repo_url>
cd project
```

### 2. Setup Environment
Create a `.env` file:
```env
OPENAI_API_KEY=your-openai-key
AMAZON_USERNAME=your-email
AMAZON_PASSWORD=your-password
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Start the Server
```bash
uvicorn main:app --reload
```

### 5. Send Requests (via Postman or PowerShell)
```powershell
$json = '{"text": "Search for iPhone 13 case on eBay and add to cart"}'
Invoke-RestMethod -Uri http://localhost:8000/interact -Method Post -Body $json -ContentType "application/json"
```

---

## 💥 Edge Cases Handled
| Case | Behavior |
|------|----------|
| `match_keyword` missing or same as `search_item` | Fallback to first result |
| Login not required (already signed in) | Skips login |
| Invalid selectors | Handled with try/except and fallback click |
| GPT output missing fields | Returns error message gracefully |
| CAPTCHA or 2FA or JS popups| Manual Steps required |
| Add to cart but not logged in | Asks of Login |

---

## 🧪 Test Prompts
- "Search for USB-C cable on Amazon and add to cart"
- "Search for wireless earbuds on eBay"
- "Login to Amazon and search for noise cancelling headphones"
- "Search for Banana printer and add to cart" (should fallback to first result)

---

## 🎯 Future Improvements
- Full Extract API (Level 2)
- Config-driven selectors per site
- Native Chrome control (Level 2+)
---

## 🧑‍💻 Author
Built by Manarth Bhavsar for CrustData Build Challenge (Lvl 1)

