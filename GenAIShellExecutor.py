import subprocess
import datetime
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

google_gemini_api_key = os.environ.get("GEMINI_API_KEY")

if not google_gemini_api_key:
    raise ValueError("❌ GEMINI_API_KEY environment variable not set.")

model = OpenAI(
    api_key=google_gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

LOG_FILE = "command_log.txt"

def get_linux_command_from_prompt(prompt):
    messages = [
        {"role": "system", "content": "You are a Linux terminal command generator. Only output the raw shell command without any explanation."},
        {"role": "user", "content": prompt}
    ]
    response = model.chat.completions.create(
        messages=messages,
        model="gemini-2.5-flash-preview-05-20"
    )
    return response.choices[0].message.content.strip()

def log_command(command, output):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"\n[{timestamp}] COMMAND: {command}\n")
        log_file.write(f"[{timestamp}] OUTPUT:\n{output}\n")
        log_file.write("="*60 + "\n")

print("\n\t🔧 Welcome to the AI-powered Linux Command Tool 🔧")
print("\t--------------------------------------------------")
print("Type 'exit' to stop.\n")

while True:
    user_prompt = input("🧠 What do you want to do on Linux? → ")

    if user_prompt.strip().lower() == "exit":
        print("👋 Exiting AI Linux tool. Goodbye!")
        break

    command = get_linux_command_from_prompt(user_prompt)
    print(f"\n💡 Suggested Command: {command}")

    confirm = input(f"⚠️ Do you want to run this command? (y/n): ").strip().lower()
    if confirm != "y":
        print("❌ Skipped command.\n")
        continue

    try:
        output = subprocess.getoutput(command)
        print("\n✅ Command executed successfully!")
        print("📄 Output:\n", output)
        log_command(command, output)
    except Exception as e:
        print("❗ Error while running command:", str(e))
