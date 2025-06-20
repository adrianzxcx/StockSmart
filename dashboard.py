import customtkinter as ctk
from tkinter import PhotoImage
import json
import os
from tkcalendar import Calendar
import threading
import time
from tkinter import filedialog, messagebox
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

# Sample inventory data
INVENTORY_DATA = [
    {
        "item_no": "001",
        "item_name": "Cooking Oil",
        "image_path": "cooking_oil.png",
        "quantity": 25,
        "unit": "Liters",
        "last_updated": "2025-06-20",
        "status": "Good",
        "price": 45.00,
        "supplier": "Golden Oil Co.",
        "category": "Oils & Fats"
    },
    {
        "item_no": "002", 
        "item_name": "Fresh Tomatoes",
        "image_path": "tomato.png",
        "quantity": 8,
        "unit": "kg",
        "last_updated": "2025-06-19",
        "status": "Low Stock",
        "price": 120.00,
        "supplier": "Fresh Farms",
        "category": "Vegetables"
    },
    {
        "item_no": "003",
        "item_name": "Soy Sauce",
        "image_path": "soy_sauce.png", 
        "quantity": 0,
        "unit": "Bottles",
        "last_updated": "2025-06-18",
        "status": "Out of Stock",
        "price": 35.00,
        "supplier": "Asian Flavors Inc.",
        "category": "Condiments"
    },
    {
        "item_no": "004",
        "item_name": "Rice",
        "image_path": "rice.png",
        "quantity": 50,
        "unit": "kg",
        "last_updated": "2025-06-21",
        "status": "Good",
        "price": 85.00,
        "supplier": "Rice Masters",
        "category": "Grains"
    },
    {
        "item_no": "005",
        "item_name": "Garlic",
        "image_path": "garlic.png",
        "quantity": 3,
        "unit": "kg", 
        "last_updated": "2025-06-20",
        "status": "Low Stock",
        "price": 200.00,
        "supplier": "Spice World",
        "category": "Spices"
    },
    {
        "item_no": "006",
        "item_name": "Sugar",
        "image_path": "sugar.png",
        "quantity": 12,
        "unit": "kg",
        "last_updated": "2025-06-19",
        "status": "Good",
        "price": 60.00,
        "supplier": "Sweet Supply Co.",
        "category": "Sweeteners"
    }
]

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
    def __init__(self, master, main_app, **kwargs):
        super().__init__(master, width=280, fg_color=COLOR_SAPPHIRE, corner_radius=0, **kwargs)
        self.pack_propagate(False)
        self.main_app = main_app
        self.active_button = None
        self.nav_buttons = {}
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

        nav_items = [
            ("Dashboard", "🏠"),
            ("Inventory", "📦"),
            ("Items", "🏷️"),
            ("History Logs", "📋")
        ]

        for name, icon in nav_items:
            btn = self.create_nav_button(nav_frame, name, icon)
            btn.pack(fill="x", pady=5)
            self.nav_buttons[name] = btn
            
        # Set initial active page
        self.set_active("Dashboard")
            
        # User section at bottom
        user_frame = ctk.CTkFrame(self, fg_color=COLOR_SECONDARY_DARK, corner_radius=12, height=80)
        user_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        user_frame.pack_propagate(False)
        
        user_info = ctk.CTkLabel(user_frame, text="👤 Mingyu Kim\nOwner", 
                               font=FONT_SMALL, text_color=COLOR_WHITE, justify="left")
        user_info.pack(expand=True, padx=15)

    def create_nav_button(self, parent, name, icon):
        btn = ctk.CTkButton(parent, text=f"{icon}  {name}", font=FONT_BUTTON,
                           text_color=COLOR_ROYAL_BLUE, fg_color="transparent",
                           hover_color=COLOR_SECONDARY_LIGHT, corner_radius=10, height=50,
                           anchor="w", command=lambda n=name: self.set_active(n))
        return btn
        
    def set_active(self, name):
        # Reset all buttons
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == name:
                btn.configure(fg_color=COLOR_SECONDARY_DARK, text_color=COLOR_WHITE)
                self.active_button = btn
            else:
                btn.configure(fg_color="transparent", text_color=COLOR_ROYAL_BLUE)
        
        # Switch page in main app
        self.main_app.switch_page(name)

