import hashlib
import operator
import time
import PyPDF2
import psutil
import pyttsx3
import requests
import speech_recognition as sr
import datetime
import os
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import cv2
import pyautogui
from pywikihow import search_wikihow
from bs4 import BeautifulSoup
import pygame
import math
from threading import Thread

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Voice Assistant - Arc Reactor Interface")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 204, 255)
LIGHT_BLUE = (173, 216, 230)

# Clock for controlling FPS
clock = pygame.time.Clock()

# Voice Assistant Status
assistant_running = True
messages_to_display = []  # Global variable to store messages for display

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

# Convert text to speech
def speak(audio):
    engine.say(audio)
    print(audio)  # Print to terminal
    messages_to_display.append(audio)  # Append to display messages
    engine.runAndWait()

# Convert voice into text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening!!!!")
        messages_to_display.append("Listening....")  # Log to display
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
    try:
        print("Recognizing....")
        messages_to_display.append("Recognizing....")  # Log to display
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        messages_to_display.append(f"user said: {query}")  # Log to display
    except Exception as e:
        speak("Please say that again....")
        return "none"
    return query

# Wish function
def wish():
    hour = int(datetime.datetime.now().hour)
    minute = int(datetime.datetime.now().minute)
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    
    if hour >= 0 and hour < 12:
        speak(f"Good Morning! It's {current_time}")
    elif hour >= 12 and hour < 18:
        speak(f"Good Afternoon! It's {current_time}")
    else:
        speak(f"Good Evening! It's {current_time}")
    
    speak("Hello Sir, I am your assistant. Please tell me how can I help you.")

def send_whatsapp_message():
    speak("Please type the phone number with country code.")
    phone_number = input("Enter phone number with country code: ").strip()
    speak("What is the message?")
    message = takecommand()
    
    from datetime import datetime
    now = datetime.now()
    hour = now.hour
    minute = now.minute + 1  # Schedule to send the message one minute from the current time

    try:
        kit.sendwhatmsg(phone_number, message, hour, minute)
        speak("Message sent successfully!")
        messages_to_display.append("Sent a WhatsApp message.")
    except Exception as e:
        speak("I am unable to send the message at this time. Please try again later.")

def send_email(to_address, subject, message_body):
    from_address = "anshugupta361646782@gmail.com"  # Replace with your email
    password = "kfpx ewzt uenf yniz"  # Replace with your app-specific password

    email_message = f"Subject: {subject}\n\n{message_body}"

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_address, password)
            server.sendmail(from_address, to_address, email_message)
        speak("The email has been sent successfully.")
        messages_to_display.append("Sent an email.")
    except Exception as e:
        print(e)
        speak("I'm unable to send the email at this time. Please check your settings.")

# Lock the folder by name
def lock_folder():
    speak("Please provide the name of the folder you want to lock.")
    folder_name = takecommand().lower()

    if not folder_name or not os.path.exists(folder_name):
        speak("The folder does not exist. Please try again.")
        return

    # Ask for a password
    speak("Please provide a password to lock this folder.")
    password = takecommand()

    if not password:
        speak("No password provided. Operation cancelled.")
        return

    # Hash the password for security
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Save the hashed password in a hidden file inside the folder
    try:
        with open(os.path.join(folder_name, ".password"), "w") as password_file:
            password_file.write(hashed_password)
        speak(f"The folder {folder_name} has been locked successfully.")
    except Exception as e:
        speak(f"An error occurred while locking the folder: {str(e)}")
        return

    # Hide the folder (Windows-specific)
    os.system(f'attrib +h {folder_name}')
    speak(f"The folder {folder_name} is now hidden and locked.")

# Unlock the folder by name
def unlock_folder():
    speak("Please provide the name of the folder you want to unlock.")
    folder_name = takecommand().lower()

    if not folder_name or not os.path.exists(folder_name):
        speak("The folder does not exist. Please try again.")
        return

    # Ask for the password
    speak("Please provide the password to unlock this folder.")
    password = takecommand()

    if not password:
        speak("No password provided. Access denied.")
        return

    # Verify the password
    try:
        with open(os.path.join(folder_name, ".password"), "r") as password_file:
            stored_hashed_password = password_file.read()

        if hashlib.sha256(password.encode()).hexdigest() == stored_hashed_password:
            # Unhide the folder
            os.system(f'attrib -h {folder_name}')
            speak(f"The folder {folder_name} has been unlocked successfully.")
        else:
            speak("Incorrect password. Access denied.")
    except FileNotFoundError:
        speak("Password file not found. This folder is not locked.")
    except Exception as e:
        speak(f"An error occurred while unlocking the folder: {str(e)}")

