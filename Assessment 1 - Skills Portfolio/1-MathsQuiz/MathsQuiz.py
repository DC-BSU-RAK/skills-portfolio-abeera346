import tkinter as tk
from tkinter import * # To import all tkinter features to use them directly 
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import random
import os
import pygame

# Store main file paths
GIF_PATH = r"C:\Users\aisha\OneDrive\Documents\GitHub\skills-portfolio-abeera346\Assessment 1 - Skills Portfolio\1-MathsQuiz\Assets\backgrounds\welcome_bg.gif"
START_BTN_PATH = r"C:\Users\aisha\OneDrive\Documents\GitHub\skills-portfolio-abeera346\Assessment 1 - Skills Portfolio\1-MathsQuiz\Assets\buttons\start.png"

# Find asset folders automatically
BG_DIR = os.path.dirname(GIF_PATH)
ASSETS_DIR = os.path.dirname(BG_DIR)
BTN_DIR = os.path.join(ASSETS_DIR, "buttons")
SND_DIR = os.path.join(ASSETS_DIR, "sounds")

# Background images for screens
STORY_GIF = os.path.join(BG_DIR, "story_bg.gif")
LOADING_GIF = os.path.join(BG_DIR, "loading_bg.gif")
DIFF_GIF = os.path.join(BG_DIR, "difficulty_bg.gif")
QUIZ_GIF = os.path.join(BG_DIR, "quiz_bg.gif")
VICTORY_GIF = os.path.join(BG_DIR, "victory_bg.gif")
FAIL_GIF = os.path.join(BG_DIR, "fail_bg.gif")
STORY_FRAME_PATH = os.path.join(ASSETS_DIR, "frames", "story_frame.png")
CODENAME_FRAME_PATH = os.path.join(ASSETS_DIR, "frames", "codename.png")

# Sound effects files
CLICK_SOUND = os.path.join(SND_DIR, "click.wav")
CORRECT_SOUND = os.path.join(SND_DIR, "correct.wav")
WRONG_SOUND = os.path.join(SND_DIR, "wrong.wav")

# Background music files
BG_MUSIC_MP3 = os.path.join(SND_DIR, "bg_music.mp3")
VICTORY_MP3 = os.path.join(SND_DIR, "victory.mp3")
FAIL_MP3 = os.path.join(SND_DIR, "fail.mp3")


# Shows background images and the gifs
class AnimatedGIF(Label):
    def __init__(self, parent, gif_path, width, height):
        super().__init__(parent)
        self.frames = []

        try:
            gif = Image.open(gif_path)
            for frame in ImageSequence.Iterator(gif):
                frame = frame.resize((width, height), Image.LANCZOS)
                self.frames.append(ImageTk.PhotoImage(frame.convert("RGBA")))
        except:
            fallback = Image.new("RGBA", (width, height), "#0a0014")
            self.frames.append(ImageTk.PhotoImage(fallback))

        self.index = 0
        self.config(image=self.frames[0])
        self.animate()

    # Makes GIF loop 
    def animate(self):
        self.index = (self.index + 1) % len(self.frames)
        self.config(image=self.frames[self.index])
        self.after(50, self.animate)


# Make window fade in
def fade_in(window, alpha=0.0):
    window.attributes("-alpha", alpha)
    if alpha < 1:
        window.after(15, fade_in, window, alpha + 0.02)


class CyberMathApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CyberMath Protocol")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#0a0014")
        self.root.attributes("-alpha", 0.0)

        # --- Window Icon ---
        self.icon_path = r"C:\Users\aisha\OneDrive\Documents\GitHub\skills-portfolio-abeera346\Assessment 1 - Skills Portfolio\1-MathsQuiz\Assets\icons\icon.png"
        try:
            icon_img = ImageTk.PhotoImage(file=self.icon_path)
            self.root.iconphoto(False, icon_img)
        except:
            pass

        # Fade in at start
        fade_in(self.root)

        # Game information storage
        self.codename = "Abeera"         # Player name goes here
        self.difficulty = "easy"
        self.score = 0
        self.total_questions = 10
        self.current_question = 0
        self.correct_answer = 0
        self.attempts = 0

        # Sound effect placeholders
        self.click_sound = None
        self.correct_sound = None
        self.wrong_sound = None

        # Music file paths
        self.bg_music_path = BG_MUSIC_MP3
        self.victory_music_path = VICTORY_MP3
        self.fail_music_path = FAIL_MP3

        # Load sound files
        self.init_sounds()

        # Start with welcome screen
        self.show_welcome()

        self.root.mainloop()

    # Prepare all game sounds
    def init_sounds(self):
        try:
            pygame.mixer.init()

            if os.path.exists(CLICK_SOUND):
                self.click_sound = pygame.mixer.Sound(CLICK_SOUND)
            if os.path.exists(CORRECT_SOUND):
                self.correct_sound = pygame.mixer.Sound(CORRECT_SOUND)
            if os.path.exists(WRONG_SOUND):
                self.wrong_sound = pygame.mixer.Sound(WRONG_SOUND)
        except:
            pass

    # Play button click sound
    def play_click(self):
        if self.click_sound:
            self.click_sound.play()

    # Play correct answer sound
    def play_correct(self):
        if self.correct_sound:
            self.correct_sound.play()

    # Play wrong answer sound
    def play_wrong(self):
        if self.wrong_sound:
            self.wrong_sound.play()

    # Play background music loop
    def play_bg_music(self):
        if os.path.exists(self.bg_music_path):
            try:
                pygame.mixer.music.load(self.bg_music_path)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
            except:
                pass

    # Stop background music
    def stop_bg_music(self):
        try:
            pygame.mixer.music.stop()
        except:
            pass

    # Play victory screen music
    def play_victory_music(self):
        if os.path.exists(self.victory_music_path):
            try:
                pygame.mixer.music.load(self.victory_music_path)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
            except:
                pass

    # Play failure screen music
    def play_fail_music(self):
        if os.path.exists(self.fail_music_path):
            try:
                pygame.mixer.music.load(self.fail_music_path)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
            except:
                pass

    # Clear current screen completely
    def clear_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

    # Show first welcome page
    def show_welcome(self):
        self.clear_screen()
        self.stop_bg_music()
        self.play_bg_music()

        bg = AnimatedGIF(self.root, GIF_PATH, 600, 600)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        try:
            btn_img_raw = Image.open(START_BTN_PATH)
            btn_img_raw = btn_img_raw.resize((180, 70), Image.LANCZOS)
            btn_normal = ImageTk.PhotoImage(btn_img_raw)
        except:
            btn_img_raw = Image.new("RGBA", (180, 70), "#FF00FF")
            btn_normal = ImageTk.PhotoImage(btn_img_raw)

        # Create glowing button effect
        glow_raw = btn_img_raw.copy().resize((210, 85), Image.LANCZOS)
        glow_bg = Image.new("RGBA", (210, 85), "#FF00FF")
        glow_bg.paste(btn_img_raw, (15, 7))
        btn_glow = ImageTk.PhotoImage(glow_bg)

        glow_label = tk.Label(self.root, image=btn_glow, bd=0, bg="#0a0014")
        glow_label.image = btn_glow

        start_btn = tk.Button(
            self.root,
            image=btn_normal,
            bd=0,
            bg="#0a0014",
            activebackground="#0a0014",
            cursor="hand2",
            command=lambda: [self.play_click(), self.show_storyline()]
        )
        start_btn.image = btn_normal
        start_btn.place(relx=0.5, rely=0.5, anchor="center")

        # Show glow on hover
        def on_enter(e):
            glow_label.place(relx=0.5, rely=0.5, anchor="center")
            start_btn.lift()

        def on_leave(e):
            glow_label.place_forget()

        start_btn.bind("<Enter>", on_enter)
        start_btn.bind("<Leave>", on_leave)

    # Show game story explanation
    def show_storyline(self):
        self.clear_screen()

        # Background moving image
        bg = AnimatedGIF(self.root, STORY_GIF, 600, 600)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        # Load story frame image
        try:
            frame_img = Image.open(STORY_FRAME_PATH)
            frame_img = frame_img.resize((480, 320), Image.LANCZOS)
            frame_img_tk = ImageTk.PhotoImage(frame_img)
        except:
            frame_img_tk = None

        frame_holder = Label(self.root, image=frame_img_tk, bg="#C974D1", bd=0)
        frame_holder.image = frame_img_tk
        frame_holder.place(relx=0.5, rely=0.5, anchor="center")

        # Text area for story
        text_frame = tk.Frame(self.root, bg="#C974D1")
        text_frame.place(relx=0.5, rely=0.42, anchor="center", width=360, height=150)

        text = (
            " The District has been seeing breaches.\n"
            "City's main firewall is being tested.\n"
            "You've been pulled in as a junior\n"
            "cyber-runner. Your job is simple:\n"
            "solve the number breaches before \n"
            "they hit the grid.\n"
        )

        story_label = Label(
            text_frame,
            text=text,
            font=("Consolas", 12),
            fg="#00FFFF",
            bg="#C974D1",
            justify="center",
            anchor="center"
        )
        story_label.pack(fill="both", expand=True, padx=15, pady=10)

        # Button area
        btn_frame = tk.Frame(self.root, bg="#C974D1")
        btn_frame.place(relx=0.5, rely=0.68, anchor="center")

        continue_btn = Button(
            btn_frame,
            text="Continue",
            font=("Consolas", 14, "bold"),
            fg="#00FFFF",
            bg="#C974D1",
            relief="flat",
            cursor="hand2",
            command=lambda: [self.play_click(), self.show_codename_screen()]
        )
        continue_btn.pack(pady=6)

        back_btn = Button(
            btn_frame,
            text="Back",
            font=("Consolas", 11),
            fg="#141313",
            bg="#C974D1",
            relief="flat",
            cursor="hand2",
            command=lambda: [self.play_click(), self.show_welcome()]
        )
        back_btn.pack()


    # Get player name input
    def show_codename_screen(self):
        self.clear_screen()

        bg = AnimatedGIF(self.root, STORY_GIF, 600, 600)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        # Load codename frame image
        try:
            frame_img = Image.open(CODENAME_FRAME_PATH)
            frame_img = frame_img.resize((500, 320), Image.LANCZOS)
            frame_img_tk = ImageTk.PhotoImage(frame_img)
        except:
            frame_img_tk = None

        # Frame image holder
        frame_holder = Label(self.root, image=frame_img_tk, bg="#000000", bd=0)
        frame_holder.image = frame_img_tk
        frame_holder.place(relx=0.5, rely=0.5, anchor="center")

        # Input area inside frame
        inner = tk.Frame(self.root, bg="#000000")
        inner.place(relx=0.5, rely=0.44, anchor="center", width=350, height=140)

        Label(
            inner, text="Enter your codename", font=("Consolas", 14, "bold"),
            fg="#00FFFF", bg="#000000"
        ).pack(pady=(8, 5))

        self.codename_var = tk.StringVar(value=self.codename)

        entry = tk.Entry(
            inner, textvariable=self.codename_var, font=("Consolas", 12),
            fg="#00FFFF", bg="#000000", insertbackground="#00FFFF",
            relief="flat", justify="center", width=16
        )
        entry.pack(pady=5)
        entry.focus_set()

        # Buttons for navigation
        btn_frame = tk.Frame(self.root, bg="#000000")
        btn_frame.place(relx=0.5, rely=0.70, anchor="center")

        def save_and_continue():
            name = self.codename_var.get().strip()
            if name:
                self.codename = name
            self.play_click()
            self.show_loading_screen()

        Button(
            btn_frame, text="Confirm", font=("Consolas", 12, "bold"),
            fg="#FF00FF", bg="#000000", relief="flat",
            cursor="hand2", command=save_and_continue, width=12
        ).pack(pady=5)

        Button(
            btn_frame, text="Back", font=("Consolas", 10),
            fg="#AAAAAA", bg="#000000", relief="flat",
            cursor="hand2",
            command=lambda: [self.play_click(), self.show_storyline()], width=10
        ).pack() 


    # Show loading animation screen
    def show_loading_screen(self):
        self.clear_screen()

        bg = AnimatedGIF(self.root, LOADING_GIF, 600, 600)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        frame = tk.Frame(self.root, bg="#05000A")
        frame.place(relx=0.5, rely=0.65, anchor="center", width=400, height=140)

        self.loading_label = Label(
            frame, text="Initializing firewall modules...",
            font=("Consolas", 12), fg="#00FFFF", bg="#05000A"
        )
        self.loading_label.pack(pady=(15, 5))

        self.progress = ttk.Progressbar(
            frame, orient="horizontal", length=260, mode="determinate"
        )
        self.progress.pack(pady=(5, 15))

        self.loading_steps = [
            "Initializing firewall modules...",
            "Decrypting user identity...",
            "Compiling security keys...",
            "Synchronizing with Neon Grid..."
        ]

        self.loading_index = 0
        self.animate_loading()

    # Cycle through loading messages
    def animate_loading(self):
        if self.loading_index < len(self.loading_steps):
            self.loading_label.config(text=self.loading_steps[self.loading_index])
            self.progress["value"] = (self.loading_index + 1) * 25
            self.loading_index += 1
            self.root.after(700, self.animate_loading)
        else:
            self.show_difficulty_screen()

    # Show difficulty selection screen
    def show_difficulty_screen(self):
        self.clear_screen()

        bg = AnimatedGIF(self.root, DIFF_GIF, 600, 600)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        Label(
            self.root, text="Select Difficulty", font=("Consolas", 22, "bold"),
            fg="#00FFFF", bg="#05000A"
        ).place(relx=0.5, rely=0.18, anchor="center")

        Button(
            self.root, text="Trainee Level", font=("Consolas", 16, "bold"),
            fg="#00FFAA", bg="#080018", relief="flat", cursor="hand2",
            command=lambda: [self.play_click(), self.start_quiz("easy")]
        ).place(relx=0.5, rely=0.40, anchor="center")

        Button(
            self.root, text="Runner Level", font=("Consolas", 16, "bold"),
            fg="#00AFFF", bg="#080018", relief="flat", cursor="hand2",
            command=lambda: [self.play_click(), self.start_quiz("moderate")]
        ).place(relx=0.5, rely=0.53, anchor="center")

        Button(
            self.root, text="Firewall Expert", font=("Consolas", 16, "bold"),
            fg="#FF00FF", bg="#080018", relief="flat", cursor="hand2",
            command=lambda: [self.play_click(), self.start_quiz("advanced")]
        ).place(relx=0.5, rely=0.66, anchor="center")

        Button(
            self.root, text="Back", font=("Consolas", 14),
            fg="#999999", bg="#05000A", relief="flat", cursor="hand2",
            command=lambda: [self.play_click(), self.show_codename_screen()]
        ).place(relx=0.08, rely=0.08, anchor="center")

    # Start the math quiz
    def start_quiz(self, difficulty):
        self.difficulty = difficulty
        self.score = 0
        self.current_question = 0
        self.next_question()

    # Create random math numbers
    def generate_numbers(self):
        if self.difficulty == "easy":
            return random.randint(1, 9), random.randint(1, 9)
        elif self.difficulty == "moderate":
            return random.randint(10, 99), random.randint(10, 99)
        else:
            return random.randint(1000, 9999), random.randint(1000, 9999)

    # Show next question screen
    def next_question(self):
        if self.current_question >= self.total_questions:
            self.show_results()
            return

        self.clear_screen()

        bg = AnimatedGIF(self.root, QUIZ_GIF, 600, 600)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        hud = tk.Frame(self.root, bg="#05000A")
        hud.place(relx=0.5, rely=0.12, anchor="center", width=520, height=70)

        Label(hud, text=f"Codename: {self.codename}", font=("Consolas", 12),
              fg="#00FFFF", bg="#05000A").place(x=15, y=10)

        Label(hud, text=f"Mode: {self.difficulty.capitalize()}", font=("Consolas", 12),
              fg="#00FFAA", bg="#05000A").place(x=15, y=35)

        Label(hud, text=f"Q {self.current_question + 1}/{self.total_questions}",
              font=("Consolas", 12), fg="#FF00FF", bg="#05000A").place(x=380, y=10)

        Label(hud, text=f"Score: {self.score}", font=("Consolas", 12),
              fg="#FFFF66", bg="#05000A").place(x=380, y=35)

        a, b = self.generate_numbers()
        op = random.choice(["+", "-"])
        if op == "-" and b > a:
            a, b = b, a

        self.correct_answer = eval(f"{a}{op}{b}")
        self.attempts = 0

        card = tk.Frame(self.root, bg="#05000A")
        card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=260)

        Label(
            card, text=f"{a}  {op}  {b}", font=("Consolas", 32, "bold"),
            fg="#FF00FF", bg="#05000A"
        ).pack(pady=(25, 10))

        self.answer_entry = tk.Entry(
            card, font=("Consolas", 22), justify="center",
            fg="#00FFFF", bg="#080018", relief="flat",
            width=10, insertbackground="#00FFFF"
        )
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus_set()   # Put cursor here

        self.feedback_label = Label(
            card, text="", font=("Consolas", 12),
            fg="#CCCCCC", bg="#05000A"
        )
        self.feedback_label.pack(pady=10)

        Button(
            card, text="Submit", font=("Consolas", 16, "bold"),
            fg="#00FFAA", bg="#080018", relief="flat", cursor="hand2",
            command=lambda: [self.play_click(), self.check_answer()]
        ).pack(pady=5)

    # Check if answer is right
    def check_answer(self):
        text = self.answer_entry.get().strip()
        if text == "":
            self.feedback_label.config(text="Enter a number to continue.")
            self.play_wrong()
            return

        try:
            ans = int(text)
        except:
            self.feedback_label.config(text="Numbers only.")
            self.play_wrong()
            return

        if ans == self.correct_answer:
            if self.attempts == 0:
                self.score += 10
                self.feedback_label.config(text="Key accepted. +10", fg="#00FFAA")
            else:
                self.score += 5
                self.feedback_label.config(text="Key accepted (2nd try). +5", fg="#00FFAA")

            self.play_correct()
            self.current_question += 1
            self.root.after(1000, self.next_question)
        else:
            self.attempts += 1
            self.play_wrong()

            if self.attempts == 1:
                self.feedback_label.config(text="Mismatch. Try again.", fg="#FF5555")
            else:
                self.feedback_label.config(text="Node compromised. Moving on.", fg="#FF5555")
                self.current_question += 1
                self.root.after(1000, self.next_question)

    # Show final results screen
    def show_results(self):
        self.clear_screen()
        self.stop_bg_music()

        if self.score >= 70:
            bg = AnimatedGIF(self.root, VICTORY_GIF, 600, 600)
            message = "FIREWALL SECURED\nSystem stable."
            color = "#00FFAA"
            self.play_victory_music()
        else:
            bg = AnimatedGIF(self.root, FAIL_GIF, 600, 600)
            message = "SECURITY BREACH RISK\nFirewall still weak."
            color = "#FF5555"
            self.play_fail_music()

        bg.place(x=0, y=0, relwidth=1, relheight=1)

        frame = Frame(self.root, bg="#05000A")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=440, height=280)

        Label(
            frame, text=f"Codename: {self.codename}", font=("Consolas", 14, "bold"),
            fg="#00FFFF", bg="#05000A"
        ).pack(pady=(20, 5))

        Label(
            frame, text=f"Score: {self.score}/100", font=("Consolas", 18, "bold"),
            fg=color, bg="#05000A"
        ).pack(pady=5)

        Label(
            frame, text=message, font=("Consolas", 12),
            fg="#CCCCCC", bg="#05000A", justify="center", wraplength=380
        ).pack(pady=10)

        Button(
            frame, text="Retry Mission", font=("Consolas", 14, "bold"),
            fg="#00FFFF", bg="#080018", relief="flat",
            cursor="hand2", command=lambda: [self.play_click(), self.show_welcome()]
        ).pack(pady=(10, 5))

        Button(
            frame, text="Exit", font=("Consolas", 12, "bold"),
            fg="#FF00FF", bg="#080018", relief="flat",
            cursor="hand2", command=lambda: [self.play_click(), self.root.destroy()]
        ).pack(pady=(0, 10))


if __name__ == "__main__":
    CyberMathApp()
