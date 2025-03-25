#VOICE ASSISTANT
AI Voice Assistant with Arc Reactor Interface
Introduction
This is an advanced AI-powered voice assistant built using Python, designed to help users perform various tasks using voice commands. The assistant features a futuristic Arc Reactor-inspired graphical user interface (GUI) created with Pygame, enhancing the user experience with real-time animations and voice interaction.

Features
🎙 Voice Recognition: Converts voice commands into text using Google Speech Recognition.
🔊 Text-to-Speech (TTS): Uses pyttsx3 to respond in a human-like voice.

🌐 Web Browsing & Searches:
Opens websites like Google, YouTube, Facebook, Twitter, LinkedIn, Instagram, and WhatsApp.
Searches Wikipedia and Google for user queries.

📨 Messaging & Email Support:
Sends WhatsApp messages using pywhatkit.
Sends emails via SMTP.

📂 File Management:
Creates and organizes folders.
Lists files by extension.
Locks and unlocks folders with password protection.

🎵 Entertainment:
Plays music from a local directory.
Searches and plays YouTube videos.

📸 Utilities:
Takes screenshots.
Opens camera for live streaming.
Reads PDF books aloud.
Retrieves system battery percentage.

🏠 Smart Assistant Functions:
Provides greetings based on the time of day.
Retrieves IP address & location.
Fetches weather and temperature details.
🔢 Mathematical Calculations: Solves basic arithmetic problems through voice commands.

Graphical User Interface (GUI)
The Arc Reactor-inspired interface displays animated effects.
Messages from the assistant are shown on-screen for a futuristic look.
The UI is created using Pygame, providing a real-time, interactive experience.

How to Use
Run the script (python main.py or relevant filename).
Speak a command (e.g., "open YouTube," "send a WhatsApp message," "what is my IP?").
The assistant will listen, process, and execute the requested action.
To exit, say "goodbye" or close the window.

Requirements
Ensure you have the following Python libraries installed:

pip install pyttsx3 SpeechRecognition PyPDF2 psutil pywhatkit wikipedia webbrowser requests pygame beautifulsoup4 smtplib pywikihow pyautogui opencv-python