def create_folder():
    speak("Please tell me the name of the new folder.")
    folder_name = takecommand().lower()
    if folder_name == "none" or not folder_name.strip():
        speak("I couldn't get the folder name. Please try again.")
        return
    
    folder_path = os.path.join(os.getcwd(), folder_name)
    try:
        os.makedirs(folder_path)
        speak(f"The folder named {folder_name} has been created successfully.")
        messages_to_display.append(f"Created folder: {folder_name}")
    except FileExistsError:
        speak(f"A folder with the name {folder_name} already exists.")
    except Exception as e:
        print(e)
        speak("An error occurred while creating the folder. Please try again.")

def list_files_by_extension():
    speak("Please tell me the extension of the files you want to list.")
    extension = takecommand().lower()
    
    if extension == "none" or not extension.strip():
        speak("I couldn't understand the extension. Please try again.")
        return
    
    if not extension.startswith('.'):
        extension = '.' + extension

    drives = [f"{chr(65 + i)}:\\" for i in range(26) if os.path.exists(f"{chr(65 + i)}:\\")]
    found_files = []

    speak(f"Searching the entire PC for {extension} files. This might take some time.")
    
    for drive in drives:
        for root, _, files in os.walk(drive):
            for file in files:
                if file.endswith(extension):
                    found_files.append(os.path.join(root, file))
    
    if found_files:
        speak(f"I found {len(found_files)} {extension} files on your PC.")
        for file in found_files[:10]:
            print(file)
            messages_to_display.append(file)  # Log to display
    else:
        speak(f"Sorry, I couldn't find any {extension} files on your PC.")

