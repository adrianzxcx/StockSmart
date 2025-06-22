import customtkinter as ctk
from PIL import Image
import threading
import time

# Appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# App Setup
app = ctk.CTk()
app.geometry("1200x800")
app.resizable(False, False)
app.title("Sign Up")

# Animation variables
is_animating = False

# Load icons (create placeholder images if files don't exist)
try:
    eye_open_img = ctk.CTkImage(Image.open("eye_open.png"), size=(25, 25))
    eye_closed_img = ctk.CTkImage(Image.open("eye_close.png"), size=(25, 25))
except FileNotFoundError:
    # Create simple placeholder images if files don't exist
    from PIL import Image, ImageDraw
    
    # Create eye open image
    img_open = Image.new('RGBA', (25, 25), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img_open)
    draw.ellipse([5, 8, 20, 17], fill='black')
    draw.ellipse([10, 10, 15, 15], fill='white')
    eye_open_img = ctk.CTkImage(img_open, size=(25, 25))
    
    # Create eye closed image
    img_closed = Image.new('RGBA', (25, 25), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img_closed)
    draw.line([5, 12, 20, 12], fill='black', width=2)
    eye_closed_img = ctk.CTkImage(img_closed, size=(25, 25))

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
left_inner_frame.grid(row=0, column=0, padx=25, pady=10, sticky="nsew")

# Title
title = ctk.CTkLabel(
    left_inner_frame,
    text="Hi!",
    font=ctk.CTkFont(family="Instrument Sans", size=60, weight="bold"),
    text_color="#0B1D4B"
)
title.grid(row=1, column=0, sticky="w", padx=(40,400),  pady=(30,0))

# Subtitle
subtitle = ctk.CTkLabel(
    left_inner_frame,
    text="Please enter your details",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
    text_color="white"
)
subtitle.grid(row=2, column=0, sticky="w", pady=(0, 10), padx=(40, 10))

# First Name Label
first_name_label = ctk.CTkLabel(
    left_inner_frame,
    text="First Name",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
)
first_name_label.grid(row=3, column=0, padx=(40, 10), pady=(0, 4), sticky="w")

# First Name Entry with animations
first_name_entry = ctk.CTkEntry(
    left_inner_frame,
    placeholder_text="     Enter your first name",
    height=50,
    width=280,
    corner_radius=8,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=16),
    border_width=2,
    border_color="#cbd3ea"
)
first_name_entry.grid(row=4, column=0, sticky="ew", pady=(0, 15), padx=(40,10))

# Last Name Label
last_name_label = ctk.CTkLabel(
    left_inner_frame,
    text="Last Name",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
)
last_name_label.grid(row=5, column=0, sticky="w", padx=(40, 0))

# Last Name Entry with animations
last_name_entry = ctk.CTkEntry(
    left_inner_frame,
    placeholder_text="     Enter your last name",
    height=50,
    corner_radius=10,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=16),
    border_width=2,
    border_color="#cbd3ea"
)
last_name_entry.grid(row=6, column=0, sticky="ew", pady=(0, 15), padx=(40,10))

# Email Label
email_label = ctk.CTkLabel(
    left_inner_frame,
    text="Email",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
)
email_label.grid(row=7, column=0, sticky="w", padx=(40, 10))

# Email Entry with animations
email_entry = ctk.CTkEntry(
    left_inner_frame,
    placeholder_text="     Enter your email",
    height=50,
    corner_radius=10,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=16),
    border_width=2,
    border_color="#cbd3ea"
)
email_entry.grid(row=8, column=0, sticky="ew", pady=(0, 15), padx=(40, 10))

# Password Label
password_label = ctk.CTkLabel(
    left_inner_frame,
    text="Password",
    text_color="white",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
)
password_label.grid(row=9, column=0, sticky="w", padx=(40, 10))

password_frame = ctk.CTkFrame(left_inner_frame, fg_color="transparent")
password_frame.grid(row=10, column=0, sticky="ew", padx=(40, 10), pady=(0, 5))
password_frame.grid_columnconfigure(0, weight=1)

