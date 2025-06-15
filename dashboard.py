import customtkinter as ctk
from tkinter import PhotoImage
import json
import os
from tkcalendar import Calendar
import threading
import time
from tkinter import filedialog
from PIL import Image, ImageTk
import shutil

# ---------- Global Configuration ---------- #
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# Enhanced Fonts with better hierarchy
FONT_H1 = ("Segoe UI", 28, "bold")
FONT_H2 = ("Segoe UI", 20, "bold")
FONT_H3 = ("Segoe UI", 16, "bold")
FONT_BODY = ("Segoe UI", 14)
FONT_SMALL = ("Segoe UI", 12)
FONT_BUTTON = ("Segoe UI", 14, "bold")
FONT_CARD_VALUE = ("Segoe UI", 32, "bold")

# Updated Color Scheme - Based on your provided palette
COLOR_GREY_BEIGE = "#f5f5eb"  # Grey Beige - Primary Background
COLOR_ROYAL_BLUE = "#11225b"  # Royal Blue - Primary Actions
COLOR_SAPPHIRE = "#8094c2"    # Sapphire - Secondary Elements

# Enhanced palette built around your main colors
COLOR_PRIMARY = COLOR_ROYAL_BLUE
COLOR_PRIMARY_HOVER = "#0d1a47"  # Darker Royal Blue
COLOR_SECONDARY = COLOR_SAPPHIRE
COLOR_SECONDARY_LIGHT = "#a0b3d9"  # Lighter Sapphire
COLOR_SECONDARY_DARK = "#6b7ba8"   # Darker Sapphire

# Background variations using Grey Beige
COLOR_MAIN_BG = COLOR_GREY_BEIGE
COLOR_SIDEBAR_BG = "#f0f0e6"      # Slightly darker Grey Beige
COLOR_SIDEBAR_ACTIVE = "#ebebd9"   # Active sidebar item
COLOR_CARD_BG = "#fafaff"          # Card backgrounds (very light grey-beige)

# Accent colors that complement your main theme
COLOR_ACCENT_SUCCESS = "#2d5a27"   # Dark green that works with your palette
COLOR_ACCENT_WARNING = "#8b6914"   # Golden brown
COLOR_ACCENT_ERROR = "#7a2e2e"     # Dark red
COLOR_ACCENT_INFO = COLOR_SAPPHIRE

# Neutral colors derived from your palette
COLOR_WHITE = "#ffffff"
COLOR_GRAY_50 = COLOR_GREY_BEIGE
COLOR_GRAY_100 = "#ebebd9"
COLOR_GRAY_200 = "#d6d6c4"
COLOR_GRAY_300 = "#c2c2af"
COLOR_GRAY_600 = "#6b6b5a"
COLOR_GRAY_700 = "#565645"
COLOR_GRAY_800 = "#414130"
COLOR_GRAY_900 = COLOR_ROYAL_BLUE

# Text colors that work well with your palette
COLOR_TEXT_PRIMARY = COLOR_ROYAL_BLUE
COLOR_TEXT_SECONDARY = COLOR_SAPPHIRE
COLOR_TEXT_MUTED = "#7a7a6b"

# Shadow effects (simulated with frames)
SHADOW_COLOR = "#00000010"

# ---------- Profile Persistence ---------- #
PROFILE_DATA_PATH = "user_profile.json"

# ---------- Enhanced Mock Data ---------- #
PRODUCT_DATA = [
    {"name": "Premium Widget A", "sku": "WGT-A001", "price": "$25.99", "stock": 120, "trend": "up"},
    {"name": "Smart Widget B", "sku": "WGT-B002", "price": "$15.49", "stock": 85, "trend": "stable"},
    {"name": "Ultra Widget C", "sku": "WGT-C003", "price": "$12.99", "stock": 0, "trend": "down"},
    {"name": "Pro Gadget X", "sku": "GDX-X004", "price": "$45.00", "stock": 42, "trend": "up"},
    {"name": "Elite Gadget Y", "sku": "GDX-Y005", "price": "$38.75", "stock": 7, "trend": "down"},
]

