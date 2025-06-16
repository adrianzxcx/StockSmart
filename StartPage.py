import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage

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
right_inner_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=0)
right_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_rowconfigure(0, weight=1)
right_inner_frame.grid_columnconfigure(0, weight=1)

# Load and place the logo image
image_path = r"LOGO.png"  # Uploaded image
light_image = Image.open(image_path)
my_image = CTkImage(light_image=light_image, size=(120, 120))  # Reduced size for smaller window

image_label = ctk.CTkLabel(right_inner_frame, image=my_image, text="")
image_label.grid(row=0, column=0, pady=(15, 0), padx=(15,0), sticky="")

# Title label
title_label = ctk.CTkLabel(
    right_inner_frame, 
    text="Welcome to\nStockSmart!", 
    font=ctk.CTkFont(family="Instrument Sans", size=42, weight="bold"), 
    text_color="#0f1e46", 
    justify="center"
)
title_label.grid(row=1, column=0, pady=(10, 15), padx=25, sticky="")

# Subtitle
sub_label = ctk.CTkLabel(
    right_inner_frame, 
    text="Please select your role to enter the system", 
    font=ctk.CTkFont(family="Instrument Sans", size=15), 
    text_color="black",
    wraplength=300  # Wrap text for better fit
)
sub_label.grid(row=2, column=0, pady=(10, 20), padx=15)

# Admin Button
admin_button = ctk.CTkButton(
    right_inner_frame, 
    text="Admin", 
    width=280, 
    height=55, 
    corner_radius=10, 
    font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold"), 
    fg_color="white", 
    text_color="black",
    hover_color="#f0f0f0"
)
admin_button.grid(row=3, column=0, pady=(15, 15), padx=15)

# Employee Button
employee_button = ctk.CTkButton(
    right_inner_frame, 
    text="Employee", 
    width=280, 
    height=55, 
    corner_radius=10, 
    font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold"), 
    fg_color="white", 
    text_color="black",
    hover_color="#f0f0f0"
)
employee_button.grid(row=4, column=0, pady=(15, 20), padx=15)

# Run the app
app.mainloop()