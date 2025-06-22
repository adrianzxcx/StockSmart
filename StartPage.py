import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
import threading
import time

# Set appearance mode and theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Create the main window
app = ctk.CTk()
app.geometry("1200x800")
app.resizable(False, False)
app.title("Start Page")

# Make columns equally divide space
for col in (0, 1):
    app.grid_columnconfigure(col, weight=1, uniform="half")
app.grid_rowconfigure(0, weight=1)

# Left Frame
left_frame = ctk.CTkFrame(app, fg_color="#f9f5eb", corner_radius=0)
left_frame.grid(row=0, column=0, sticky="nsew")

# Right Frame
right_frame = ctk.CTkFrame(app, fg_color="#8094c2", corner_radius=0)
right_frame.grid(row=0, column=1, sticky="nsew")

# Content Frame inside Right Frame
right_inner_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
right_inner_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=(30, 0))

# Load and place the logo image
image_path = r"LOGO.png"  # Uploaded image
light_image = Image.open(image_path)
my_image = CTkImage(light_image=light_image, size=(200, 200))

image_label = ctk.CTkLabel(right_inner_frame, image=my_image, text="")
image_label.grid(row=0, column=0, pady=(15, 0), padx=(50, 0), sticky="ew")

# Title label
title_label = ctk.CTkLabel(
    right_inner_frame,
    text="Welcome to\nStockSmart!",
    font=ctk.CTkFont(family="Instrument Sans", size=60, weight="bold"),
    text_color="#0f1e46",
    justify="center"
)
title_label.grid(row=1, column=0, pady=(0, 15), padx=(50, 0), sticky="ew")

# Subtitle
sub_label = ctk.CTkLabel(
    right_inner_frame,
    text="Please select your role to enter the system",
    font=ctk.CTkFont(family="Instrument Sans", size=20),
    text_color="black"
)
sub_label.grid(row=2, column=0, pady=(10, 20), padx=(50, 0), sticky="ew")

# Admin Button
admin_button = ctk.CTkButton(
    right_inner_frame,
    text="Admin",
    width=280,
    height=60,
    corner_radius=10,
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
    fg_color="white",
    text_color="black",
    hover_color="#f0f0f0"
)
admin_button.grid(row=3, column=0, pady=(15, 15), padx=(140, 100), sticky="ew")

# Employee Button
employee_button = ctk.CTkButton(
    right_inner_frame,
    text="Employee",
    width=280,
    height=60,
    corner_radius=10,
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
    fg_color="white",
    text_color="black",
    hover_color="#f0f0f0"
)
employee_button.grid(row=4, column=0, pady=(15, 20), padx=(140, 100), sticky="ew")

# ----------- Animations -----------

def animate_entrance():
    """Entrance animation for all widgets"""
    def run_animation():
        widgets = [image_label, title_label, sub_label, admin_button, employee_button]

        for widget in widgets:
            widget.grid_remove()

        for widget in widgets:
            time.sleep(0.15)
            app.after(0, widget.grid)

    threading.Thread(target=run_animation, daemon=True).start()

def animate_hover(widget, hovered):
    """Hover animation for buttons"""
    if hovered:
        widget.configure(fg_color="#e6e6e6")
    else:
        widget.configure(fg_color="white")

# Bind hover events
admin_button.bind("<Enter>", lambda e: animate_hover(admin_button, True))
admin_button.bind("<Leave>", lambda e: animate_hover(admin_button, False))

employee_button.bind("<Enter>", lambda e: animate_hover(employee_button, True))
employee_button.bind("<Leave>", lambda e: animate_hover(employee_button, False))

# Start entrance animation
animate_entrance()

# Run the app
app.mainloop()
