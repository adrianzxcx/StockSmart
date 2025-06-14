import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage

# Set appearance mode and theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Create the main window
app = ctk.CTk()
app.geometry(f"{app.winfo_screenwidth()}x{app.winfo_screenheight()}")
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
right_inner_frame.grid(row=0, column=0, sticky="nsew")
right_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_rowconfigure(0, weight=1)
right_inner_frame.grid_columnconfigure(0, weight=1)

# Load and place the logo image
image_path = r"LOGO.png"  # Uploaded image
light_image = Image.open(image_path)
my_image = CTkImage(light_image=light_image, size=(300, 300))  # Resize as needed

image_label = ctk.CTkLabel(right_inner_frame, image=my_image, text="")
image_label.grid(row=0, column=0, pady=(0, 0), padx=(20,0))

# Title label
title_label = ctk.CTkLabel(right_inner_frame, text="Welcome to\nStockSmart!",
font=ctk.CTkFont(size=102, weight="bold"), text_color="#0f1e46", justify="center")
title_label.grid(row=1, column=0, pady=(0,25),padx=(20,0))

# Subtitle
sub_label = ctk.CTkLabel(right_inner_frame, text="Please select your role to enter the system",
font=ctk.CTkFont(size=36), text_color="black")
sub_label.grid(row=2, column=0, pady=(20, 10), padx=(20,0))

# Admin Button
admin_button = ctk.CTkButton(right_inner_frame, text="Admin", width=400, height=90, corner_radius=20,
font=ctk.CTkFont(size=30, weight="bold"), fg_color="white", text_color="black")
admin_button.grid(row=3, column=0, pady=(30, 20), padx=(20,0))

# Employee Button
employee_button = ctk.CTkButton(right_inner_frame, text="Employee", width=400, height=90, corner_radius=20,
font=ctk.CTkFont(size=30, weight="bold"), fg_color="white", text_color="black")
employee_button.grid(row=4, column=0, pady=(20, 0), padx=(20,0))

# Run the app
app.mainloop()
