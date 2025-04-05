from scraper import login_and_fetch_tasks

print("🔍 Fetching tasks...")

tasks = login_and_fetch_tasks()

print(f"✅ Found {len(tasks)} task(s)")
for task in tasks:
    print(f"{task['id']} – {task['title']}")
