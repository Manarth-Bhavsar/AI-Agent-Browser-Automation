from fastapi import APIRouter
from api.models import CommandInput
from agent import interpreter
from browser import driver
from browser import actions as site_actions

router = APIRouter()

@router.post("/interact")
def interact(command: CommandInput):
    parsed = interpreter.parse_command(command.text)
    print(parsed)
    site = parsed.get("site")
    action_list = parsed.get("action",[])

    if not site or not action_list:
        return {"status":"error", "message":"Missing site, action or keyword in parsed command."}
    
    browser = driver.get_driver()
    try:
        executed = site_actions.execute_actions(browser,site,action_list,parsed)
        print(f"Executing actions for site={site}: {executed}")
        return {"status": "ok", "executed": executed, "site": site}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        browser.quit()