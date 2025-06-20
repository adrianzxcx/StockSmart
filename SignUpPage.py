import customtkinter as ctk
from PIL import Image

# Appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# App Setup
app = ctk.CTk()
app.geometry("1200x800")
app.resizable(False, False)
app.title("Sign Up")

# Load icons
eye_open_img = ctk.CTkImage(Image.open("eye_open.png"), size=(25, 25))
eye_closed_img = ctk.CTkImage(Image.open("eye_close.png"), size=(25, 25))

show_password = False
show_confirm_password = False

# Grid config
for col in (0, 1):
    app.grid_columnconfigure(col, weight=1, uniform="half")
app.grid_rowconfigure(0, weight=1)

# Frames
left_frame = ctk.CTkFrame(app, fg_color="#8094c2", corner_radius=0)
left_frame.grid(row=0, column=0, sticky="nsew")

right_frame = ctk.CTkFrame(app, fg_color="#f9f5eb", corner_radius=0)
right_frame.grid(row=0, column=1, sticky="nsew")

left_inner_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
left_inner_frame.grid(row=0, column=0, padx=20, pady=10, sticky="n")

# Title
title = ctk.CTkLabel(
    left_inner_frame,
    text="Hi!",
    font=ctk.CTkFont(family="Instrument Sans", size=46, weight="bold"),
    text_color="#0B1D4B"
)
title.grid(row=1, column=0, sticky="w", padx=(20, 200))

# Subtitle
subtitle = ctk.CTkLabel(
    left_inner_frame,
    text="Please enter your details",
    font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold"),
    text_color="white"
)
subtitle.grid(row=2, column=0, sticky="w", pady=(0, 10), padx=(20, 0))

# First Name Label
first_name_label = ctk.CTkLabel(
    left_inner_frame,
    text="First Name",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold")
)
first_name_label.grid(row=3, column=0, sticky="w", padx=(20, 0))

# First Name Entry
first_name_entry = ctk.CTkEntry(
    left_inner_frame,
    placeholder_text="Enter your first name",
    height = 40,
    width = 280,
    corner_radius=8,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=15),
    border_width=0
)
first_name_entry.grid(row=4, column=0, sticky="ew", pady=(0, 5), padx=(20, 0))
# Last Name
ctk.CTkLabel(
    left_inner_frame,
    text="Last Name",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold")
).grid(row=5, column=0, sticky="w", padx=(20, 0))
ctk.CTkEntry(
    left_inner_frame,
    placeholder_text="  Enter your last name",
    height=40,
    corner_radius=10,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=15)
).grid(row=6, column=0, sticky="ew", pady=(0, 5), padx=(20, 0))

# Email
ctk.CTkLabel(
    left_inner_frame,
    text="Email",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold")
).grid(row=7, column=0, sticky="w", padx=(20, 0))
ctk.CTkEntry(
    left_inner_frame,
    placeholder_text="  Enter your email",
    height=40,
    corner_radius=10,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=15)
).grid(row=8, column=0, sticky="ew", pady=(0, 5), padx=(20, 0))

# Password
ctk.CTkLabel(
    left_inner_frame,
    text="Password",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold")
).grid(row=9, column=0, sticky="w", padx=(20, 0))

password_frame = ctk.CTkFrame(left_inner_frame, fg_color="transparent")
password_frame.grid(row=10, column=0, sticky="ew", padx=(20, 0), pady=(0, 5))
password_frame.grid_columnconfigure(0, weight=1)

password_entry = ctk.CTkEntry(
    password_frame,
    placeholder_text="  Enter your password",
    show="*",
    height=40,
    corner_radius=10,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=15)
)
password_entry.grid(row=0, column=0, sticky="ew")

def toggle_password():
    global show_password
    show_password = not show_password
    password_entry.configure(show="" if show_password else "*")
    eye_button.configure(image=eye_open_img if show_password else eye_closed_img)

eye_button = ctk.CTkButton(
    password_frame,
    text="",
    image=eye_closed_img,
    width=40,
    height=40,
    command=toggle_password,
    fg_color="transparent",
    hover_color="#d6d6d6"
)
eye_button.grid(row=0, column=1, padx=(5, 0))

# Confirm Password
ctk.CTkLabel(
    left_inner_frame,
    text="Confirm Password",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=15, weight="bold")
).grid(row=11, column=0, sticky="w", padx=(20, 0))

confirm_frame = ctk.CTkFrame(left_inner_frame, fg_color="transparent")
confirm_frame.grid(row=12, column=0, sticky="ew", padx=(20, 0), pady=(0, 5))
confirm_frame.grid_columnconfigure(0, weight=1)

confirm_entry = ctk.CTkEntry(
    confirm_frame,
    placeholder_text="  Confirm your password",
    show="*",
    height=40,
    corner_radius=10,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=16)
)
confirm_entry.grid(row=0, column=0, sticky="ew", padx=(0, 0))

def toggle_confirm():
    global show_confirm_password
    show_confirm_password = not show_confirm_password
    confirm_entry.configure(show="" if show_confirm_password else "*")
    confirm_button.configure(image=eye_open_img if show_confirm_password else eye_closed_img)

confirm_button = ctk.CTkButton(
    confirm_frame,
    text="",
    image=eye_closed_img,
    width=40,
    height=40,
    command=toggle_confirm,
    fg_color="transparent",
    hover_color="#d6d6d6"
)
confirm_button.grid(row=0, column=1, padx=(5, 0))

# Sign Up Button
signin_button = ctk.CTkButton(
    left_inner_frame,
    text="Sign Up",
    fg_color="#0B1D4B",
    height=40,
    corner_radius=6,
    font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold")
)
signin_button.grid(row=13, column=0, sticky="ew", pady=(10, 10), padx=(130, 120))

# Sign In Link
signup_row = ctk.CTkFrame(left_inner_frame, fg_color="transparent")
signup_row.grid(row=14, column=0, sticky="n", pady=(0, 30))

signup_label = ctk.CTkLabel(
    signup_row,
    text="Already have an account?",
    font=ctk.CTkFont(family="Instrument Sans", size=16, weight="normal"),
    text_color="white"
)
signup_label.grid(row=0, column=0, padx=(20, 0))

signup_link = ctk.CTkLabel(
    signup_row,
    text=" Sign In here",
    font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold"),
    text_color="#2f2f41",
    cursor="hand2"
)
signup_link.grid(row=0, column=1)

# Run the app
app.mainloop()