MOST_CONSUMED = [
    ("Cooking Oil", 85, COLOR_PRIMARY),
    ("Fresh Onions", 78, COLOR_ACCENT_SUCCESS),
    ("Tomatoes", 72, COLOR_ACCENT_ERROR),
    ("Garlic Cloves", 68, COLOR_SECONDARY),
    ("Potatoes", 65, COLOR_ACCENT_WARNING),
    ("Cane Sugar", 58, COLOR_SECONDARY_DARK),
    ("All-Purpose Flour", 52, COLOR_GRAY_600),
    ("Soy Sauce", 48, COLOR_GRAY_700),
    ("Fresh Ginger", 42, COLOR_GRAY_800)
]

def load_user_profile_data():
    if os.path.exists(PROFILE_DATA_PATH):
        with open(PROFILE_DATA_PATH, "r") as f:
            return json.load(f)
    return {
        "First Name": "Mingyu",
        "Last Name": "Kim",
        "Email": "kimmingyu@gmail.com",
        "Phone Number": "+82 10-1234-5678",
        "Department": "Inventory Management",
        "Role": "Owner"
    }

def save_user_profile_data(data):
    with open(PROFILE_DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

class AnimatedButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.original_color = self._fg_color
        
    def on_enter(self, event):
        self.configure(cursor="hand2")
        # Subtle hover animation
        
    def on_leave(self, event):
        self.configure(cursor="")

class ShadowFrame(ctk.CTkFrame):
    """Custom frame with shadow effect simulation"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
class EnhancedCard(ctk.CTkFrame):
    def __init__(self, parent, bg_color, icon_text, value, label_text, trend=None):
        super().__init__(parent, corner_radius=16, fg_color=COLOR_CARD_BG, border_width=1, border_color=COLOR_GRAY_200)
        
        # Hover effect
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        # Icon with colored background
        icon_frame = ctk.CTkFrame(self, fg_color=bg_color, corner_radius=12, width=60, height=60)
        icon_frame.pack(pady=(20, 10))
        icon_frame.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(icon_frame, text=icon_text, font=("Segoe UI", 24), text_color=COLOR_WHITE)
        icon_label.pack(expand=True)
        
        # Value with animation placeholder
        self.value_label = ctk.CTkLabel(self, text="0", font=FONT_CARD_VALUE, text_color=COLOR_TEXT_PRIMARY)
        self.value_label.pack(pady=(0, 5))
        
        # Label
        label = ctk.CTkLabel(self, text=label_text, font=FONT_BODY, text_color=COLOR_TEXT_MUTED)
        label.pack(pady=(0, 20))
        
        # Trend indicator
        if trend:
            trend_frame = ctk.CTkFrame(self, fg_color="transparent")
            trend_frame.pack(pady=(0, 15))
            
            trend_color = COLOR_ACCENT_SUCCESS if trend == "up" else COLOR_ACCENT_ERROR if trend == "down" else COLOR_TEXT_MUTED
            trend_icon = "↗" if trend == "up" else "↘" if trend == "down" else "→"
            
            trend_label = ctk.CTkLabel(trend_frame, text=f"{trend_icon} {trend.title()}", 
                                     font=FONT_SMALL, text_color=trend_color)
            trend_label.pack()
        
        # Animate the value
        self.animate_value(value)
        
    def animate_value(self, target_value):
        """Animate the counter from 0 to target value"""
        def animate():
            current = 0
            target = int(target_value.replace(',', ''))
            step = max(1, target // 30)  # 30 frames for smooth animation
            
            while current < target:
                current = min(current + step, target)
                formatted_value = f"{current:,}" if current >= 1000 else str(current)
                self.value_label.configure(text=formatted_value)
                time.sleep(0.03)
        
        threading.Thread(target=animate, daemon=True).start()
        
    def on_enter(self, event):
        self.configure(border_width=2, border_color=COLOR_PRIMARY)
        
    def on_leave(self, event):
        self.configure(border_width=1, border_color=COLOR_GRAY_200)

class UserProfilePopup(ctk.CTkToplevel):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.edit_mode = False
        self.master = master
        self.setup_window()
        self.setup_ui()
        
        # Center the popup on the parent window
        self.center_on_parent()
        
        # Make the popup modal
        self.transient(master)
        self.grab_set()
        
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        self.title("User Profile")
        self.geometry("500x650")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_MAIN_BG)
        
        # Remove window decorations for a more modern look (optional)
        # self.overrideredirect(True)

    def center_on_parent(self):
        """Center the popup window on the parent window"""
        self.update_idletasks()
        
        # Get parent window geometry
        parent_x = self.master.winfo_x()
        parent_y = self.master.winfo_y()
        parent_width = self.master.winfo_width()
        parent_height = self.master.winfo_height()
        
        # Calculate center position
        popup_width = 500
        popup_height = 650
        x = parent_x + (parent_width - popup_width) // 2
        y = parent_y + (parent_height - popup_height) // 2
        
        self.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    def setup_ui(self):
        # Main container with modern styling
        main_container = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, corner_radius=20, 
                                    border_width=2, border_color=COLOR_GRAY_200)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header with close button
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent", height=60)
        header_frame.pack(fill="x", padx=25, pady=(20, 0))
        header_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(header_frame, text="👤 User Profile", font=FONT_H2, text_color=COLOR_TEXT_PRIMARY)
        title_label.pack(side="left", pady=15)

        # Close button
        close_btn = AnimatedButton(header_frame, text="✕", font=("Segoe UI", 16, "bold"),
                                 fg_color=COLOR_ACCENT_ERROR, hover_color="#5a1e1e",
                                 text_color=COLOR_WHITE, corner_radius=15, width=30, height=30,
                                 command=self.on_close)
        close_btn.pack(side="right", pady=15)

        # Edit button
        self.edit_btn = AnimatedButton(header_frame, text="✏ Edit", command=self.toggle_edit,
                                     fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER,
                                     text_color=COLOR_WHITE, corner_radius=8, height=36)
        self.edit_btn.pack(side="right", padx=(0, 10), pady=15)

        # Content area
        content_frame = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)

        # Profile image section
        self.setup_profile_image_section(content_frame)

        # Profile form
        self.entries = {}
        self.profile_data = load_user_profile_data()

        # Form fields with enhanced styling
        for i, (label_text, default_value) in enumerate(self.profile_data.items()):
            # Skip Photo Path field in the form
            if label_text == "Photo Path":
                continue
                
            # Field container
            field_frame = ctk.CTkFrame(content_frame, fg_color="transparent", height=80)
            field_frame.pack(fill="x", pady=10)
            field_frame.pack_propagate(False)
            
            # Label
            label = ctk.CTkLabel(field_frame, text=label_text, font=FONT_H3, text_color=COLOR_TEXT_SECONDARY)
            label.pack(anchor="w", pady=(0, 5))
            
            # Entry with modern styling
            entry = ctk.CTkEntry(field_frame, placeholder_text=f"Enter {label_text.lower()}",
                               font=FONT_BODY, text_color=COLOR_TEXT_PRIMARY, height=45,
                               fg_color=COLOR_GRAY_50, border_color=COLOR_GRAY_300,
                               corner_radius=10)
            entry.insert(0, default_value)
            entry.configure(state="readonly")
            entry.pack(fill="x", pady=(0, 5))
            self.entries[label_text] = entry

        # Action buttons
        button_frame = ctk.CTkFrame(main_container, fg_color="transparent", height=60)
        button_frame.pack(fill="x", padx=25, pady=(0, 20))
        button_frame.pack_propagate(False)

        # Save and Cancel buttons (initially hidden)
        self.save_btn = AnimatedButton(button_frame, text="💾 Save Changes", 
                                     fg_color=COLOR_ACCENT_SUCCESS, hover_color="#1f3d1b",
                                     text_color=COLOR_WHITE, corner_radius=10, height=45,
                                     command=self.save_changes)
        
        self.cancel_btn = AnimatedButton(button_frame, text="❌ Cancel", 
                                       fg_color=COLOR_GRAY_600, hover_color=COLOR_GRAY_700,
                                       text_color=COLOR_WHITE, corner_radius=10, height=45,
                                       command=self.cancel_changes)

    def setup_profile_image_section(self, content_frame):
        """Setup the profile image section with upload functionality"""
        # Profile image section
        profile_section = ctk.CTkFrame(content_frame, fg_color="transparent", height=140)
        profile_section.pack(fill="x", pady=(0, 20))
        profile_section.pack_propagate(False)
        
        profile_frame = ctk.CTkFrame(profile_section, fg_color=COLOR_PRIMARY, corner_radius=60, 
                                   width=120, height=120)
        profile_frame.pack()
        profile_frame.pack_propagate(False)
        
        # Check if user has a profile photo
        photo_path = self.profile_data.get("Photo Path", "") if hasattr(self, 'profile_data') else ""
        if photo_path and os.path.exists(photo_path):
            try:
                image = Image.open(photo_path)
                image = image.resize((100, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                self.profile_icon = ctk.CTkLabel(profile_frame, image=photo, text="")
                self.profile_icon.image = photo  # Keep a reference
            except:
                # Fallback to default icon
                self.profile_icon = ctk.CTkLabel(profile_frame, text="👤", font=("Segoe UI", 48), text_color=COLOR_WHITE)
        else:
            self.profile_icon = ctk.CTkLabel(profile_frame, text="👤", font=("Segoe UI", 48), text_color=COLOR_WHITE)
        
        self.profile_icon.pack(expand=True)
        
        # Upload button (initially hidden)
        self.upload_btn = AnimatedButton(profile_section, text="📷 Upload Photo", 
                                       fg_color=COLOR_SECONDARY, hover_color=COLOR_SECONDARY_DARK,
                                       text_color=COLOR_WHITE, corner_radius=8, height=30,
                                       font=FONT_SMALL, command=self.upload_photo)
        # Don't pack initially - will be shown in edit mode

    def upload_photo(self):
        """Handle photo upload functionality"""
        file_path = filedialog.askopenfilename(
            title="Select Profile Photo",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Create a directory for profile photos if it doesn't exist
                if not os.path.exists("profile_photos"):
                    os.makedirs("profile_photos")
                
                # Copy the image to our profile photos directory
                file_extension = os.path.splitext(file_path)[1]
                new_filename = f"profile_{self.profile_data.get('First Name', 'user').lower()}{file_extension}"
                new_path = os.path.join("profile_photos", new_filename)
                
                # Copy and resize the image
                image = Image.open(file_path)
                # Resize to a reasonable size (120x120 for profile)
                image = image.resize((120, 120), Image.Resampling.LANCZOS)
                image.save(new_path)
                
                # Update profile data with photo path
                self.profile_data["Photo Path"] = new_path
                
                # Update the profile image display
                self.update_profile_image(new_path)
                
                print(f"Profile photo uploaded successfully: {new_path}")
                
            except Exception as e:
                print(f"Error uploading photo: {e}")

    def update_profile_image(self, image_path):
        """Update the profile image display"""
        try:
            # Load and display the new image
            image = Image.open(image_path)
            image = image.resize((100, 100), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Update the profile icon
            self.profile_icon.configure(image=photo, text="")
            self.profile_icon.image = photo  # Keep a reference
            
        except Exception as e:
            print(f"Error updating profile image: {e}")

    def toggle_edit(self):
        self.edit_mode = not self.edit_mode
        new_state = "normal" if self.edit_mode else "readonly"

        for entry in self.entries.values():
            entry.configure(state=new_state)
            if self.edit_mode:
                entry.configure(border_color=COLOR_PRIMARY, border_width=2)
            else:
                entry.configure(border_color=COLOR_GRAY_300, border_width=1)

        # Update UI based on edit mode
        if self.edit_mode:
            self.edit_btn.configure(text="❌ Cancel Edit")
            self.save_btn.pack(side="left", expand=True, fill="x", padx=(0, 10))
            self.cancel_btn.pack(side="right", expand=True, fill="x", padx=(10, 0))
            # Show upload button in edit mode
            if hasattr(self, 'upload_btn'):
                self.upload_btn.pack(pady=(5, 0))
        else:
            self.edit_btn.configure(text="✏ Edit")
            self.save_btn.pack_forget()
            self.cancel_btn.pack_forget()
            # Hide upload button when not editing
            if hasattr(self, 'upload_btn'):
                self.upload_btn.pack_forget()

    def save_changes(self):
        """Save the profile changes"""
        updated_data = {label: entry.get() for label, entry in self.entries.items()}
        # Keep the photo path if it exists
        if "Photo Path" in self.profile_data:
            updated_data["Photo Path"] = self.profile_data["Photo Path"]
        
        self.profile_data.update(updated_data)
        save_user_profile_data(self.profile_data)
        
        # Exit edit mode
        self.edit_mode = False
        self.toggle_edit()
        
        # Show success message (you could add a toast notification here)
        print("Profile updated successfully!")

    def cancel_changes(self):
        """Cancel changes and restore original values"""
        for label, entry in self.entries.items():
            entry.delete(0, 'end')
            entry.insert(0, self.profile_data[label])
        
        # Exit edit mode
        self.edit_mode = False
        self.toggle_edit()

    def on_close(self):
        """Handle window close event"""
        if self.edit_mode:
            # If in edit mode, ask for confirmation or auto-cancel
            self.cancel_changes()
        
        self.grab_release()
        self.destroy()

class ModernSidebar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=280, fg_color=COLOR_SAPPHIRE, corner_radius=0, **kwargs)
        self.pack_propagate(False)
        self.active_button = None
        self.setup_ui()
        
    def setup_ui(self):
        # Logo section with better styling
        logo_frame = ctk.CTkFrame(self, fg_color="transparent", height=100)
        logo_frame.pack(fill="x", pady=(30, 40))
        logo_frame.pack_propagate(False)
        
        logo_icon = ctk.CTkLabel(logo_frame, text="📊", font=("Segoe UI", 32))
        logo_icon.pack()
        
        logo_label = ctk.CTkLabel(logo_frame, text="StockSmart", font=FONT_H1, text_color=COLOR_ROYAL_BLUE)
        logo_label.pack(pady=(5, 0))
        
        subtitle = ctk.CTkLabel(logo_frame, text="Dashboard", font=FONT_SMALL, text_color=COLOR_ROYAL_BLUE)
        subtitle.pack()

        # Navigation with modern design
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="x", padx=20)

        nav_buttons = [
            ("Dashboard", "🏠", True),
            ("Inventory", "📦", False),
            ("Items", "🏷️", False),
            ("History Logs", "📋", False)
        ]

        for name, icon, is_active in nav_buttons:
            btn = self.create_nav_button(nav_frame, name, icon, is_active)
            btn.pack(fill="x", pady=5)
            
        # User section at bottom
        user_frame = ctk.CTkFrame(self, fg_color=COLOR_SECONDARY_DARK, corner_radius=12, height=80)
        user_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        user_frame.pack_propagate(False)
        
        user_info = ctk.CTkLabel(user_frame, text="👤 Mingyu Kim\nOwner", 
                               font=FONT_SMALL, text_color=COLOR_WHITE, justify="left")
        user_info.pack(expand=True, padx=15)

    def create_nav_button(self, parent, name, icon, is_active=False):
        fg_color = COLOR_SECONDARY_DARK if is_active else "transparent"
        text_color = COLOR_ROYAL_BLUE if is_active else COLOR_ROYAL_BLUE
        hover_color = COLOR_SECONDARY_LIGHT if not is_active else COLOR_SECONDARY_DARK
        
        btn = ctk.CTkButton(parent, text=f"{icon}  {name}", font=FONT_BUTTON,
                           text_color=text_color, fg_color=fg_color,
                           hover_color=hover_color, corner_radius=10, height=50,
                           anchor="w", command=lambda n=name: self.set_active(n))
        
        if is_active:
            self.active_button = btn
            
        return btn
        
    def set_active(self, name):
        print(f"{name} clicked")
        # Reset all buttons and set new active

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("StockSmart Dashboard - Enhanced")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        self.configure(bg=COLOR_MAIN_BG)

        self.profile_popup = None
        self.setup_ui()

    def setup_ui(self):
        # Modern sidebar
        self.sidebar = ModernSidebar(self)
        self.sidebar.pack(side="left", fill="y")

        # Main content area
        self.main_frame = ctk.CTkScrollableFrame(self, fg_color=COLOR_MAIN_BG, corner_radius=0)
        self.main_frame.pack(side="left", fill="both", expand=True)

        self.build_top_bar()
        self.build_overview_section()
        self.build_analytics_section()

    def build_top_bar(self):
        top_bar = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=80)
        top_bar.pack(fill="x", padx=30, pady=(20, 0))
        top_bar.pack_propagate(False)

        # Welcome section
        welcome_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        welcome_frame.pack(side="left", expand=True, fill="both")
        
        welcome_label = ctk.CTkLabel(welcome_frame, text="Good morning, Mingyu! 👋", 
                                   font=FONT_H1, text_color=COLOR_TEXT_PRIMARY)
        welcome_label.pack(anchor="w", pady=(10, 0))
        
        subtitle = ctk.CTkLabel(welcome_frame, text="Here's what's happening with your inventory today", 
                              font=FONT_BODY, text_color=COLOR_TEXT_MUTED)
        subtitle.pack(anchor="w")

        # Actions section
        actions_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        actions_frame.pack(side="right")

        # Notification bell with badge
        notif_frame = ctk.CTkFrame(actions_frame, fg_color=COLOR_CARD_BG, corner_radius=8, width=50, height=50)
        notif_frame.pack(side="left", padx=10)
        notif_frame.pack_propagate(False)
        
        bell = ctk.CTkLabel(notif_frame, text="🔔", font=("Segoe UI", 18))
        bell.pack(expand=True)

        # Profile button
        profile_btn = AnimatedButton(actions_frame, text="👤 Mingyu Kim ▼", font=FONT_BODY,
                                   text_color=COLOR_TEXT_SECONDARY, fg_color=COLOR_CARD_BG,
                                   hover_color=COLOR_SIDEBAR_ACTIVE, corner_radius=8, height=50,
                                   command=self.show_user_profile)
        profile_btn.pack(side="left", padx=10)

    def build_overview_section(self):
        # Main overview container
        overview_frame = ctk.CTkFrame(self.main_frame, corner_radius=16, fg_color=COLOR_CARD_BG, 
                                    border_width=1, border_color=COLOR_GRAY_200)
        overview_frame.pack(fill="x", padx=30, pady=20)

        # Section header
        header_frame = ctk.CTkFrame(overview_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(25, 20))
        
        overview_label = ctk.CTkLabel(header_frame, text="📊 Overview", font=FONT_H2, text_color=COLOR_TEXT_PRIMARY)
        overview_label.pack(side="left")
        
        refresh_btn = AnimatedButton(header_frame, text="🔄 Refresh", font=FONT_SMALL,
                                   fg_color=COLOR_SIDEBAR_BG, text_color=COLOR_TEXT_SECONDARY,
                                   hover_color=COLOR_SIDEBAR_ACTIVE, corner_radius=6, height=32,
                                   command=self.refresh_data)
        refresh_btn.pack(side="right")

        # Cards container
        cards_frame = ctk.CTkFrame(overview_frame, fg_color="transparent")
        cards_frame.pack(fill="x", padx=30, pady=(0, 25))

        # Enhanced cards with trends using your color scheme
        cards_data = [
            (COLOR_PRIMARY, "📦", "1,247", "Total Products", "up"),
            (COLOR_ACCENT_SUCCESS, "✅", "15,830", "Items in Stock", "up"),
            (COLOR_ACCENT_ERROR, "⚠️", "23", "Out of Stock", "down"),
            (COLOR_ACCENT_WARNING, "🔔", "156", "Low Stock Alerts", "stable")
        ]

        for bg_color, icon, value, label, trend in cards_data:
            card = EnhancedCard(cards_frame, bg_color, icon, value, label, trend)
            card.pack(side="left", expand=True, fill="both", padx=8)

    def build_analytics_section(self):
        # Analytics container
        analytics_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        analytics_frame.pack(fill="x", padx=30, pady=(0, 30))

        # Calendar section
        calendar_frame = ctk.CTkFrame(analytics_frame, corner_radius=16, fg_color=COLOR_CARD_BG,
                                    border_width=1, border_color=COLOR_GRAY_200)
        calendar_frame.pack(side="left", fill="y", padx=(0, 15))

        cal_header = ctk.CTkLabel(calendar_frame, text="📅 Calendar", font=FONT_H3, text_color=COLOR_TEXT_PRIMARY)
        cal_header.pack(pady=(20, 15))

        calendar = Calendar(
            calendar_frame,
            selectmode='day',
            year=2025, month=6, day=15,
            background=COLOR_CARD_BG,
            foreground=COLOR_TEXT_SECONDARY,
            headersbackground=COLOR_PRIMARY,
            headersforeground=COLOR_WHITE,
            selectbackground=COLOR_SECONDARY,
            selectforeground=COLOR_WHITE,
            weekendbackground=COLOR_SIDEBAR_BG,
            weekendforeground=COLOR_TEXT_MUTED,
            bordercolor=COLOR_GRAY_200,
            font=FONT_BODY,
            firstweekday='sunday'
        )
        calendar.pack(padx=20, pady=(0, 20))

        # Consumption chart
        chart_frame = ctk.CTkFrame(analytics_frame, corner_radius=16, fg_color=COLOR_CARD_BG,
                                 border_width=1, border_color=COLOR_GRAY_200)
        chart_frame.pack(side="right", fill="both", expand=True)

        chart_header = ctk.CTkFrame(chart_frame, fg_color="transparent")
        chart_header.pack(fill="x", padx=25, pady=(20, 15))
        
        chart_title = ctk.CTkLabel(chart_header, text="📈 Top Consumed Products", 
                                 font=FONT_H3, text_color=COLOR_TEXT_PRIMARY)
        chart_title.pack(side="left")
        
        period_label = ctk.CTkLabel(chart_header, text="This Week", 
                                  font=FONT_SMALL, text_color=COLOR_TEXT_MUTED)
        period_label.pack(side="right")

        # Enhanced consumption bars
        chart_content = ctk.CTkScrollableFrame(chart_frame, fg_color="transparent")
        chart_content.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        for i, (item, value, color) in enumerate(MOST_CONSUMED):
            self.create_consumption_bar(chart_content, item, value, color, i)

    def create_consumption_bar(self, parent, item, value, color, index):
        bar_container = ctk.CTkFrame(parent, fg_color="transparent", height=50)
        bar_container.pack(fill="x", pady=8)
        bar_container.pack_propagate(False)

        # Item info
        info_frame = ctk.CTkFrame(bar_container, fg_color="transparent")
        info_frame.pack(fill="x")
        
        item_label = ctk.CTkLabel(info_frame, text=item, font=FONT_BODY, text_color=COLOR_TEXT_SECONDARY)
        item_label.pack(side="left")
        
        value_label = ctk.CTkLabel(info_frame, text=f"{value}%", font=FONT_SMALL, text_color=COLOR_TEXT_MUTED)
        value_label.pack(side="right")

        # Progress bar
        progress_bg = ctk.CTkFrame(bar_container, fg_color=COLOR_SIDEBAR_BG, height=8, corner_radius=4)
        progress_bg.pack(fill="x", pady=(5, 0))
        
        # Animated progress bar
        progress_bar = ctk.CTkFrame(progress_bg, fg_color=color, height=8, corner_radius=4)
        progress_bar.place(x=0, y=0, relheight=1)
        
        # Animate the progress bar
        self.animate_progress_bar(progress_bar, value)

    def animate_progress_bar(self, bar, target_width):
        def animate():
            current_width = 0
            target = target_width / 100  # Convert percentage to decimal
            step = target / 30  # 30 frames
            
            while current_width < target:
                current_width = min(current_width + step, target)
                bar.place(x=0, y=0, relwidth=current_width, relheight=1)
                time.sleep(0.02)
        
        threading.Thread(target=animate, daemon=True).start()

    def show_user_profile(self):
        """Show the user profile popup"""
        if self.profile_popup is None or not self.profile_popup.winfo_exists():
            self.profile_popup = UserProfilePopup(self)
        else:
            # If popup already exists, bring it to front
            self.profile_popup.lift()
            self.profile_popup.focus()

    def refresh_data(self):
        print("Refreshing data...")
        # Add actual refresh logic here

if __name__ == "__main__":
    app = App()
    app.mainloop()