import tkinter as tk
from tkinter import *
import random
import os
import pygame
import threading 
from PIL import Image, ImageTk, ImageSequence

# Define color scheme for the application interface
BG_COLOR = "#d9d9d9"
ACCENT = "#5ce1e6"
BTN_COLOR = "#2F3C4F"
BTN_HOVER = "#41546A"

# Set up file paths for all assets used in the application
SCRIPT_DIR = os.path.dirname(__file__)
BG_GIF = os.path.join(SCRIPT_DIR, "Assets", "backgrounds", "welcome_bg.gif")
MAIN_BG_GIF = os.path.join(SCRIPT_DIR, "Assets", "backgrounds", "main_bg.gif")
ACTIVATE_BTN_IMG = os.path.join(SCRIPT_DIR, "Assets", "buttons", "activate.png")
DRUMROLL_SOUND = os.path.join(SCRIPT_DIR, "Assets", "sounds", "drumroll.wav")
BG_MUSIC = os.path.join(SCRIPT_DIR, "Assets", "sounds", "bg_music.mp3")
CLICK_SOUND = os.path.join(SCRIPT_DIR, "Assets", "sounds", "click.wav")
PUNCHLINE_FRAME_IMG = os.path.join(SCRIPT_DIR, "Assets", "backgrounds", "punchline_frame.png")

# Paths for button images
TELL_JOKE_IMG = os.path.join(SCRIPT_DIR, "Assets", "buttons", "tell_joke.png")
SHOW_PUNCHLINE_IMG = os.path.join(SCRIPT_DIR, "Assets", "buttons", "show_punchline.png")
NEXT_JOKE_IMG = os.path.join(SCRIPT_DIR, "Assets", "buttons", "next_joke.png")
QUIT_IMG = os.path.join(SCRIPT_DIR, "Assets", "buttons", "quit.png")

# Function to load jokes from external text file
def load_jokes():
    jokes = []
    file_path = os.path.join(SCRIPT_DIR, "Assets", "randomJokes.txt")

    # Provide default joke if file doesn't exist
    if not os.path.exists(file_path):
        return [("Why did the chicken cross the road?", "To get to the other side.")]

    # Parse joke file and split into setup and punchline
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if "?" in line:
                setup, punchline = line.strip().split("?", 1)
                jokes.append((setup + "?", punchline))
    return jokes

JOKES = load_jokes()

# Class to handle animated GIF display
class AnimatedGIF(Label):
    def __init__(self, parent, gif_path, width, height):
        super().__init__(parent)
        self.frames = []

        # Load and process GIF frames
        if os.path.exists(gif_path):
            gif = Image.open(gif_path)
            for frame in ImageSequence.Iterator(gif):
                frame = frame.resize((width, height))
                self.frames.append(ImageTk.PhotoImage(frame))
        else:
            # Create placeholder if GIF not found
            img = Image.new("RGB", (width, height), BG_COLOR)
            self.frames.append(ImageTk.PhotoImage(img))

        self.index = 0
        self.config(image=self.frames[0])
        self.animate()

    def animate(self):
        # Cycle through frames to create animation
        if len(self.frames) > 1:
            self.index = (self.index + 1) % len(self.frames)
            self.config(image=self.frames[self.index])
        self.after(70, self.animate)

# Text-to-Speech management class
class SimpleTTS:
    def __init__(self):
        self.is_speaking = False
        self.stop_speaking = False
        self.current_thread = None
    
    def speak(self, text):
        # Stop any ongoing speech before starting new one
        if self.is_speaking:
            self.stop()
            
        self.stop_speaking = False
        self.is_speaking = True
        
        def speak_thread():
            try:
                import pyttsx3
                # Initialize new TTS engine for each speech to avoid conflicts
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)
                engine.setProperty('volume', 0.8)
                
                # Prefer female voice if available
                voices = engine.getProperty('voices')
                if len(voices) > 1:
                    engine.setProperty('voice', voices[1].id)
                
                # Speak text unless interrupted
                if not self.stop_speaking:
                    engine.say(text)
                    engine.runAndWait()
                    
                engine.stop()
                
            except Exception as e:
                print(f"TTS Error: {e}")
            finally:
                self.is_speaking = False
        
        # Run TTS in separate thread to prevent UI freezing
        self.current_thread = threading.Thread(target=speak_thread)
        self.current_thread.daemon = True
        self.current_thread.start()
    
    def stop(self):
        # Flag to stop current speech operation
        self.stop_speaking = True
        self.is_speaking = False

