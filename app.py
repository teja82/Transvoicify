import tkinter as tk
from tkinter import messagebox
import os
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import pygame

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Supported languages for translation and speech
LANGUAGES = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Hindi": "hi",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Telugu": "te",
    "Bengali": "bn",
    "Tamil": "ta"
}

# Function to translate text
def translate_text():
    text = text_box.get(1.0, tk.END).strip()
    if text:
        target_lang = LANGUAGES[language_var.get()]
        translated_text = GoogleTranslator(source="auto", target=target_lang).translate(text)
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, translated_text)
        messagebox.showinfo("Translation", f"Text translated to {language_var.get()} ✅")
    else:
        messagebox.showwarning("Warning", "Please enter some text to translate! ⚠")

# Function to convert text to speech
def text_to_speech():
    text = text_box.get(1.0, tk.END).strip()
    if text:
        target_lang = LANGUAGES[language_var.get()]
        status_label.config(text="Speaking... 🎙")
        
        # Convert text to speech using gTTS
        tts = gTTS(text, lang=target_lang)
        
        # Save the audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            audio_path = temp_audio.name
            tts.save(audio_path)
        
        # Play the generated speech
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        
        # Wait until the audio finishes playing
        while pygame.mixer.music.get_busy():
            continue
        
        # Delete the temporary file after playing
        os.remove(audio_path)
        
        status_label.config(text="Done ✅")
    else:
        messagebox.showwarning("Warning", "Please enter some text to convert! ⚠")

# Create main window
root = tk.Tk()
root.title("Text to Speech Converter 📝🎧")
root.geometry("700x500")
root.configure(bg="lavender")

# Header label
header_label = tk.Label(root, text="Text to Speech Converter", font=("Arial", 16, "bold"), bg="lavender")
header_label.pack(pady=10)

# Text Box to input text
text_box = tk.Text(root, height=10, width=50, wrap="word", font=("Arial", 12))
text_box.pack(pady=10)

# Dropdown to select language
language_var = tk.StringVar(root)
language_var.set("English")  # Default language

language_menu = tk.OptionMenu(root, language_var, *LANGUAGES.keys())
language_menu.config(font=("Arial", 12), bg="#D3D3D3")
language_menu.pack(pady=5)

# Buttons to translate and speak
translate_button = tk.Button(root, text="Translate 🌍", command=translate_text, font=("Arial", 12), bg="#FFA500", fg="white", padx=10, pady=5)
translate_button.pack(pady=5)

speak_button = tk.Button(root, text="Convert to Speech 🎤", command=text_to_speech, font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
speak_button.pack(pady=5)

# Status label
status_label = tk.Label(root, text="", font=("Arial", 12), bg="lavender")
status_label.pack(pady=5)

# Run the application
root.mainloop()