password_entry = ctk.CTkEntry(
    password_frame,
    placeholder_text="     Enter your password",
    show="*",
    height=50,
    corner_radius=10,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=15),
    border_width=2,
    border_color="#cbd3ea"
)
password_entry.grid(row=0, column=0, sticky="ew", pady=(0, 15))

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
    height=50,
    command=toggle_password,
    fg_color="transparent",
    hover_color="#d6d6d6"
)
eye_button.grid(row=0, column=1, padx=(5, 0))

# Confirm Password Label
confirm_password_label = ctk.CTkLabel(
    left_inner_frame,
    text="Confirm Password",
    text_color="#112250",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
)
confirm_password_label.grid(row=11, column=0, sticky="w", padx=(40, 10))

confirm_frame = ctk.CTkFrame(left_inner_frame, fg_color="transparent")
confirm_frame.grid(row=12, column=0, sticky="ew", padx=(40, 10), pady=(0, 5))
confirm_frame.grid_columnconfigure(0, weight=1)

confirm_entry = ctk.CTkEntry(
    confirm_frame,
    placeholder_text="     Confirm your password",
    show="*",
    height=50,
    corner_radius=10,
    fg_color="#cbd3ea",
    font=ctk.CTkFont(family="Instrument Sans", size=16),
    border_width=2,
    border_color="#cbd3ea"
)
confirm_entry.grid(row=0, column=0, sticky="ew", padx=(0, 0), pady=(0, 15))

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
    height=50,
    command=toggle_confirm,
    fg_color="transparent",
    hover_color="#d6d6d6"
)
confirm_button.grid(row=0, column=1, padx=(5, 0))

# Sign Up Button
signup_button = ctk.CTkButton(
    left_inner_frame,
    text="Sign Up",
    fg_color="#0B1D4B",
    height=50,
    corner_radius=6,
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold")
)
signup_button.grid(row=13, column=0, sticky="ew", pady=(30, 10), padx=(130, 120))

# Sign In Link
signin_row = ctk.CTkFrame(left_inner_frame, fg_color="transparent")
signin_row.grid(row=14, column=0, sticky="n", pady=(0, 30))

signin_label = ctk.CTkLabel(
    signin_row,
    text="Already have an account?",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="normal"),
    text_color="white"
)
signin_label.grid(row=0, column=0, padx=(10, 0))

signin_link = ctk.CTkLabel(
    signin_row,
    text=" Sign In here",
    font=ctk.CTkFont(family="Instrument Sans", size=20, weight="bold"),
    text_color="#2f2f41",
    cursor="hand2"
)
signin_link.grid(row=0, column=1)

# Animation Functions
def animate_entry_focus(entry, is_focused):
    """Animate entry field when focused/unfocused"""
    if is_focused:
        entry.configure(border_color="#0B1D4B", border_width=3)
        # Subtle scale effect simulation
        entry.configure(height=52)
    else:
        entry.configure(border_color="#cbd3ea", border_width=2)
        entry.configure(height=50)

def animate_hover(label, is_hovered):
    """Animate label hover effects"""
    if is_hovered:
        # Darken color on hover
        label.configure(text_color="#1a1a2e")
    else:
        # Return to original color
        label.configure(text_color="#2f2f41")

def signup_click():
    """Handle sign up button click with animation"""
    global is_animating
    if is_animating:
        return
        
    is_animating = True
    
    # Button press animation
    original_text = signup_button.cget("text")
    signup_button.configure(text="Creating account...", state="disabled")
    
    def reset_button():
        time.sleep(1.5)  # Simulate signup process
        app.after(0, lambda: signup_button.configure(text=original_text, state="normal"))
        global is_animating
        is_animating = False
        
        # Show success animation
        app.after(0, show_success_message)
    
    threading.Thread(target=reset_button, daemon=True).start()