# Main application class
class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Joke Assistant")
        self.root.geometry("700x400")
        self.root.resizable(False, False)

        # Initialize pygame for audio with suppressed welcome message
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
        pygame.mixer.init()
        
        # Set up text-to-speech functionality
        self.tts = SimpleTTS()
        self.tts_enabled = True

        self.current_setup = ""
        self.current_punchline = ""

        self.play_background_music()
        self.build_welcome_screen()

    # Text-to-speech methods
    def speak_text(self, text):
        # Convert text to speech if TTS is enabled
        if self.tts_enabled:
            self.tts.speak(text)

    def stop_speech(self):
        # Immediately stop any active speech
        self.tts.stop()

    # Typewriter animation for text display
    def typewriter_effect(self, text, label, index=0):
        # Display text character by character with calculated timing
        if index < len(text):
            current_text = text[:index+1]
            label.config(text=current_text)
            # Dynamic delay based on text length for natural pacing
            delay = max(30, 2500 // len(text))
            self.root.after(delay, lambda: self.typewriter_effect(text, label, index+1))

    # Audio management methods
    def play_click_sound(self):
        # Play button click sound effect
        if os.path.exists(CLICK_SOUND):
            try:
                click_sound = pygame.mixer.Sound(CLICK_SOUND)
                click_sound.set_volume(0.5)
                click_sound.play()
            except Exception as e:
                print("Error playing click sound:", e)

    def play_background_music(self):
        # Play continuous background music
        if os.path.exists(BG_MUSIC):
            try:
                pygame.mixer.music.load(BG_MUSIC)
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
            except Exception as e:
                print("Error playing background music:", e)

    # Welcome screen construction
    def build_welcome_screen(self):
        self.welcome_frame = Frame(self.root, bg=BG_COLOR)
        self.welcome_frame.pack(fill="both", expand=True)

        # Animated background for welcome screen
        self.bg_anim = AnimatedGIF(self.welcome_frame, BG_GIF, 700, 400)
        self.bg_anim.place(x=0, y=0)

        # Load and display activation button
        if os.path.exists(ACTIVATE_BTN_IMG):
            img = Image.open(ACTIVATE_BTN_IMG).resize((160, 55), Image.LANCZOS)
            self.activate_img = ImageTk.PhotoImage(img)
        else:
            self.activate_img = None

        # Central activation button
        self.activate_btn = Button(
            self.welcome_frame,
            image=self.activate_img,
            bg="#d9d9d9",
            bd=0,
            activebackground="#d9d9d9",
            command=self.activate_button_click
        )

        self.activate_btn.lift()
        self.activate_btn.place(relx=0.5, rely=0.5, anchor="center")

    def activate_button_click(self):
        # Transition from welcome to main screen
        self.play_click_sound()
        self.load_main_screen()

    # Button image loading and preparation
    def load_button_images(self):
        button_size = (160, 55)
        
        self.tell_joke_img = self.load_button_image(TELL_JOKE_IMG, button_size)
        self.show_punchline_img = self.load_button_image(SHOW_PUNCHLINE_IMG, button_size)
        self.next_joke_img = self.load_button_image(NEXT_JOKE_IMG, button_size)
        self.quit_img = self.load_button_image(QUIT_IMG, button_size)

    def load_button_image(self, path, size):
        # Load and resize button images with fallback
        if os.path.exists(path):
            img = Image.open(path).resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        else:
            img = Image.new("RGB", size, BTN_COLOR)
            return ImageTk.PhotoImage(img)

    # Main application screen setup
    def load_main_screen(self):
        self.welcome_frame.destroy()
        self.load_button_images()

        self.main_frame = Frame(self.root, bg=BG_COLOR)
        self.main_frame.pack(fill="both", expand=True)

        # Main screen animated background
        self.main_bg_anim = AnimatedGIF(self.main_frame, MAIN_BG_GIF, 700, 400)
        self.main_bg_anim.place(x=0, y=0)

        # Frame for joke text display
        self.joke_frame = Frame(self.main_frame, bg=BG_COLOR)
        self.joke_frame.place(relx=0.5, rely=0.25, anchor="center")

        # Label for joke setup text
        self.setup_label = Label(
            self.joke_frame,
            text="",
            font=("Poppins", 14, "bold"),
            bg=BG_COLOR,
            fg="#000000",
            wraplength=500,
            justify="center"
        )
        self.setup_label.pack(pady=10)

        # Frame for control buttons
        self.button_frame = Frame(self.main_frame, bg=BG_COLOR)
        self.button_frame.place(relx=0.5, rely=0.65, anchor="center")

        # Common button styling
        btn_style = {
            "bg": BG_COLOR,
            "bd": 0,
            "activebackground": BG_COLOR,
        }

        # Create all functional buttons
        Button(self.button_frame, image=self.tell_joke_img, command=self.tell_joke_click, **btn_style).pack(pady=3)
        Button(self.button_frame, image=self.show_punchline_img, command=self.show_punchline_click, **btn_style).pack(pady=3)
        Button(self.button_frame, image=self.next_joke_img, command=self.next_joke_click, **btn_style).pack(pady=3)
        Button(self.button_frame, image=self.quit_img, command=self.quit_click, **btn_style).pack(pady=3)

    # Button action handlers
    def tell_joke_click(self):
        self.play_click_sound()
        self.get_random_joke()

    def show_punchline_click(self):
        self.play_click_sound()
        self.show_punchline_window()

    def next_joke_click(self):
        self.play_click_sound()
        self.get_random_joke()

    def quit_click(self):
        self.play_click_sound()
        self.root.quit()

    # Joke selection and presentation logic
    def get_random_joke(self):
        # Stop any current speech before new joke
        self.stop_speech()
        
        self.setup_label.config(text="")
        self.current_setup, self.current_punchline = random.choice(JOKES)
        
        # Display joke with typewriter animation
        self.typewriter_effect(self.current_setup, self.setup_label)
        
        # Speak the joke setup
        if self.tts_enabled:
            self.speak_text(self.current_setup)

    # Punchline reveal window
    def show_punchline_window(self):
        pop = Toplevel(self.root)
        pop.geometry("500x300")
        pop.title("Punchline")
        pop.config(bg=BG_COLOR)
        
        # Load punchline frame background
        if os.path.exists(PUNCHLINE_FRAME_IMG):
            frame_img = Image.open(PUNCHLINE_FRAME_IMG)
            frame_img = frame_img.resize((500, 300), Image.LANCZOS)
            self.punchline_frame_bg = ImageTk.PhotoImage(frame_img)
            bg_label = Label(pop, image=self.punchline_frame_bg)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_bg_color = BG_COLOR
        else:
            bg_bg_color = BG_COLOR
            pop.config(bg=bg_bg_color)

        # Play drumroll sound effect
        if os.path.exists(DRUMROLL_SOUND):
            try:
                drumroll_sound = pygame.mixer.Sound(DRUMROLL_SOUND)
                drumroll_sound.play()
            except Exception as e:
                print("Error playing drumroll:", e)

        # Initial drumroll message
        label = Label(
            pop,
            text="🎵 Drumroll...",
            font=("Poppins", 16, "bold"),
            bg=bg_bg_color,
            fg=ACCENT
        )
        label.place(relx=0.5, rely=0.5, anchor="center")

        def reveal():
            # Replace drumroll with actual punchline after delay
            label.config(text=self.current_punchline, fg="#1A1A1A", font=("Poppins", 14, "bold"))
            # Speak the punchline
            if self.tts_enabled:
                self.speak_text(self.current_punchline)

        pop.after(3000, reveal)

# Application entry point
if __name__ == "__main__":
    root = Tk()
    app = JokeApp(root)
    root.mainloop()
