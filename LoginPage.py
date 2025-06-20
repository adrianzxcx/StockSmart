import customtkinter as ctk
import threading
import time

# Appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class AnimatedLoginApp:
    def __init__(self):
        # App Setup
        self.app = ctk.CTk()
        self.app.geometry("1200x800")
        self.app.resizable(False, False)
        self.app.title("Login Page")
        
        # Animation variables
        self.is_animating = False
        
        self.setup_ui()
        self.animate_entrance()
    
    def setup_ui(self):
        # Grid Layout
        for col in (0, 1):
            self.app.grid_columnconfigure(col, weight=1, uniform="half")
        self.app.grid_rowconfigure(0, weight=1)

        # Left Frame
        self.left_frame = ctk.CTkFrame(self.app, fg_color="#8094c2", corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.left_frame.grid_propagate(False)

        # Right Frame
        self.right_frame = ctk.CTkFrame(self.app, fg_color="#f9f5eb", corner_radius=0)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Configure left frame grid
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        # Inner Content Frame (Left) - Initially hidden for animation
        self.left_inner_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.left_inner_frame.grid(row=0, column=0, padx=25, pady=20, sticky="")
        self.left_inner_frame.grid_columnconfigure(0, weight=1)
        
        # Initially hide the frame for entrance animation
        self.left_inner_frame.configure(fg_color="transparent")

        # Title
        self.title = ctk.CTkLabel(
            self.left_inner_frame,
            text="Welcome back!",
            font=ctk.CTkFont(family="Instrument Sans", size=38, weight="bold"),
            text_color="#0B1D4B"
        )
        self.title.grid(row=0, column=0, pady=(0, 0), padx=(20,100), sticky="w")

        # Subtitle
        self.subtitle = ctk.CTkLabel(
            self.left_inner_frame,
            text="Please enter your details",
            font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold"),
            text_color="white"
        )
        self.subtitle.grid(row=1, column=0, pady=(0, 25), padx=(25,0), sticky="w")

        # Email Label
        self.email_label = ctk.CTkLabel(
            self.left_inner_frame,
            text="Email",
            text_color="white",
            font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold")
        )
        self.email_label.grid(row=2, column=0, sticky="w", pady=(0, 4), padx=15)

        # Email Entry with focus animations
        self.email_entry = ctk.CTkEntry(
            self.left_inner_frame,
            placeholder_text="Enter your email",
            height=40,
            width=280,
            corner_radius=8,
            fg_color="#cbd3ea",
            font=ctk.CTkFont(family="Instrument Sans", size=15),
            border_width=2,
            border_color="#cbd3ea"
        )
        self.email_entry.grid(row=3, column=0, sticky="ew", pady=(0, 15), padx=15)
        self.email_entry.bind("<FocusIn>", lambda e: self.animate_entry_focus(self.email_entry, True))
        self.email_entry.bind("<FocusOut>", lambda e: self.animate_entry_focus(self.email_entry, False))

        # Password Label
        self.password_label = ctk.CTkLabel(
            self.left_inner_frame,
            text="Password",
            text_color="white",
            font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold")
        )
        self.password_label.grid(row=4, column=0, sticky="w", pady=(0, 4), padx=15)

        # Password Entry with focus animations
        self.password_entry = ctk.CTkEntry(
            self.left_inner_frame,
            placeholder_text="Enter your password",
            show="*",
            height=40,
            width=280,
            corner_radius=8,
            fg_color="#cbd3ea",
            font=ctk.CTkFont(family="Instrument Sans", size=15),
            border_width=2,
            border_color="#cbd3ea"
        )
        self.password_entry.grid(row=5, column=0, sticky="ew", pady=(0, 8), padx=15)
        self.password_entry.bind("<FocusIn>", lambda e: self.animate_entry_focus(self.password_entry, True))
        self.password_entry.bind("<FocusOut>", lambda e: self.animate_entry_focus(self.password_entry, False))

        # Forgot Password with hover animation
        self.forgot_password = ctk.CTkLabel(
            self.left_inner_frame,
            text="Forgot Password?",
            text_color="#2f2f41",
            font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold"),
            cursor="hand2"
        )
        self.forgot_password.grid(row=6, column=0, sticky="e", pady=(0, 20), padx=15)
        self.forgot_password.bind("<Enter>", lambda e: self.animate_hover(self.forgot_password, True))
        self.forgot_password.bind("<Leave>", lambda e: self.animate_hover(self.forgot_password, False))
        self.forgot_password.bind("<Button-1>", self.forgot_password_click)

        # Sign In Button with hover and click animations
        self.signin_button = ctk.CTkButton(
            self.left_inner_frame,
            text="Sign In",
            fg_color="#1A40A1",
            hover_color="#162A5C",
            height=40,
            width=280,
            corner_radius=8,
            font=ctk.CTkFont(family="Instrument Sans", size=16, weight="bold"),
            command=self.signin_click
        )
        self.signin_button.grid(row=7, column=0, sticky="", pady=(0, 20), padx=(100,100))

        # Sign Up Row
        self.signup_row = ctk.CTkFrame(self.left_inner_frame, fg_color="transparent")
        self.signup_row.grid(row=8, column=0, sticky="", pady=(0, 0))
        self.signup_row.grid_columnconfigure((0, 1), weight=0)

        # Sign Up Label
        self.signup_label = ctk.CTkLabel(
            self.signup_row,
            text="Don't have an account?",
            font=ctk.CTkFont(family="Instrument Sans", size=15, weight="normal"),
            text_color="white"
        )
        self.signup_label.grid(row=0, column=0, padx=(0, 5))

        # Sign Up Link with hover animation
        self.signup_link = ctk.CTkLabel(
            self.signup_row,
            text="Sign Up here",
            font=ctk.CTkFont(family="Instrument Sans", size=15, weight="bold"),
            text_color="#2f2f41",
            cursor="hand2"
        )
        self.signup_link.grid(row=0, column=1, padx=(0, 0))
        self.signup_link.bind("<Enter>", lambda e: self.animate_hover(self.signup_link, True))
        self.signup_link.bind("<Leave>", lambda e: self.animate_hover(self.signup_link, False))
        self.signup_link.bind("<Button-1>", self.signup_click)

    def animate_entrance(self):
        """Animate the entrance of form elements"""
        def entrance_animation():
            # Start with elements invisible
            elements = [
                self.title, self.subtitle, self.email_label, self.email_entry,
                self.password_label, self.password_entry, self.forgot_password,
                self.signin_button, self.signup_row
            ]
            
            # Initially hide all elements
            for element in elements:
                element.grid_remove()
            
            # Animate elements appearing one by one
            for i, element in enumerate(elements):
                time.sleep(0.1)  # Delay between each element
                self.app.after(0, lambda el=element: el.grid())
                
                # Add a subtle fade-in effect by temporarily changing opacity
                if hasattr(element, 'configure'):
                    try:
                        # Quick opacity animation simulation
                        original_color = element.cget("text_color") if hasattr(element, 'cget') else None
                        if original_color:
                            self.app.after(0, lambda: self.fade_in_element(element, original_color))
                    except:
                        pass
        
        # Run animation in separate thread
        threading.Thread(target=entrance_animation, daemon=True).start()

    def fade_in_element(self, element, original_color):
        """Simple fade-in effect simulation"""
        try:
            # This is a simplified fade-in effect
            element.configure(text_color=original_color)
        except:
            pass

    def animate_entry_focus(self, entry, is_focused):
        """Animate entry field when focused/unfocused"""
        if is_focused:
            entry.configure(border_color="#0B1D4B", border_width=3)
            # Subtle scale effect simulation
            entry.configure(height=42)
        else:
            entry.configure(border_color="#cbd3ea", border_width=2)
            entry.configure(height=40)

    def animate_hover(self, label, is_hovered):
        """Animate label hover effects"""
        if is_hovered:
            # Darken color on hover
            if label == self.forgot_password:
                label.configure(text_color="#1a1a2e")
            elif label == self.signup_link:
                label.configure(text_color="#1a1a2e")
        else:
            # Return to original color
            label.configure(text_color="#2f2f41")

    def signin_click(self):
        """Handle sign in button click with animation"""
        if self.is_animating:
            return
            
        self.is_animating = True
        
        # Button press animation
        original_text = self.signin_button.cget("text")
        self.signin_button.configure(text="Signing in...", state="disabled")
        
        def reset_button():
            time.sleep(1.5)  # Simulate login process
            self.app.after(0, lambda: self.signin_button.configure(text=original_text, state="normal"))
            self.is_animating = False
            
            # Show success animation
            self.app.after(0, self.show_success_message)
        
        threading.Thread(target=reset_button, daemon=True).start()

    def show_success_message(self):
        """Show a temporary success message"""
        success_label = ctk.CTkLabel(
            self.left_inner_frame,
            text="✓ Login Successful!",
            font=ctk.CTkFont(family="Instrument Sans", size=14, weight="bold"),
            text_color="#2d5016"
        )
        success_label.grid(row=9, column=0, pady=(10, 0))
        
        # Remove success message after 2 seconds
        self.app.after(2000, success_label.destroy)

    def forgot_password_click(self, event):
        """Handle forgot password click"""
        # Temporary feedback
        original_text = self.forgot_password.cget("text")
        self.forgot_password.configure(text="Check your email!")
        
        def reset_text():
            time.sleep(2)
            self.app.after(0, lambda: self.forgot_password.configure(text=original_text))
        
        threading.Thread(target=reset_text, daemon=True).start()

    def signup_click(self, event):
        """Handle sign up click"""
        # Temporary feedback
        original_text = self.signup_link.cget("text")
        self.signup_link.configure(text="Opening signup...")
        
        def reset_text():
            time.sleep(1.5)
            self.app.after(0, lambda: self.signup_link.configure(text=original_text))
        
        threading.Thread(target=reset_text, daemon=True).start()

    def run(self):
        """Start the application"""
        self.app.mainloop()

# Create and run the app
if __name__ == "__main__":
    app = AnimatedLoginApp()
    app.run()