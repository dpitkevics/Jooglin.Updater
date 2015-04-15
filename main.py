from browser_updater import chrome

# import sys
# from systemlib.app_process import pkill
# pkill("chrome.exe")
# sys.exit()

chrome_updater = chrome.ChromeUpdater()
is_execution_successful = chrome_updater.execute_search_engine_change()

print(is_execution_successful)