class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.setup_ui()
        
    def setup_ui(self):
        self.configure(fg_color=COLOR_MAIN_BG, corner_radius=0)
        
        # Header
        self.build_header()
        
        # Main content with scrollable frame
        main_content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Statistics Cards
        self.build_stats_cards(main_content)
        
        # Charts Section
        self.build_charts_section(main_content)
        
        # Recent Activity
        self.build_recent_activity(main_content)

    def build_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        header_frame.pack(fill="x", padx=30, pady=(20, 0))
        header_frame.pack_propagate(False)

        # Title section
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", expand=True, fill="both")
        
        title_label = ctk.CTkLabel(title_frame, text="🏠 Dashboard", 
                                 font=FONT_H1, text_color=COLOR_TEXT_PRIMARY)
        title_label.pack(anchor="w", pady=(15, 0))
        
        current_date = datetime.now().strftime("%B %d, %Y")
        subtitle = ctk.CTkLabel(title_frame, text=f"Welcome back, Mingyu! Today is {current_date}", 
                              font=FONT_BODY, text_color=COLOR_TEXT_MUTED)
        subtitle.pack(anchor="w")

        # Actions section
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.pack(side="right")

        # Quick Add Button
        add_btn = AnimatedButton(
            actions_frame,
            text="➕ Add Item",
            font=FONT_BUTTON,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            corner_radius=8,
            height=40,
            command=self.quick_add_item
        )
        add_btn.pack(side="left", padx=10)

        # User dropdown
        user_btn = AnimatedButton(actions_frame, text="👤 Mingyu Kim ▼", font=FONT_BODY,
                                text_color=COLOR_TEXT_SECONDARY, fg_color=COLOR_CARD_BG,
                                hover_color=COLOR_SIDEBAR_ACTIVE, corner_radius=8, height=40,
                                command=self.show_user_menu)
        user_btn.pack(side="left", padx=10)

    def build_stats_cards(self, parent):
        stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Calculate statistics
        total_items = len(INVENTORY_DATA)
        low_stock = len([item for item in INVENTORY_DATA if item["status"] == "Low Stock"])
        out_of_stock = len([item for item in INVENTORY_DATA if item["status"] == "Out of Stock"])
        total_value = sum(item["quantity"] * item["price"] for item in INVENTORY_DATA)
        
        stats_data = [
            ("Total Items", str(total_items), "📦", COLOR_PRIMARY),
            ("Low Stock", str(low_stock), "⚠️", COLOR_ACCENT_WARNING),
            ("Out of Stock", str(out_of_stock), "🚫", COLOR_ACCENT_ERROR),
            ("Total Value", f"₱{total_value:,.2f}", "💰", COLOR_ACCENT_SUCCESS)
        ]
        
        for i, (title, value, icon, color) in enumerate(stats_data):
            card = self.create_stat_card(stats_frame, title, value, icon, color)
            card.grid(row=0, column=i, padx=10, sticky="ew")
            stats_frame.grid_columnconfigure(i, weight=1)

    def create_stat_card(self, parent, title, value, icon, color):
        card = ctk.CTkFrame(parent, fg_color=COLOR_CARD_BG, corner_radius=12, height=120)
        card.grid_propagate(False)
        
        # Icon
        icon_label = ctk.CTkLabel(card, text=icon, font=("Segoe UI", 24))
        icon_label.pack(pady=(15, 5))
        
        # Value
        value_label = ctk.CTkLabel(card, text=value, font=FONT_CARD_VALUE, text_color=color)
        value_label.pack()
        
        # Title
        title_label = ctk.CTkLabel(card, text=title, font=FONT_SMALL, text_color=COLOR_TEXT_MUTED)
        title_label.pack(pady=(0, 15))
        
        return card

    def build_charts_section(self, parent):
        charts_frame = ctk.CTkFrame(parent, fg_color="transparent")
        charts_frame.pack(fill="x", pady=(0, 20))
        
        # Mock chart - Inventory by Category
        chart_card = ctk.CTkFrame(charts_frame, fg_color=COLOR_CARD_BG, corner_radius=12)
        chart_card.pack(fill="x", pady=10)
        
        chart_title = ctk.CTkLabel(chart_card, text="📊 Inventory by Category", 
                                 font=FONT_H3, text_color=COLOR_TEXT_PRIMARY)
        chart_title.pack(pady=(20, 10))
        
        # Simple text-based chart representation
        categories = {}
        for item in INVENTORY_DATA:
            cat = item.get("category", "Other")
            categories[cat] = categories.get(cat, 0) + 1
        
        for category, count in categories.items():
            cat_frame = ctk.CTkFrame(chart_card, fg_color="transparent")
            cat_frame.pack(fill="x", padx=20, pady=5)
            
            cat_label = ctk.CTkLabel(cat_frame, text=f"{category}: {count} items", 
                                   font=FONT_BODY, text_color=COLOR_TEXT_PRIMARY)
            cat_label.pack(side="left")
            
            # Progress bar representation
            progress = ctk.CTkProgressBar(cat_frame, width=200, height=10)
            progress.pack(side="right", padx=(10, 0))
            progress.set(count / total_items if total_items > 0 else 0)
        
        # Add some padding at bottom
        ctk.CTkLabel(chart_card, text="", height=20).pack()

    def build_recent_activity(self, parent):
        activity_frame = ctk.CTkFrame(parent, fg_color=COLOR_CARD_BG, corner_radius=12)
        activity_frame.pack(fill="x", pady=10)
        
        activity_title = ctk.CTkLabel(activity_frame, text="📋 Recent Activity", 
                                    font=FONT_H3, text_color=COLOR_TEXT_PRIMARY)
        activity_title.pack(pady=(20, 10))
        
        # Sample recent activities
        recent_activities = [
            ("➕", "Added 9 stocks of Cooking Oil", "10 mins ago"),
            ("➖", "Deducted 3 stocks of Fresh Onions", "25 mins ago"),
            ("✏️", "Updated price of Tomatoes", "1 hour ago"),
            ("🆕", "Added Organic Quinoa to inventory", "2 hours ago")
        ]
        
        for icon, description, time in recent_activities:
            activity_item = ctk.CTkFrame(activity_frame, fg_color="transparent")
            activity_item.pack(fill="x", padx=20, pady=5)
            
            icon_label = ctk.CTkLabel(activity_item, text=icon, font=("Segoe UI", 16))
            icon_label.pack(side="left", padx=(0, 10))
            
            desc_label = ctk.CTkLabel(activity_item, text=description, 
                                    font=FONT_BODY, text_color=COLOR_TEXT_PRIMARY)
            desc_label.pack(side="left")
            
            time_label = ctk.CTkLabel(activity_item, text=time, 
                                    font=FONT_SMALL, text_color=COLOR_TEXT_MUTED)
            time_label.pack(side="right")
        
        # Add some padding at bottom
        ctk.CTkLabel(activity_frame, text="", height=20).pack()

    def quick_add_item(self):
        messagebox.showinfo("Quick Add", "Quick Add Item feature coming soon!")

    def show_user_menu(self):
        messagebox.showinfo("User Menu", "User menu options coming soon!")

class ItemsPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.setup_ui()

    def setup_ui(self):
        self.configure(fg_color=COLOR_MAIN_BG, corner_radius=0)
        
        # Header
        self.build_header()
        
        # Main content
        main_content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Items grid
        self.build_items_grid(main_content)

    def build_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        header_frame.pack(fill="x", padx=30, pady=(20, 0))
        header_frame.pack_propagate(False)

        # Title section
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", expand=True, fill="both")
        
        title_label = ctk.CTkLabel(title_frame, text="🏷️ Items", 
                                 font=FONT_H1, text_color=COLOR_TEXT_PRIMARY)
        title_label.pack(anchor="w", pady=(15, 0))
        
        subtitle = ctk.CTkLabel(title_frame, text="Manage individual items and their details", 
                              font=FONT_BODY, text_color=COLOR_TEXT_MUTED)
        subtitle.pack(anchor="w")

        # Actions section
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.pack(side="right")

        # Add New Item Button
        add_btn = AnimatedButton(
            actions_frame,
            text="➕ Add New Item",
            font=FONT_BUTTON,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            corner_radius=8,
            height=40,
            command=self.add_new_item
        )
        add_btn.pack(side="left", padx=10)

        # User dropdown
        user_btn = AnimatedButton(actions_frame, text="👤 Mingyu Kim ▼", font=FONT_BODY,
                                text_color=COLOR_TEXT_SECONDARY, fg_color=COLOR_CARD_BG,
                                hover_color=COLOR_SIDEBAR_ACTIVE, corner_radius=8, height=40,
                                command=self.show_user_menu)
        user_btn.pack(side="left", padx=10)

    def build_items_grid(self, parent):
        # Grid container
        grid_frame = ctk.CTkFrame(parent, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        
        # Configure grid columns
        for i in range(3):  # 3 columns
            grid_frame.grid_columnconfigure(i, weight=1)
        
        # Create item cards
        for i, item in enumerate(INVENTORY_DATA):
            row = i // 3
            col = i % 3
            
            item_card = self.create_item_card(grid_frame, item)
            item_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def create_item_card(self, parent, item):
        card = ctk.CTkFrame(parent, fg_color=COLOR_CARD_BG, corner_radius=12)
        
        # Item emoji/icon
        emoji_map = {
            "Cooking Oil": "🛢️",
            "Fresh Tomatoes": "🍅", 
            "Soy Sauce": "🍶",
            "Rice": "🌾",
            "Garlic": "🧄",
            "Sugar": "🧂"
        }
        item_emoji = emoji_map.get(item["item_name"], "📦")
        
        # Icon
        icon_frame = ctk.CTkFrame(card, fg_color=COLOR_PRIMARY, corner_radius=50, width=80, height=80)
        icon_frame.pack(pady=(20, 10))
        icon_frame.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(icon_frame, text=item_emoji, font=("Segoe UI", 32))
        icon_label.pack(expand=True)
        
        # Item name
        name_label = ctk.CTkLabel(card, text=item["item_name"], 
                                font=FONT_H3, text_color=COLOR_TEXT_PRIMARY)
        name_label.pack(pady=(0, 5))
        
        # Item details
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(fill="x", padx=20, pady=10)
        
        # Quantity
        qty_label = ctk.CTkLabel(details_frame, text=f"Qty: {item['quantity']} {item['unit']}", 
                               font=FONT_BODY, text_color=COLOR_TEXT_SECONDARY)
        qty_label.pack()
        
        # Price
        price_label = ctk.CTkLabel(details_frame, text=f"₱{item['price']:.2f}", 
                                 font=FONT_BODY, text_color=COLOR_TEXT_SECONDARY)
        price_label.pack()
        
        # Status
        status_colors = {
            "Good": COLOR_ACCENT_SUCCESS,
            "Low Stock": COLOR_ACCENT_WARNING,
            "Out of Stock": COLOR_ACCENT_ERROR
        }
        
        status_label = ctk.CTkLabel(details_frame, text=item["status"], 
                                  font=ctk.CTkFont(weight="bold", size=12),
                                  text_color=status_colors.get(item["status"], COLOR_TEXT_PRIMARY))
        status_label.pack(pady=(5, 0))
        
        # Action buttons
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        edit_btn = AnimatedButton(button_frame, text="Edit", font=FONT_SMALL,
                                fg_color=COLOR_SECONDARY, hover_color=COLOR_SECONDARY_DARK,
                                corner_radius=6, height=30,
                                command=lambda: self.edit_item(item))
        edit_btn.pack(side="left", padx=(0, 5), fill="x", expand=True)
        
        delete_btn = AnimatedButton(button_frame, text="Delete", font=FONT_SMALL,
                                  fg_color=COLOR_ACCENT_ERROR, hover_color="#5a1f1f",
                                  corner_radius=6, height=30,
                                  command=lambda: self.delete_item(item))
        delete_btn.pack(side="right", padx=(5, 0), fill="x", expand=True)
        
        return card

    def add_new_item(self):
        messagebox.showinfo("Add Item", "Add new item dialog coming soon!")

    def edit_item(self, item):
        messagebox.showinfo("Edit Item", f"Edit {item['item_name']} dialog coming soon!")

    def delete_item(self, item):
        result = messagebox.askyesno("Delete Item", f"Are you sure you want to delete {item['item_name']}?")
        if result:
            messagebox.showinfo("Deleted", f"{item['item_name']} has been deleted!")

    def show_user_menu(self):
        messagebox.showinfo("User Menu", "User menu options coming soon!")

class InventoryPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.search_var = ctk.StringVar()
        self.filter_var = ctk.StringVar(value="All")
        self.filtered_data = INVENTORY_DATA.copy()
        self.setup_ui()
        
    def setup_ui(self):
        # Main Content Area Frame
        self.configure(fg_color=COLOR_MAIN_BG, corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Header with title and user info
        self.build_header()
        
        # Content container
        content_container = ctk.CTkFrame(self, corner_radius=16, fg_color=COLOR_CARD_BG,
                                       border_width=1, border_color=COLOR_GRAY_200)
        content_container.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        content_container.grid_columnconfigure(0, weight=1)
        content_container.grid_rowconfigure(2, weight=1)
        
        # Header Label inside content
        header_label = ctk.CTkLabel(
            content_container,
            text="📦 Inventory Overview",
            font=FONT_H2,
            text_color=COLOR_TEXT_PRIMARY
        )
        header_label.grid(row=0, column=0, pady=(25, 20), padx=25, sticky="nw")
        
        # Search and Filter Bar
        self.create_search_filter_bar(content_container)
        
        # Inventory Table
        self.create_inventory_table(content_container)

    def build_header(self):
        """Build the header section with title and user info"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 0))
        header_frame.pack_propagate(False)
        header_frame.grid_columnconfigure(0, weight=1)

        # Title section
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(title_frame, text="📦 Inventory", 
                                 font=FONT_H1, text_color=COLOR_TEXT_PRIMARY)
        title_label.grid(row=0, column=0, sticky="w", pady=(15, 0))
        
        subtitle = ctk.CTkLabel(title_frame, text="Manage your inventory items and stock levels", 
                              font=FONT_BODY, text_color=COLOR_TEXT_MUTED)
        subtitle.grid(row=1, column=0, sticky="w")

        # Actions section
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=1, sticky="e")

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
                                command=