def TaskExecution():
    while True:
        query = takecommand().lower()

        if "wake up" in query:
            wish()  # Greet the user
            break  # Exit the loop to start processing commands

    while True:
        query = takecommand().lower()

        # Logic building task
        if "open notepad" in query:
            npath = "C:\\Windows\\notepad.exe"
            os.startfile(npath)
            messages_to_display.append("Opened Notepad.")
        elif "close notepad" in query:  # for closing
            os.system("taskkill /f /im notepad.exe")
            messages_to_display.append("Closed Notepad.")

        elif "hello" in query or "hey" in query:  # basic commands
            speak("hello sir, may I help you with something.")

        elif "how are you" in query or "how r u" in query:
            speak("I am fine sir, what about you.")

        elif "also good" in query or "fine" in query:
            speak("that's great to hear from you.")

        elif "thank u" and "thank" in query:
            speak("it's my pleasure sir.")

        elif "you can sleep" in query or "sleep now" in query:
            speak("okay sir, I am going to sleep you can call me anytime.")
            TaskExecution()
            break

        elif "open command prompt" in query:
            os.system("start cmd")
        elif "close command prompt" in query:  # for closing
            os.system("taskkill /f /im cmd.exe")

        elif "play music" in query or "play song" in query:
            music_dir = "C:\\Users\\Anshu\\music1"
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
                messages_to_display.append("Playing music.")
            else:
                speak("No music files found in the specified directory.")
        
        elif "ip address" in query:
            ip = requests.get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")

        elif "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=4)
            speak("According to Wikipedia")
            speak(result)
            messages_to_display.append(result)

        elif "open camera" in query:
            speak("Opening camera.")
            cap = cv2.VideoCapture(0)  # 0 is the ID for the default webcam
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    cv2.imshow("Camera", frame)
                    # Press 'q' to close the camera
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break
            cap.release()
            cv2.destroyAllWindows()
            speak("Camera closed.")

        elif "open instagram" in query:
            webbrowser.open("https://www.instagram.com")
            messages_to_display.append("Opened Instagram.")
        elif "close instagram" in query:  # for closing
            os.system("taskkill /f /im chrome.exe")

        elif "open facebook" in query:
            webbrowser.open("https://www.facebook.com")
            messages_to_display.append("Opened Facebook.")
        elif "close facebook" in query:  # for closing
            os.system("taskkill /f /im chrome.exe")

        elif "open whatsapp" in query:
            webbrowser.open("https://web.whatsapp.com")
            messages_to_display.append("Opened WhatsApp.")
        elif "close whatsapp" in query:  # for closing
            os.system("taskkill /f /im chrome.exe")

        elif "open youtube" in query:
            speak("What do you want to watch on YouTube?")
            search_query = takecommand().lower()
            if search_query != "none":  # Check if takecommand returned a valid response
                speak(f"Playing {search_query} on YouTube.")
                kit.playonyt(search_query)
                messages_to_display.append(f"Playing {search_query} on YouTube.")
            else:
                speak("I didn't catch that. Please try again.")
        elif "close youtube" in query:  # for closing
            os.system("taskkill /f /im chrome.exe")

        elif "open twitter" in query:
            webbrowser.open("https://www.twitter.com")
            messages_to_display.append("Opened Twitter.")
        elif "close twitter" in query:  # for closing
            os.system("taskkill /f /im chrome.exe")

        elif "open linkedin" in query:
            webbrowser.open("https://www.linkedin.com")
            messages_to_display.append("Opened LinkedIn.")
        elif "close linkedin" in query:  # for closing
            os.system("taskkill /f /im chrome.exe")

        elif "open google" in query:
            speak("What should I search on google")
            cm = takecommand().lower()
            webbrowser.open(f"{cm}")
            messages_to_display.append(f"Searched Google for: {cm}")
        elif "close google" in query:  # for closing
            os.system("taskkill /f /im msedge.exe")
        
        elif "send message" in query:
            send_whatsapp_message()
        
        elif "where i am" in query or "where we are" in query:  # Check for location query
            speak("Wait sir, let me check")
            try:
                # Fetch the public IP address
                ipAdd = requests.get('https://api.ipify.org').text
                print("IP Address:", ipAdd)
                
                # Construct the URL for geolocation API
                url = f'https://get.geojs.io/v1/ip/geo/{ipAdd}.json'
                geo_requests = requests.get(url)
                
                # Log the raw response to help with debugging
                print("Geo Data Response:", geo_requests.text)
                
                # Parse the JSON response
                geo_data = geo_requests.json()
                
                # Retrieve city and country with default values to avoid KeyError
                city = geo_data.get('city', 'Unknown')
                country = geo_data.get('country', 'Unknown')
                
                # Inform the user of the location
                speak(f"Sir, I am not sure, but I think we are in {city} city of {country} country.")
            except Exception as e:
                # Log the error and inform the user
                print("Error:", e)
                speak("Sorry sir, due to a network issue, I am not able to find where we are.")

        elif "take screenshot" in query or "take a screenshot" in query:
            speak("Sir, please tell me the name for this screenshot file")
            name = takecommand().lower()
            speak("Please sir, hold the screen for a few seconds, I am taking the screenshot")
            time.sleep(3)
    
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("I am done sir, the screenshot is saved in our main folder. Now I am ready for the next command.")

        elif "send email" in query:
            speak("Please type the recipient's email address and press Enter.")
            to_address = input("Enter the recipient's email address: ")

            speak("What should be the subject of the email?")
            subject = takecommand().lower()

            speak("What should I say in the message?")
            message_body = takecommand().lower()

            send_email(to_address, subject, message_body)

        elif "read book" in query:
            speak("Set my speaking speed between 100 to 200")  # Jarvis speaking speed should be controlled by user
            sp = takecommand().lower()
            engine.setProperty('rate', sp)
            book = open("C:\\Users\\Anshu\\Documents\\PDF\\I_dont_love_you.pdf", 'rb')
            pdfReader = PyPDF2.PdfReader(book)  # Use PdfReader instead of PdfFileReader
            pages = len(pdfReader.pages)
            speak(f"Total number of pages in this book: {pages}")
            
            speak("Sir, please tell me the page number I have to read.")
            while True:
                pg = takecommand()
                if pg.isdigit():
                    pg = int(pg)
                    if 0 <= pg < pages:
                        page = pdfReader.pages[pg]
                        text = page.extract_text()
                        speak(text)
                        break
                    else:
                        speak("Invalid page number. Please say a valid page number.")
                else:
                    speak("Please say a number.")

        elif "temperature" in query:
            search = "temperature in Navi Mumbai"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            temp = data.find("div", class_="BNeawe").text
            speak(f"Current {search} is {temp}")

        elif "hide all files" in query or "hide this folder" in query or "visible for everyone" in query:  # working only for this folder
            speak("Sir, please tell me if you want to hide this folder or make it visible for everyone.")
            condition = takecommand().lower()

            if "hide" in condition:
                os.system("attrib +h /s /d")  # Use the attrib command to hide all files
                speak("Sir, all the files in this folder are now hidden.")

            elif "visible" in condition:
                os.system("attrib -h /s /d")  # Use the attrib command to make all files visible
                speak("Sir, all the files in this folder are now visible to everyone.")

            elif "leave it" in condition or "leave for now" in condition:
                speak("Okay, sir.")

        elif 'how to' in query:
            speak('How-to-do mode activated, searching your query')
            how = query
            max_results = 1
            how_to = search_wikihow(how, max_results)
            assert len(how_to) == 1  # Ensure only one result is returned
            speak(how_to[0].summary)  # Speak the result without printing it

        elif "search" in query and "on google" in query:
            # Extract the search term dynamically
            search_query = query.replace("search", "").replace("on google", "").strip()
            if search_query:
                speak(f"Searching {search_query} on Google.")
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
            else:
                speak("What should I search on Google?")
                search_query = takecommand().lower()
                if search_query and search_query != "none":
                    speak(f"Searching {search_query} on Google.")
                    webbrowser.open(f"https://www.google.com/search?q={search_query}")
                else:
                    speak("I didn't catch that. Please say it again.")

        elif "close google" in query or "close the google" in query:
            try:
                os.system("taskkill /f /im chrome.exe")
                speak("Google Chrome has been closed.")
            except Exception as e:
                speak(f"Unable to close Google Chrome. Error: {str(e)}")

        elif "do some calculations" in query or "can you calculate" in query:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak("Say what you want to calculate, example: 3 plus 3")
                print("listening....")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            my_string = r.recognize_google(audio)
            print(my_string)

            def get_operator_fn(op):
                return {
                    '+': operator.add,  # plus
                    '-': operator.sub,  # minus
                    'x': operator.mul,  # multiplied by
                    'divided': operator.truediv,  # divided
                }[op]

            def eval_binary_expr(op1, oper, op2):  # e.g., 5 plus 8
                op1, op2 = int(op1), int(op2)
                return get_operator_fn(oper)(op1, op2)

            speak("Your result is")
            speak(eval_binary_expr(*my_string.split()))

        elif "how much power left" in query or "how much power we have" in query or "battery" in query:
            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak(f"Sir, our system has {percentage} percent battery")

        elif "create folder" in query or "make a folder" in query:
            create_folder()

        elif "lock folder" in query:
            lock_folder()

        elif "remove password" in query:
            unlock_folder()

        elif "list files" in query or "list all files" in query:
            list_files_by_extension()

        elif "good bye" in query:
            speak("thanks for using me sir, have a good day")
            global assistant_running
            assistant_running = False  # Stop the GUI loop
            break  # Exit the `TaskExecution` loop
          #  sys.exit()
           # pygame.quit() 
            