def show_success_message():
    """Show a temporary success message"""
    success_label = ctk.CTkLabel(
        left_inner_frame,
        text="✓ Account Created Successfully!",
        font=ctk.CTkFont(family="Instrument Sans", size=18, weight="bold"),
        text_color="#2d5016"
    )
    success_label.grid(row=15, column=0, pady=(10, 0))
    
    # Remove success message after 2 seconds
    app.after(2000, success_label.destroy)

def signin_click(event):
    """Handle sign in click"""
    # Temporary feedback
    original_text = signin_link.cget("text")
    signin_link.configure(text="Opening sign in...")
    
    def reset_text():
        time.sleep(1.5)
        app.after(0, lambda: signin_link.configure(text=original_text))
    
    threading.Thread(target=reset_text, daemon=True).start()

def animate_entrance():
    """Animate the entrance of form elements"""
    def entrance_animation():
        # Start with elements invisible
        elements = [
            title, subtitle, 
            first_name_label, first_name_entry,
            last_name_label, last_name_entry,
            email_label, email_entry,
            password_label, password_frame,
            confirm_password_label, confirm_frame,
            signup_button, signin_row
        ]
        
        # Initially hide all elements
        for element in elements:
            element.grid_remove()
        
        # Animate elements appearing one by one
        for i, element in enumerate(elements):
            time.sleep(0.12)  # Delay between each element
            app.after(0, lambda el=element: el.grid())
    
    # Run animation in separate thread
    threading.Thread(target=entrance_animation, daemon=True).start()

def validate_passwords():
    """Add real-time password validation feedback"""
    password = password_entry.get()
    confirm = confirm_entry.get()
    
    if len(password) > 0 and len(confirm) > 0:
        if password == confirm:
            confirm_entry.configure(border_color="#2d5016")  # Green for match
        else:
            confirm_entry.configure(border_color="#cc3300")  # Red for mismatch

# Bind Events
# Entry focus animations
first_name_entry.bind("<FocusIn>", lambda e: animate_entry_focus(first_name_entry, True))
first_name_entry.bind("<FocusOut>", lambda e: animate_entry_focus(first_name_entry, False))

last_name_entry.bind("<FocusIn>", lambda e: animate_entry_focus(last_name_entry, True))
last_name_entry.bind("<FocusOut>", lambda e: animate_entry_focus(last_name_entry, False))

email_entry.bind("<FocusIn>", lambda e: animate_entry_focus(email_entry, True))
email_entry.bind("<FocusOut>", lambda e: animate_entry_focus(email_entry, False))

password_entry.bind("<FocusIn>", lambda e: animate_entry_focus(password_entry, True))
password_entry.bind("<FocusOut>", lambda e: animate_entry_focus(password_entry, False))

confirm_entry.bind("<FocusIn>", lambda e: animate_entry_focus(confirm_entry, True))
confirm_entry.bind("<FocusOut>", lambda e: animate_entry_focus(confirm_entry, False))

# Password validation on typing
password_entry.bind("<KeyRelease>", lambda e: validate_passwords())
confirm_entry.bind("<KeyRelease>", lambda e: validate_passwords())

# Sign in link hover and click
signin_link.bind("<Enter>", lambda e: animate_hover(signin_link, True))
signin_link.bind("<Leave>", lambda e: animate_hover(signin_link, False))
signin_link.bind("<Button-1>", signin_click)

# Eye button hover effects
eye_button.bind("<Enter>", lambda e: eye_button.configure(hover_color="#b8b8b8"))
eye_button.bind("<Leave>", lambda e: eye_button.configure(hover_color="#d6d6d6"))

confirm_button.bind("<Enter>", lambda e: confirm_button.configure(hover_color="#b8b8b8"))
confirm_button.bind("<Leave>", lambda e: confirm_button.configure(hover_color="#d6d6d6"))

# Sign up button command
signup_button.configure(command=signup_click)

# Start entrance animation
animate_entrance()

# Run the app
app.mainloop()