import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry(f"{app.winfo_screenwidth()}x{app.winfo_screenheight()}") #Full screen width and height
app.resizable(False, False) #Make window unresizable
app.title("Login Page")



#Make columns equally divide space
for col in (0, 1):
    app.grid_columnconfigure(col, weight=1, uniform="half")
app.grid_rowconfigure(0, weight=1)

#Left Frame
left_frame = ctk.CTkFrame(app, fg_color="#8094c2", corner_radius=0)
left_frame.grid(row=0, column=0, sticky="nsew")

#Right Frame
right_frame = ctk.CTkFrame(app, fg_color="#f9f5eb", corner_radius=0)
right_frame.grid(row=0, column=1, sticky="nsew")

#Content in Left Frame
left_inner_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
left_inner_frame.grid(row=0, column=0, padx=40, pady=60, sticky="nsew")


#Welcome
title = ctk.CTkLabel(
    left_inner_frame,
    text="Welcome back!",
    font=ctk.CTkFont(size=104, weight="bold"),
    text_color="#0B1D4B"
)
title.grid(row=1, column=0, sticky="n", pady=(100,0), padx=(80, 0))

#Subtitle
subtitle = ctk.CTkLabel(
    left_inner_frame,
    text="Please enter your details",
    font=ctk.CTkFont(size=30),
    text_color="white"
)
subtitle.grid(row=2, column=0, sticky="w", pady=(0, 30), padx=(100, 0))

#Email
ctk.CTkLabel(
    left_inner_frame,
    text="Email",
    text_color="white",
    font=ctk.CTkFont(size=20)
).grid(row=3, column=0, sticky="w", pady=(50, 0), padx=(80,0))

email_entry = ctk.CTkEntry(
    left_inner_frame,
    placeholder_text="  Enter your email",
    height=70,
    corner_radius=10,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(size=20)
)
email_entry.grid(row=4, column=0, sticky="ew", pady=(8, 35), padx=(80,0))

#Password
ctk.CTkLabel(
    left_inner_frame,
    text="Password",
    text_color="white",
    font=ctk.CTkFont(size=20)
).grid(row=5, column=0, sticky="w", padx=(80,0))

password_entry = ctk.CTkEntry(
    left_inner_frame,
    placeholder_text="  Enter your password",
    show="*",
    height=70,
    corner_radius=10,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(size=20),
    width=350
)
password_entry.grid(row=6, column=0, sticky="ew", pady=(8, 5), padx=(80,0))

# Forgot Password (Right-aligned)
forgot_password = ctk.CTkLabel(
    left_inner_frame,
    text="Forgot Password",
    text_color="white",
    font=ctk.CTkFont(size=20)
)
forgot_password.grid(row=7, column=0, sticky="e", pady=(5, 25), padx=(0,5))

# Sign In Button
signin_button = ctk.CTkButton(
    left_inner_frame,
    text="Sign In",
    fg_color="#0B1D4B",
    height=70,
    corner_radius=6,
    font=ctk.CTkFont(size=20)
)
signin_button.grid(row=8, column=0, sticky="ew", pady=(0, 20), padx=(250,200))

# Sign Up Link - Centered
signup_row = ctk.CTkFrame(left_inner_frame, fg_color="transparent")
signup_row.grid(row=9, column=0, sticky="n", pady=(0, 40))  # Just before bottom spacer


signup_label = ctk.CTkLabel(
    signup_row,
    text="Don’t have an account?",
    font=ctk.CTkFont(size=20),
    text_color="white"
)
signup_label.grid(row=0, column=0, padx=(50,0))

signup_link = ctk.CTkLabel(
    signup_row,
    text=" Sign Up here",
    font=ctk.CTkFont(size=20, weight="bold"),
    text_color="#2f2f41",
    cursor="hand2"
)
signup_link.grid(row=0, column=1,)


app.mainloop()