# Function to draw the arc reactor
def draw_arc_reactor(center_x, center_y, radius, glow_radius, angle_offset):
    pygame.draw.circle(screen, LIGHT_BLUE, (center_x, center_y), glow_radius, width=2)
    pygame.draw.circle(screen, BLUE, (center_x, center_y), radius)

    for i in range(6):
        angle = math.radians(i * 60 + angle_offset)
        inner_x = center_x + radius * 0.5 * math.cos(angle)
        inner_y = center_y + radius * 0.5 * math.sin(angle)
        outer_x = center_x + radius * math.cos(angle)
        outer_y = center_y + radius * math.sin(angle)
        pygame.draw.line(screen, WHITE, (inner_x, inner_y), (outer_x, outer_y), 2)

    pygame.draw.circle(screen, WHITE, (center_x, center_y), radius // 3)

# Function to display messages on screen
def display_messages():
    y_offset = 20
    for message in messages_to_display[-5:]:  # Show only the last 5 messages
        text_surface = pygame.font.Font(None, 24).render(message, True, WHITE)
        screen.blit(text_surface, (10, y_offset))
        y_offset += 30

# Main GUI loop
'''def gui():
    global assistant_running
    angle_offset = 0
    glow_radius = 100
    grow = True

    # Start the voice assistant logic in a separate thread
    Thread(target=TaskExecution, daemon=True).start()

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                assistant_running = False
                pygame.quit()
                sys.exit()

        if grow:
            glow_radius += 1
            if glow_radius >= 120:
                grow = False
        else:
            glow_radius -= 1
            if glow_radius <= 100:
                grow = True

        angle_offset += 2
        draw_arc_reactor(WIDTH // 2, HEIGHT // 2, 50, glow_radius, angle_offset)
        display_messages()
        pygame.display.flip()
        clock.tick(80)
 '''
def gui():
    global assistant_running
    angle_offset = 0
    glow_radius = 100
    grow = True

    # Start the voice assistant logic in a separate thread
    Thread(target=TaskExecution, daemon=True).start()

    while assistant_running:  # Loop runs as long as assistant is active
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                assistant_running = False  # Stop the loop if the user closes the window
                pygame.quit()
                sys.exit()

        # Glow effect for Arc Reactor
        if grow:
            glow_radius += 1
            if glow_radius >= 120:
                grow = False
        else:
            glow_radius -= 1
            if glow_radius <= 100:
                grow = True

        # Draw the Arc Reactor and display messages
        angle_offset += 2
        draw_arc_reactor(WIDTH // 2, HEIGHT // 2, 50, glow_radius, angle_offset)
        display_messages()

        pygame.display.flip()
        clock.tick(80)

    pygame.quit()  # Ensure the Pygame window closes
    sys.exit()  # Exit the program
       

if __name__ == "__main__":
    gui()