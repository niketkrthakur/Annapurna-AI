# Annapurna-AI
Annapurna AI – A Python-based demo to interact with the Annapurna AI API using POST requests for authentication and data submission.
🚀 Annapurna AI – Python API Demo

Annapurna AI is a lightweight Python demo project that shows how to interact with the Annapurna AI API using POST requests. It demonstrates user authentication, data submission, and basic API integration in Python.

🌟 Features

✅ Simple Python integration with Annapurna AI API

✅ Demonstrates POST request authentication

✅ Handles success and failure responses

✅ Easy to extend for other API functionalities

📦 Installation

Clone the repository:

git clone https://github.com/your-username/annapurna-ai-demo.git


Navigate to the project folder:

cd annapurna-ai-demo


Install required dependencies:

pip install requests

🛠️ Usage

Open main.py (or your script file).

Update the username and password fields with your credentials.

Run the script:

python main.py


You will see a message indicating whether login was successful or failed.

💻 Code Example
import requests

url = "https://www.annapurna_ai.com/post"
data = {
    "username": "Niket",
    "password": 5123456
}

response = requests.post(url, data=data)

if response.status_code == 200:
    print("☑️ Login Successful")
else:
    print("❌ Login Failed")

🤝 Contributing

We welcome contributions! You can:

Improve documentation 📚

Add new API endpoints or features 🔧

Implement better error handling and logging 🛠️

📜 License

This project is open source and licensed under the MIT License.
