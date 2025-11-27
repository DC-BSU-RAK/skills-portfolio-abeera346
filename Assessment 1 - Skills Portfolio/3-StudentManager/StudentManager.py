import customtkinter as ctk
from tkinter import messagebox
import pygame
import os

# Initialize pygame mixer for sound effects
pygame.mixer.init()

class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("1400x900")
        
        # Set up the theme for the application
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Store student data and current view
        self.students = {}
        self.current_view = None
        # Path to the student data file
        self.data_file = r"C:\Users\aisha\OneDrive\Documents\GitHub\skills-portfolio-abeera346\Assessment 1 - Skills Portfolio\3-StudentManager\Assets\studentMarks.txt"
        
        # Load button click sound
        self.click_sound = self.load_sound(r"C:\Users\aisha\OneDrive\Documents\GitHub\skills-portfolio-abeera346\Assessment 1 - Skills Portfolio\3-StudentManager\Assets\sounds\click.wav")
        
        # Load student data from file
        self.load_student_data()
        
        # Set up the user interface
        self.setup_ui()
        
    def load_sound(self, sound_path):
        # Try to load the sound file, return None if file not found
        try:
            if os.path.exists(sound_path):
                return pygame.mixer.Sound(sound_path)
            print(f"Sound file not found: {sound_path}")
            return None
        except Exception as e:
            print(f"Error loading sound: {e}")
            return None
    
    def play_click_sound(self):
        # Play the click sound if it's loaded
        if self.click_sound:
            try:
                self.click_sound.play()
            except:
                pass  # If sound can't play, just continue without it
    
    def load_student_data(self):
        # Read student data from the text file
        try:
            with open(self.data_file, 'r') as file:
                lines = file.readlines()
                
            # Check if file is empty
            if not lines:
                messagebox.showerror("Error", "File is empty!")
                return
                
            # First line contains total number of students
            total_students = int(lines[0].strip())
            self.students = {}
            
            # Process each student record
            for i in range(1, len(lines)):
                line = lines[i].strip()
                if line:
                    # Split the line by commas to get individual data fields
                    parts = line.split(',')
                    if len(parts) == 6:
                        student_id = parts[0].strip()
                        # Store student data in dictionary
                        self.students[student_id] = {
                            'name': parts[1].strip(),
                            'coursework1': int(parts[2].strip()),
                            'coursework2': int(parts[3].strip()),
                            'coursework3': int(parts[4].strip()),
                            'exam': int(parts[5].strip())
                        }
            
            print(f"Loaded {len(self.students)} student records")
            
        except FileNotFoundError:
            messagebox.showerror("Error", "studentMarks.txt file not found!")
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")
            self.root.quit()
    
    def calculate_student_stats(self, student_data):
        # Calculate total coursework marks (3 courseworks, each out of 20)
        total_coursework = student_data['coursework1'] + student_data['coursework2'] + student_data['coursework3']
        
        # Calculate total marks (coursework + exam out of 100)
        total_marks = total_coursework + student_data['exam']
        
        # Calculate percentage based on 160 total possible marks
        percentage = (total_marks / 160) * 100
        
        # Determine grade based on percentage
        if percentage >= 70:
            grade = 'A'
        elif percentage >= 60:
            grade = 'B'
        elif percentage >= 50:
            grade = 'C'
        elif percentage >= 40:
            grade = 'D'
        else:
            grade = 'F'
            
        return {
            'total_coursework': total_coursework,
            'total_marks': total_marks,
            'percentage': percentage,
            'grade': grade
        }
    
    def setup_ui(self):
        # Create main container frame
        main_container = ctk.CTkFrame(self.root, fg_color="#f8fafc")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create header section
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent", height=100)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Application title
        ctk.CTkLabel(
            header_frame,
            text="Student Manager",
            font=("Arial", 32, "bold"),
            text_color="#1e293b"
        ).pack(side="left", anchor="w", padx=20)
        
        # Display total student count
        stats_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        stats_frame.pack(side="right", padx=20)
        
        total_students = len(self.students)
        ctk.CTkLabel(
            stats_frame,
            text=f"Total Students: {total_students}",
            font=("Arial", 14, "bold"),
            text_color="#475569"
        ).pack(side="right", padx=10)
        
        # Create main content area
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # Set up navigation sidebar
        self.setup_sidebar(content_frame)
        
        # Create scrollable content area for student records
        self.content_area = ctk.CTkScrollableFrame(
            content_frame, 
            fg_color="transparent",
            scrollbar_button_color="#cbd5e1",
            scrollbar_button_hover_color="#94a3b8"
        )
        self.content_area.pack(side="left", fill="both", expand=True, padx=(20, 0))
        
        # Show all students by default when app starts
        self.show_all_students()
    
    def setup_sidebar(self, parent):
        # Create sidebar for navigation buttons
        sidebar = ctk.CTkFrame(parent, fg_color="#1e293b", width=300, corner_radius=15)
        sidebar.pack(side="left", fill="y", padx=(0, 20))
        sidebar.pack_propagate(False)
        
        # Sidebar title
        ctk.CTkLabel(
            sidebar,
            text="Navigation",
            font=("Arial", 20, "bold"),
            text_color="#f1f5f9"
        ).pack(anchor="w", pady=(30, 20), padx=20)
        
        # Define the four main navigation buttons as required
        nav_buttons = [
            ("📊 View All Students", self.show_all_students),
            ("👤 Individual Student", self.show_individual_student),
            ("🏆 Highest Score", self.show_highest_score),
            ("📉 Lowest Score", self.show_lowest_score),
        ]
        
        self.nav_buttons = {}
        
        # Create each navigation button
        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                font=("Arial", 14),
                fg_color="transparent",
                hover_color="#334155",
                text_color="#f1f5f9",
                anchor="w",
                height=50,
                corner_radius=10,
                command=lambda cmd=command: self.navigate_to(cmd)
            )
            btn.pack(fill="x", padx=15, pady=5)
            self.nav_buttons[text] = btn
        
        # Exit button at bottom of sidebar
        ctk.CTkButton(
            sidebar,
            text="🚪 Exit Application",
            font=("Arial", 14, "bold"),
            fg_color="#dc2626",
            hover_color="#b91c1c",
            text_color="#ffffff",
            anchor="w",
            height=50,
            corner_radius=10,
            command=self.exit_application
        ).pack(side="bottom", fill="x", padx=15, pady=20)
    
    def navigate_to(self, command):
        # Play click sound and execute the button's command
        self.play_click_sound()
        command()
    
    def clear_content(self):
        # Remove all widgets from the content area
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def show_all_students(self):
        # Display all student records in a list
        self.clear_content()
        self.highlight_nav_button("📊 View All Students")
        
        # Page title
        ctk.CTkLabel(
            self.content_area,
            text="All Student Records",
            font=("Arial", 28, "bold"),
            text_color="#1e293b"
        ).pack(anchor="w", pady=(0, 20))
        
        # Check if there are any students to display
        if not self.students:
            ctk.CTkLabel(
                self.content_area,
                text="No student records found.",
                font=("Arial", 16),
                text_color="#64748b"
            ).pack(anchor="w", pady=20)
            return
        
        # Calculate class average percentage
        total_percentage = 0
        for student_data in self.students.values():
            stats = self.calculate_student_stats(student_data)
            total_percentage += stats['percentage']
        class_average = total_percentage / len(self.students)
        
        # Display class summary
        summary_frame = ctk.CTkFrame(self.content_area, fg_color="#e0f2fe", corner_radius=10)
        summary_frame.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(
            summary_frame,
            text=f"Class Summary: {len(self.students)} students • Average: {class_average:.1f}%",
            font=("Arial", 16, "bold"),
            text_color="#0369a1"
        ).pack(padx=20, pady=15)
        
        # Create a card for each student
        for student_id, student_data in self.students.items():
            self.create_student_card(student_id, student_data)
    
    def create_student_card(self, student_id, student_data):
        # Calculate student statistics
        stats = self.calculate_student_stats(student_data)
        
        # Create a card to display student information
        card = ctk.CTkFrame(self.content_area, fg_color="#ffffff", corner_radius=15, border_width=2, border_color="#e2e8f0")
        card.pack(fill="x", pady=8)
        
        # Card content area
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)
        
        # Left side - Student name and ID
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            left_frame,
            text=student_data['name'],
            font=("Arial", 18, "bold"),
            text_color="#1e293b"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            left_frame,
            text=f"ID: {student_id}",
            font=("Arial", 14),
            text_color="#64748b"
        ).pack(anchor="w", pady=(5, 0))
        
        # Right side - Grade and percentage
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.pack(side="right")
        
        # Color code for each grade
        grade_color = {
            'A': '#10b981', 'B': '#3b82f6', 'C': '#f59e0b', 
            'D': '#f97316', 'F': '#ef4444'
        }[stats['grade']]
        
        # Create grade badge with color
        grade_badge = ctk.CTkFrame(right_frame, fg_color=grade_color, corner_radius=20)
        grade_badge.pack(side="left", padx=(10, 0))
        
        ctk.CTkLabel(
            grade_badge,
            text=f"Grade {stats['grade']}",
            font=("Arial", 14, "bold"),
            text_color="#ffffff"
        ).pack(padx=15, pady=5)
        
        # Display percentage
        ctk.CTkLabel(
            right_frame,
            text=f"{stats['percentage']:.1f}%",
            font=("Arial", 16, "bold"),
            text_color=grade_color
        ).pack(side="left", padx=(15, 0))
        
        # Detailed marks information
        details_frame = ctk.CTkFrame(card, fg_color="#f8fafc", corner_radius=10)
        details_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        details_text = (
            f"Coursework: {student_data['coursework1']}, {student_data['coursework2']}, {student_data['coursework3']} "
            f"(Total: {stats['total_coursework']}/60) • "
            f"Exam: {student_data['exam']}/100 • "
            f"Overall: {stats['total_marks']}/160"
        )
        
        ctk.CTkLabel(
            details_frame,
            text=details_text,
            font=("Arial", 12),
            text_color="#475569"
        ).pack(padx=15, pady=10)
    
    def show_individual_student(self):
        # Allow user to select and view individual student
        self.clear_content()
        self.highlight_nav_button("👤 Individual Student")
        
        ctk.CTkLabel(
            self.content_area,
            text="Individual Student Record",
            font=("Arial", 28, "bold"),
            text_color="#1e293b"
        ).pack(anchor="w", pady=(0, 30))
        
        # Check if students exist
        if not self.students:
            ctk.CTkLabel(
                self.content_area,
                text="No student records available.",
                font=("Arial", 16),
                text_color="#64748b"
            ).pack(anchor="w")
            return
        
        # Student selection area
        selection_frame = ctk.CTkFrame(self.content_area, fg_color="#f1f5f9", corner_radius=15)
        selection_frame.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(
            selection_frame,
            text="Select Student:",
            font=("Arial", 18, "bold"),
            text_color="#1e293b"
        ).pack(anchor="w", padx=20, pady=15)
        
        # Create dropdown list of students
        student_list = [f"{data['name']} ({sid})" for sid, data in self.students.items()]
        
        selected_student = ctk.StringVar(value=student_list[0] if student_list else "")
        
        student_dropdown = ctk.CTkComboBox(
            selection_frame,
            values=student_list,
            variable=selected_student,
            font=("Arial", 14),
            width=400,
            height=45,
            corner_radius=10
        )
        student_dropdown.pack(anchor="w", padx=20, pady=(0, 20))
        
        # Area to display selected student
        self.individual_display_area = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.individual_display_area.pack(fill="both", expand=True)
        
        def show_selected_student():
            # Extract student ID from selection and display their record
            selection = selected_student.get()
            student_id = selection.split('(')[-1].rstrip(')')
            if student_id in self.students:
                self.display_individual_student(student_id)
        
        # Button to view selected student
        ctk.CTkButton(
            selection_frame,
            text="View Student Record",
            font=("Arial", 14, "bold"),
            fg_color="#6366f1",
            hover_color="#4f46e5",
            height=45,
            corner_radius=10,
            command=show_selected_student
        ).pack(anchor="w", padx=20, pady=(0, 20))
        
        # Show first student by default
        if student_list:
            show_selected_student()
    
    def display_individual_student(self, student_id):
        # Clear previous student display
        for widget in self.individual_display_area.winfo_children():
            widget.destroy()
        
        # Get student data and calculate stats
        student_data = self.students[student_id]
        stats = self.calculate_student_stats(student_data)
        
        # Create main display card
        card = ctk.CTkFrame(self.individual_display_area, fg_color="#ffffff", corner_radius=15, border_width=2, border_color="#e2e8f0")
        card.pack(fill="both", expand=True)
        
        # Header section with student name and ID
        header_frame = ctk.CTkFrame(card, fg_color="#f8fafc", corner_radius=15)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        # Color for grade display
        grade_color = {
            'A': '#10b981', 'B': '#3b82f6', 'C': '#f59e0b', 
            'D': '#f97316', 'F': '#ef4444'
        }[stats['grade']]
        
        # Display student name and ID
        ctk.CTkLabel(
            header_frame,
            text=student_data['name'],
            font=("Arial", 24, "bold"),
            text_color="#1e293b"
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        ctk.CTkLabel(
            header_frame,
            text=f"Student ID: {student_id}",
            font=("Arial", 16),
            text_color="#64748b"
        ).pack(anchor="w", padx=20, pady=(0, 20))
        
        # Statistics grid
        stats_frame = ctk.CTkFrame(card, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        stats_data = [
            ("Overall Percentage", f"{stats['percentage']:.1f}%", grade_color),
            ("Final Grade", stats['grade'], grade_color),
            ("Total Coursework", f"{stats['total_coursework']}/60", "#3b82f6"),
            ("Exam Mark", f"{student_data['exam']}/100", "#8b5cf6"),
            ("Total Marks", f"{stats['total_marks']}/160", "#06b6d4"),
        ]
        
        # Create statistic cards in a grid
        for i, (label, value, color) in enumerate(stats_data):
            row = i // 3
            col = i % 3
            
            stat_card = ctk.CTkFrame(stats_frame, fg_color="#f8fafc", corner_radius=10, height=120)
            stat_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            stats_frame.grid_columnconfigure(col, weight=1)
            stat_card.grid_propagate(False)
            
            ctk.CTkLabel(
                stat_card,
                text=label,
                font=("Arial", 14),
                text_color="#64748b"
            ).pack(pady=(20, 5))
            
            ctk.CTkLabel(
                stat_card,
                text=value,
                font=("Arial", 20, "bold"),
                text_color=color
            ).pack(pady=5)
        
        # Coursework breakdown section
        ctk.CTkLabel(
            card,
            text="Coursework Breakdown",
            font=("Arial", 18, "bold"),
            text_color="#1e293b"
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        coursework_frame = ctk.CTkFrame(card, fg_color="transparent")
        coursework_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Display individual coursework marks
        coursework_data = [
            ("Coursework 1", student_data['coursework1'], 20),
            ("Coursework 2", student_data['coursework2'], 20),
            ("Coursework 3", student_data['coursework3'], 20),
        ]
        
        for i, (label, score, max_score) in enumerate(coursework_data):
            course_card = ctk.CTkFrame(coursework_frame, fg_color="#f8fafc", corner_radius=10, height=80)
            course_card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            coursework_frame.grid_columnconfigure(i, weight=1)
            course_card.grid_propagate(False)
            
            ctk.CTkLabel(
                course_card,
                text=label,
                font=("Arial", 14, "bold"),
                text_color="#475569"
            ).pack(pady=(15, 5))
            
            ctk.CTkLabel(
                course_card,
                text=f"{score}/{max_score}",
                font=("Arial", 16),
                text_color="#1e293b"
            ).pack(pady=5)
    
    def show_highest_score(self):
        # Find and display student with highest overall percentage
        self.clear_content()
        self.highlight_nav_button("🏆 Highest Score")
        
        ctk.CTkLabel(
            self.content_area,
            text="Highest Scoring Student",
            font=("Arial", 28, "bold"),
            text_color="#1e293b"
        ).pack(anchor="w", pady=(0, 30))
        
        # Check if students exist
        if not self.students:
            ctk.CTkLabel(
                self.content_area,
                text="No student records available.",
                font=("Arial", 16),
                text_color="#64748b"
            ).pack(anchor="w")
            return
        
        # Find student with highest percentage
        highest_percentage = -1
        best_student_id = None
        
        for student_id, student_data in self.students.items():
            stats = self.calculate_student_stats(student_data)
            if stats['percentage'] > highest_percentage:
                highest_percentage = stats['percentage']
                best_student_id = student_id
        
        # Display top performer with celebration styling
        if best_student_id:
            celebration_frame = ctk.CTkFrame(self.content_area, fg_color="#fef3c7", corner_radius=15)
            celebration_frame.pack(fill="x", pady=(0, 30))
            
            ctk.CTkLabel(
                celebration_frame,
                text="🎉 TOP PERFORMER 🎉",
                font=("Arial", 24, "bold"),
                text_color="#d97706"
            ).pack(pady=20)
            
            self.display_individual_student_highlight(best_student_id, "highest")
    
    def show_lowest_score(self):
        # Find and display student with lowest overall percentage
        self.clear_content()
        self.highlight_nav_button("📉 Lowest Score")
        
        ctk.CTkLabel(
            self.content_area,
            text="Student Needing Support",
            font=("Arial", 28, "bold"),
            text_color="#1e293b"
        ).pack(anchor="w", pady=(0, 30))
        
        # Check if students exist
        if not self.students:
            ctk.CTkLabel(
                self.content_area,
                text="No student records available.",
                font=("Arial", 16),
                text_color="#64748b"
            ).pack(anchor="w")
            return
        
        # Find student with lowest percentage
        lowest_percentage = 101
        worst_student_id = None
        
        for student_id, student_data in self.students.items():
            stats = self.calculate_student_stats(student_data)
            if stats['percentage'] < lowest_percentage:
                lowest_percentage = stats['percentage']
                worst_student_id = student_id
        
        # Display student needing support with appropriate styling
        if worst_student_id:
            support_frame = ctk.CTkFrame(self.content_area, fg_color="#fee2e2", corner_radius=15)
            support_frame.pack(fill="x", pady=(0, 30))
            
            ctk.CTkLabel(
                support_frame,
                text=" NEEDS ADDITIONAL SUPPORT ",
                font=("Arial", 24, "bold"),
                text_color="#dc2626"
            ).pack(pady=20)
            
            self.display_individual_student_highlight(worst_student_id, "lowest")
    
    def display_individual_student_highlight(self, student_id, highlight_type):
        # Display student with special highlighting for highest/lowest
        student_data = self.students[student_id]
        stats = self.calculate_student_stats(student_data)
        
        # Choose background color based on highlight type
        if highlight_type == "highest":
            card_bg = "#f0fdf4"  # Light green for top performer
            border_color = "#22c55e"
        else:
            card_bg = "#fef2f2"  # Light red for student needing support
            border_color = "#ef4444"
        
        # Create highlighted card
        card = ctk.CTkFrame(self.content_area, fg_color=card_bg, corner_radius=15, border_width=3, border_color=border_color)
        card.pack(fill="both", expand=True)
        
        # Content area
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Student name and ID
        ctk.CTkLabel(
            content_frame,
            text=student_data['name'],
            font=("Arial", 28, "bold"),
            text_color="#1e293b"
        ).pack(anchor="w", pady=(0, 10))
        
        ctk.CTkLabel(
            content_frame,
            text=f"Student ID: {student_id}",
            font=("Arial", 18),
            text_color="#64748b"
        ).pack(anchor="w", pady=(0, 30))
        
        # Key metrics display
        metrics_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        metrics_frame.pack(fill="x", pady=(0, 30))
        
        metrics = [
            ("Overall Percentage", f"{stats['percentage']:.1f}%", "#1e293b"),
            ("Final Grade", stats['grade'], "#1e293b"),
            ("Total Marks", f"{stats['total_marks']}/160", "#1e293b"),
        ]
        
        # Create metric cards
        for i, (label, value, color) in enumerate(metrics):
            metric_card = ctk.CTkFrame(metrics_frame, fg_color="#ffffff", corner_radius=10, height=120)
            metric_card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            metrics_frame.grid_columnconfigure(i, weight=1)
            metric_card.grid_propagate(False)
            
            ctk.CTkLabel(
                metric_card,
                text=label,
                font=("Arial", 16),
                text_color="#64748b"
            ).pack(pady=(25, 10))
            
            ctk.CTkLabel(
                metric_card,
                text=value,
                font=("Arial", 24, "bold"),
                text_color=color
            ).pack(pady=10)
    
    def highlight_nav_button(self, button_text):
        # Highlight the currently active navigation button
        for text, button in self.nav_buttons.items():
            if text == button_text:
                button.configure(fg_color="#334155")  # Active button color
            else:
                button.configure(fg_color="transparent")  # Inactive button color
    
    def exit_application(self):
        # Confirm and exit the application
        self.play_click_sound()
        if messagebox.askyesno("Exit", "Are you sure you want to exit the application?"):
            self.root.quit()

def main():
    # Create the main window and start the application
    root = ctk.CTk()
    app = StudentManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()