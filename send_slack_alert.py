import requests
import json

SLACK_WEBHOOK_URL = "SLACK_WEBHOOK_URL"

def send_alert(message):
payload = {"text": message}
response = requests.post(
SLACK_WEBHOOK_URL, 
data=json.dumps(payload),
headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
print("✅ Alert sent successfully!")
else:
print("❌ Failed to send alert:", response.text)

if __name__ == "__main__":
send_alert("🚨 Slack Bot Test: The notification system is working!")

