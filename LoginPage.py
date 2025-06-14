import customtkinter as ctk

# Appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# App Setup
app = ctk.CTk()
app.geometry("900x600")
app.resizable(False, False)  # Make window unresizable
app.title("Login Page")

# Grid Layout
for col in (0, 1):
    app.grid_columnconfigure(col, weight=1, uniform="half")
app.grid_rowconfigure(0, weight=1)

# Left Frame
left_frame = ctk.CTkFrame(app, fg_color="#8094c2", corner_radius=0)
left_frame.grid(row=0, column=0, sticky="nsew")

# Right Frame
right_frame = ctk.CTkFrame(app, fg_color="#f9f5eb", corner_radius=0)
right_frame.grid(row=0, column=1, sticky="nsew")

# Configure left frame grid
left_frame.grid_rowconfigure(0, weight=1)
left_frame.grid_columnconfigure(0, weight=1)

# Inner Content Frame (Left) - Centered vertically
left_inner_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
left_inner_frame.grid(row=0, column=0, padx=25, pady=20, sticky="")

# Configure inner frame columns
left_inner_frame.grid_columnconfigure(0, weight=1)

# Title
title = ctk.CTkLabel(
    left_inner_frame,
    text="Welcome back!",
    font=ctk.CTkFont(family="Instrument Sans", size=38, weight="bold"),
    text_color="#0B1D4B"
)
title.grid(row=0, column=0, pady=(0, 0), padx=(20,100), sticky="w")

# Subtitle
subtitle = ctk.CTkLabel(
    left_inner_frame,
    text="Please enter your details",
    font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold"),
    text_color="white"
)
subtitle.grid(row=1, column=0, pady=(0, 25), padx=(25,0), sticky="w")

# Email Label
email_label = ctk.CTkLabel(
    left_inner_frame,
    text="Email",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold")
)
email_label.grid(row=2, column=0, sticky="w", pady=(0, 4), padx=15)

# Email Entry
email_entry = ctk.CTkEntry(
    left_inner_frame,
    placeholder_text="Enter your email",
    height=40,
    width=280,
    corner_radius=8,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=15),
    border_width=0
)
email_entry.grid(row=3, column=0, sticky="ew", pady=(0, 15), padx=15)

# Password Label
password_label = ctk.CTkLabel(
    left_inner_frame,
    text="Password",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold")
)
password_label.grid(row=4, column=0, sticky="w", pady=(0, 4), padx=15)

# Password Entry
password_entry = ctk.CTkEntry(
    left_inner_frame,
    placeholder_text="Enter your password",
    show="*",
    height=40,
    width=280,
    corner_radius=8,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=15),
    border_width=0
)
password_entry.grid(row=5, column=0, sticky="ew", pady=(0, 8), padx=15)

# Forgot Password
forgot_password = ctk.CTkLabel(
    left_inner_frame,
    text="Forgot Password?",
    text_color="#2f2f41",
    font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold"),
    cursor="hand2"
)
forgot_password.grid(row=6, column=0, sticky="e", pady=(0, 20), padx=15)

# Sign In Button
signin_button = ctk.CTkButton(
    left_inner_frame,
    text="Sign In",
    fg_color="#0B1D4B",
    hover_color="#162A5C",
    height=40,
    width=280,
    corner_radius=8,
    font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold")
)
signin_button.grid(row=7, column=0, sticky="", pady=(0, 20), padx=(100,100))

# Sign Up Row
signup_row = ctk.CTkFrame(left_inner_frame, fg_color="transparent")
signup_row.grid(row=8, column=0, sticky="", pady=(0, 0))

# Configure signup row
signup_row.grid_columnconfigure((0, 1), weight=0)

# Sign Up Label
signup_label = ctk.CTkLabel(
    signup_row,
    text="Don't have an account?",
    font=ctk.CTkFont(family="Instrument Sans", size=15, weight="normal"),
    text_color="white"
)
signup_label.grid(row=0, column=0, padx=(0, 5))

# Sign Up Link
signup_link = ctk.CTkLabel(
    signup_row,
    text="Sign Up here",
    font=ctk.CTkFont(family="Instrument Sans", size=15, weight="bold"),
    text_color="#2f2f41",
    cursor="hand2"
)
signup_link.grid(row=0, column=1, padx=(0, 0))

# Start app
app.mainloop()