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
from datetime import datetime, timedelta

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

class AnimatedButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.original_color = self._fg_color
        
    def on_enter(self, event):
        self.configure(cursor="hand2")
        
    def on_leave(self, event):
        self.configure(cursor="")

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
        
        subtitle = ctk.CTkLabel(logo_frame, text="Inventory Management", font=FONT_SMALL, text_color=COLOR_ROYAL_BLUE)
        subtitle.pack()

        # Navigation with modern design
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="x", padx=20)

        nav_buttons = [
            ("Dashboard", "🏠", False),
            ("Inventory", "📦", False),
            ("Items", "🏷️", False),
            ("History Logs", "📋", True)  # This is now active
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
        text_color = COLOR_WHITE if is_active else COLOR_ROYAL_BLUE
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

class FilterPopup(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Filter History")
        self.geometry("400x400")
        self.resizable(False, False)
        self.parent = parent
        
        # Make the popup always stay on top
        self.attributes("-topmost", True)
        
        # Center the popup on the parent window
        self.transient(parent)
        
        # Set focus to this window
        self.grab_set()
        self.focus_set()
        
        # Position the popup in the center of the parent window
        self.center_on_parent()
        
        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.setup_ui()

    def center_on_parent(self):
        """Center the popup on the parent window"""
        self.update_idletasks()  # Ensure the window size is calculated
        
        # Get parent window position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Get popup size
        popup_width = self.winfo_reqwidth()
        popup_height = self.winfo_reqheight()
        
        # Calculate center position
        x = parent_x + (parent_width - popup_width) // 2
        y = parent_y + (parent_height - popup_height) // 2
        
        # Set the position
        self.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    def setup_ui(self):
        """Setup the UI elements"""
        # Example filter options
        self.action_types = {
            "Add": ctk.BooleanVar(),
            "Deduct": ctk.BooleanVar(),
            "Update": ctk.BooleanVar(),
            "Alert": ctk.BooleanVar(),
            "Remove": ctk.BooleanVar()
        }
        self.user_entry = ctk.CTkEntry(self, placeholder_text="User (optional)")
        self.date_from = ctk.CTkEntry(self, placeholder_text="From Date (YYYY-MM-DD)")
        self.date_to = ctk.CTkEntry(self, placeholder_text="To Date (YYYY-MM-DD)")

        ctk.CTkLabel(self, text="Action Types:", font=FONT_H3).pack(anchor="w", padx=20, pady=(20, 0))
        for name, var in self.action_types.items():
            ctk.CTkCheckBox(self, text=name, variable=var).pack(anchor="w", padx=40)

        ctk.CTkLabel(self, text="User:", font=FONT_H3).pack(anchor="w", padx=20, pady=(20, 0))
        self.user_entry.pack(fill="x", padx=40)

        ctk.CTkLabel(self, text="Date Range:", font=FONT_H3).pack(anchor="w", padx=20, pady=(20, 0))
        self.date_from.pack(fill="x", padx=40, pady=(0, 5))
        self.date_to.pack(fill="x", padx=40)

        # Button frame for better layout
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)
        
        # Apply button
        apply_btn = ctk.CTkButton(button_frame, text="Apply Filters", 
                                 fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER,
                                 command=self.apply)
        apply_btn.pack(side="left", padx=10)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(button_frame, text="Cancel", 
                                  fg_color=COLOR_GRAY_600, hover_color=COLOR_GRAY_700,
                                  command=self.on_close)
        cancel_btn.pack(side="left", padx=10)

    def apply(self):
        """Apply filters and close popup"""
        filters = {
            "action_types": [k.lower() for k, v in self.action_types.items() if v.get()],
            "users": [self.user_entry.get()] if self.user_entry.get() else [],
            "date_from": self.date_from.get(),
            "date_to": self.date_to.get()
        }
        self.parent.apply_filters(filters)
        self.on_close()

    def on_close(self):
        """Handle window close event"""
        # Reset the filter popup reference in parent
        self.parent.filter_popup = None
        self.grab_release()
        self.destroy()

class HistoryLogsPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("StockSmart - History Logs")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        self.configure(bg=COLOR_MAIN_BG)
        
        # Initialize filter popup reference
        self.filter_popup = None
        
        # Sample history data
        self.history_data = self.generate_history_data()
        
        self.setup_ui()

    def generate_history_data(self):
        """Generate sample history data"""
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        return {
            "Today, May 23, 2025": [
                {
                    "action": "Added Stocks:",
                    "description": "Kim Mingyu added 9 stocks of Cooking Oil",
                    "time": "10 mins ago",
                    "type": "add",
                    "icon": "➕"
                },
                {
                    "action": "Deducted Stocks:",
                    "description": "Kim Mingyu deducted 3 stocks of Fresh Onions",
                    "time": "25 mins ago",
                    "type": "deduct",
                    "icon": "➖"
                },
                {
                    "action": "Updated Item:",
                    "description": "Kim Mingyu updated the price of Tomatoes to $2.50",
                    "time": "1 hour ago",
                    "type": "update",
                    "icon": "✏️"
                },
                {
                    "action": "Added New Item:",
                    "description": "Kim Mingyu added Organic Quinoa to inventory",
                    "time": "2 hours ago",
                    "type": "add",
                    "icon": "🆕"
                }
            ],
            "Yesterday, May 22, 2025": [
                {
                    "action": "Deducted Stocks:",
                    "description": "Kim Mingyu deducted 15 stocks of All-Purpose Flour",
                    "time": "8:30 PM",
                    "type": "deduct",
                    "icon": "➖"
                },
                {
                    "action": "Added Stocks:",
                    "description": "Kim Mingyu added 20 stocks of Soy Sauce",
                    "time": "6:15 PM",
                    "type": "add",
                    "icon": "➕"
                },
                {
                    "action": "Stock Alert:",
                    "description": "System generated low stock alert for Fish Sauce",
                    "time": "3:45 PM",
                    "type": "alert",
                    "icon": "⚠️"
                },
                {
                    "action": "Updated Item:",
                    "description": "Kim Mingyu updated expiry date for Cane Sugar",
                    "time": "2:20 PM",
                    "type": "update",
                    "icon": "✏️"
                },
                {
                    "action": "Removed Item:",
                    "description": "Kim Mingyu removed expired Rice Noodles from inventory",
                    "time": "11:30 AM",
                    "type": "remove",
                    "icon": "🗑️"
                }
            ]
        }

    def setup_ui(self):
        # Modern sidebar
        self.sidebar = ModernSidebar(self)
        self.sidebar.pack(side="left", fill="y")

        # Main content area
        self.main_frame = ctk.CTkFrame(self, fg_color=COLOR_MAIN_BG, corner_radius=0)
        self.main_frame.pack(side="left", fill="both", expand=True)

        self.build_header()
        self.build_content()

    def build_header(self):
        """Build the header section with title and user info"""
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=80)
        header_frame.pack(fill="x", padx=30, pady=(20, 0))
        header_frame.pack_propagate(False)

        # Title section
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", expand=True, fill="both")
        
        title_label = ctk.CTkLabel(title_frame, text="📋 History", 
                                 font=FONT_H1, text_color=COLOR_TEXT_PRIMARY)
        title_label.pack(anchor="w", pady=(15, 0))
        
        subtitle = ctk.CTkLabel(title_frame, text="Track all inventory changes and activities", 
                              font=FONT_BODY, text_color=COLOR_TEXT_MUTED)
        subtitle.pack(anchor="w")

        # Actions section
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.pack(side="right")

        # Notification bell
        notif_btn = AnimatedButton(
            actions_frame,
            text="🔔",
            font=("Segoe UI", 18),
            fg_color=COLOR_CARD_BG,
            hover_color=COLOR_SIDEBAR_ACTIVE,
            text_color=COLOR_TEXT_SECONDARY,
            corner_radius=8,
            width=50,
            height=50,
            command=self.show_notifications
        )
        notif_btn.pack(side="left", padx=10)

        # User dropdown
        user_btn = AnimatedButton(actions_frame, text="👤 Mingyu Kim ▼", font=FONT_BODY,
                                text_color=COLOR_TEXT_SECONDARY, fg_color=COLOR_CARD_BG,
                                hover_color=COLOR_SIDEBAR_ACTIVE, corner_radius=8, height=50,
                                command=self.show_user_menu)
        user_btn.pack(side="left", padx=10)

    def build_content(self):
        """Build the main content area with search and history feed"""
        # Content container
        content_container = ctk.CTkFrame(self.main_frame, corner_radius=16, fg_color=COLOR_CARD_BG,
                                       border_width=1, border_color=COLOR_GRAY_200)
        content_container.pack(fill="both", expand=True, padx=30, pady=20)

        # Toolbar section
        self.build_toolbar(content_container)
        
        # History feed
        self.build_history_feed(content_container)

    def build_toolbar(self, parent):
        """Build the search and filter toolbar"""
        toolbar_frame = ctk.CTkFrame(parent, fg_color="transparent", height=60)
        toolbar_frame.pack(fill="x", padx=25, pady=(20, 15))
        toolbar_frame.pack_propagate(False)

        # Search section
        search_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        search_frame.pack(side="left", expand=True, fill="both")

        search_label = ctk.CTkLabel(search_frame, text="🔍", font=("Segoe UI", 16), 
                                  text_color=COLOR_TEXT_MUTED)
        search_label.pack(side="left", padx=(0, 10), pady=15)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search History...",
                                       font=FONT_BODY, text_color=COLOR_TEXT_PRIMARY, height=40,
                                       fg_color=COLOR_GRAY_50, border_color=COLOR_GRAY_300,
                                       corner_radius=8)
        self.search_entry.pack(side="left", expand=True, fill="x", pady=15)
        self.search_entry.bind("<KeyRelease>", self.on_search)

        # Filter section
        filter_frame = ctk.CTkFrame(toolbar_frame, fg_color="transparent")
        filter_frame.pack(side="right", padx=(15, 0))

        filter_btn = AnimatedButton(filter_frame, text="🔽 Filter", font=FONT_BODY,
                                  fg_color=COLOR_SECONDARY, hover_color=COLOR_SECONDARY_DARK,
                                  text_color=COLOR_WHITE, corner_radius=8, height=40,
                                  command=self.show_filter_menu)
        filter_btn.pack(pady=15)

    def build_history_feed(self, parent):
        """Build the scrollable history feed"""
        # Feed container
        feed_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        feed_frame.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        # Build history sections
        for date, activities in self.history_data.items():
            self.create_date_section(feed_frame, date, activities)

    def create_date_section(self, parent, date, activities):
        """Create a date section with activities"""
        # Date header
        date_header = ctk.CTkFrame(parent, fg_color="transparent", height=50)
        date_header.pack(fill="x", pady=(15, 10))
        date_header.pack_propagate(False)

        # Date line with decorative elements
        line_frame = ctk.CTkFrame(date_header, fg_color="transparent")
        line_frame.pack(expand=True, fill="both")

        # Left line
        left_line = ctk.CTkFrame(line_frame, fg_color=COLOR_GRAY_300, height=2)
        left_line.pack(side="left", expand=True, fill="x", pady=24)

        # Date label
        date_label = ctk.CTkLabel(line_frame, text=date, font=FONT_H3,
                                text_color=COLOR_TEXT_PRIMARY)
        date_label.pack(side="left", padx=20)

        # Right line
        right_line = ctk.CTkFrame(line_frame, fg_color=COLOR_GRAY_300, height=2)
        right_line.pack(side="right", expand=True, fill="x", pady=24)

        # Activities
        for activity in activities:
            self.create_activity_item(parent, activity)

    def create_activity_item(self, parent, activity):
        """Create an individual activity item"""
        activity_frame = ctk.CTkFrame(parent, fg_color=COLOR_WHITE, corner_radius=10,
                                    border_width=1, border_color=COLOR_GRAY_200)
        activity_frame.pack(fill="x", pady=5)

        # Content container
        content_frame = ctk.CTkFrame(activity_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)

        # Left side - Icon and content
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", expand=True, fill="x")

        # Icon
        icon_label = ctk.CTkLabel(left_frame, text=activity["icon"], font=("Segoe UI", 18))
        icon_label.pack(side="left", padx=(0, 15))

        # Text content
        text_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        text_frame.pack(side="left", expand=True, fill="x")

        # Action label
        action_label = ctk.CTkLabel(text_frame, text=activity["action"], 
                                  font=FONT_H3, text_color=self.get_action_color(activity["type"]),
                                  anchor="w")
        action_label.pack(anchor="w")

        # Description
        desc_label = ctk.CTkLabel(text_frame, text=activity["description"],
                                font=FONT_BODY, text_color=COLOR_TEXT_SECONDARY,
                                anchor="w", wraplength=400)
        desc_label.pack(anchor="w", pady=(2, 0))

        # Right side - Time
        time_label = ctk.CTkLabel(content_frame, text=activity["time"],
                                font=FONT_SMALL, text_color=COLOR_TEXT_MUTED)
        time_label.pack(side="right", anchor="ne")

    def get_action_color(self, action_type):
        """Get color based on action type"""
        color_map = {
            "add": COLOR_ACCENT_SUCCESS,
            "deduct": COLOR_ACCENT_ERROR,
            "update": COLOR_ACCENT_INFO,
            "alert": COLOR_ACCENT_WARNING,
            "remove": COLOR_ACCENT_ERROR
        }
        return color_map.get(action_type, COLOR_TEXT_PRIMARY)

    def on_search(self, event):
        """Handle search functionality"""
        search_term = self.search_entry.get().lower()
        print(f"Searching for: {search_term}")
        # Implement search filtering logic here

    def show_filter_menu(self):
        """Show filter options menu - only if not already open"""
        if self.filter_popup is None or not self.filter_popup.winfo_exists():
            self.filter_popup = FilterPopup(self)
        else:
            # If popup already exists, bring it to front and focus
            self.filter_popup.lift()
            self.filter_popup.focus_set()

    def show_notifications(self):
        """Show notifications"""
        print("Notifications clicked")

    def show_user_menu(self):
        """Show user menu"""
        print("User menu clicked")

    def apply_filters(self, filters):
        """Apply the selected filters to the history data"""
        print("Applying filters:", filters)
        # Implement filtering logic based on the selected options

if __name__ == "__main__":
    app = HistoryLogsPage()
    app.mainloop()