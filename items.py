import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from PIL import Image
from customtkinter import CTkImage

# Colors (Enhanced palette from the inventory code)
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

# Enhanced Fonts with better hierarchy
FONT_H1 = ("Segoe UI", 28, "bold")
FONT_H2 = ("Segoe UI", 20, "bold")
FONT_H3 = ("Segoe UI", 16, "bold")
FONT_BODY = ("Segoe UI", 14)
FONT_SMALL = ("Segoe UI", 12)
FONT_BUTTON = ("Segoe UI", 14, "bold")
FONT_CARD_VALUE = ("Segoe UI", 32, "bold")

# Sample items data with more details
ITEMS_DATA = [
    {
        "item_no": "0001",
        "item_name": "Cooking Oil",
        "image_path": "cooking_oil.png",
        "type": "Staple",
        "unit": "bottle",
        "storage_location": "Pantry",
        "category": "Oils & Fats",
        "supplier": "Golden Oil Co.",
        "description": "Premium cooking oil for all kitchen needs"
    },
    {
        "item_no": "0002", 
        "item_name": "Tomato",
        "image_path": "tomato.png",
        "type": "Fruit",
        "unit": "pieces",
        "storage_location": "Pantry",
        "category": "Vegetables",
        "supplier": "Fresh Farms",
        "description": "Fresh red tomatoes"
    },
    {
        "item_no": "0003",
        "item_name": "Potato",
        "image_path": "potato.png", 
        "type": "Vegetable",
        "unit": "pieces",
        "storage_location": "Pantry",
        "category": "Vegetables",
        "supplier": "Fresh Farms",
        "description": "Quality potatoes for cooking"
    },
    {
        "item_no": "0004",
        "item_name": "Carrot",
        "image_path": "carrot.png",
        "type": "Vegetable",
        "unit": "pieces",
        "storage_location": "Refrigerator",
        "category": "Vegetables",
        "supplier": "Fresh Farms",
        "description": "Fresh orange carrots"
    },
    {
        "item_no": "0005",
        "item_name": "Onion",
        "image_path": "onion.png",
        "type": "Vegetable", 
        "unit": "pieces",
        "storage_location": "Pantry",
        "category": "Vegetables",
        "supplier": "Fresh Farms",
        "description": "Red onions for cooking"
    },
    {
        "item_no": "0006",
        "item_name": "Soy Sauce",
        "image_path": "soy_sauce.png",
        "type": "Condiment",
        "unit": "bottle",
        "storage_location": "Pantry",
        "category": "Condiments",
        "supplier": "Asian Flavors Inc.",
        "description": "Premium soy sauce"
    },
    {
        "item_no": "0007",
        "item_name": "Fish Sauce",
        "image_path": "fish_sauce.png",
        "type": "Condiment",
        "unit": "bottle",
        "storage_location": "Pantry",
        "category": "Condiments",
        "supplier": "Asian Flavors Inc.",
        "description": "Traditional fish sauce"
    },
    {
        "item_no": "0008",
        "item_name": "Ketchup",
        "image_path": "ketchup.png",
        "type": "Condiment",
        "unit": "bottle",
        "storage_location": "Refrigerator",
        "category": "Condiments",
        "supplier": "Condiment Co.",
        "description": "Tomato ketchup"
    },
    {
        "item_no": "0009",
        "item_name": "Sugar",
        "image_path": "sugar.png",
        "type": "Staple",
        "unit": "pack",
        "storage_location": "Pantry",
        "category": "Sweeteners",
        "supplier": "Sweet Supply Co.",
        "description": "White granulated sugar"
    },
    {
        "item_no": "0010",
        "item_name": "Flour",
        "image_path": "flour.png",
        "type": "Staple",
        "unit": "pack",
        "storage_location": "Pantry",
        "category": "Grains",
        "supplier": "Flour Mills Inc.",
        "description": "All-purpose flour"
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
    def __init__(self, master, **kwargs):
        super().__init__(master, width=280, fg_color=COLOR_SAPPHIRE, corner_radius=0, **kwargs)
        self.pack_propagate(False)
        self.active_button = None
        self.setup_ui()
        
    def setup_ui(self):
        logo_frame = ctk.CTkFrame(self, fg_color="transparent", height=100)
        logo_frame.pack(fill="x", pady=(30, 40))
        logo_frame.pack_propagate(False)
        logo_frame.grid_columnconfigure(1, weight=1)

        # Load and place logo image
        try:
            logo_image = Image.open("LOGO2.png")
            logo_ctk = CTkImage(light_image=logo_image, size=(60, 60))
            logo_icon = ctk.CTkLabel(logo_frame, image=logo_ctk, text="")
            logo_icon.grid(row=0, column=0, padx=(20, 0), sticky="w")
        except:
            # Fallback if logo image not found
            logo_icon = ctk.CTkLabel(logo_frame, text="📦", font=("Segoe UI", 40), text_color=COLOR_ROYAL_BLUE)
            logo_icon.grid(row=0, column=0, padx=(20, 0), sticky="w")

        # App name and subtitle next to logo
        text_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        text_frame.grid(row=0, column=1, sticky="w")

        logo_label = ctk.CTkLabel(text_frame, text="StockSmart", font=FONT_H1, text_color=COLOR_ROYAL_BLUE)
        logo_label.pack(anchor="w")

        # Navigation with modern design
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="x", padx=20)

        nav_buttons = [
            ("Dashboard", "🏠", False),
            ("Inventory", "📦", False),
            ("Items", "🏷️", True),  # This is now active
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

class ItemsPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.search_var = ctk.StringVar()
        self.filter_var = ctk.StringVar(value="All")
        self.filtered_data = ITEMS_DATA.copy()
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
        content_container.grid_rowconfigure(3, weight=1)
        
        # Header Label inside content
        header_frame = ctk.CTkFrame(content_container, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=(25, 0))
        header_frame.grid_columnconfigure(0, weight=1)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="Item Management",
            font=FONT_H2,
            text_color=COLOR_TEXT_PRIMARY
        )
        header_label.grid(row=0, column=0, sticky="w")
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Today, May 25, 2025",
            font=FONT_BODY,
            text_color=COLOR_TEXT_MUTED
        )
        subtitle_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
        
        # Add Item button
        add_btn = AnimatedButton(
            header_frame,
            text="+ Add Item",
            font=FONT_BUTTON,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            corner_radius=8,
            height=40,
            width=120,
            command=self.add_item
        )
        add_btn.grid(row=0, column=1, rowspan=2, sticky="e")
        
        # Search and Filter Bar (Updated to match inventory page)
        self.create_search_filter_bar(content_container)
        
        # Category Filter Tabs
        self.create_category_tabs(content_container)
        
        # Items Table
        self.create_items_table(content_container)

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
        
        title_label = ctk.CTkLabel(title_frame, text="Items", 
                                 font=FONT_H1, text_color=COLOR_TEXT_PRIMARY)
        title_label.grid(row=0, column=0, sticky="w", pady=(15, 0))
        
        subtitle = ctk.CTkLabel(title_frame, text="Manage your inventory items and categories", 
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
        user_btn = AnimatedButton(actions_frame, text="👤 User Name ▼", font=FONT_BODY,
                                text_color=COLOR_TEXT_SECONDARY, fg_color=COLOR_CARD_BG,
                                hover_color=COLOR_SIDEBAR_ACTIVE, corner_radius=8, height=50,
                                command=self.show_user_menu)
        user_btn.pack(side="left", padx=10)

    def create_search_filter_bar(self, parent):
        """Create search and filter controls matching inventory page style"""
        filter_frame = ctk.CTkFrame(parent, fg_color="transparent")
        filter_frame.grid(row=1, column=0, sticky="ew", padx=25, pady=(20, 10))
        filter_frame.grid_columnconfigure(1, weight=1)
        
        # Filter dropdown
        filter_label = ctk.CTkLabel(filter_frame, text="Filter:", font=FONT_BODY, text_color=COLOR_TEXT_MUTED)
        filter_label.grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        type_options = ["All", "Fruit", "Vegetable", "Condiment", "Staple"]
        filter_dropdown = ctk.CTkComboBox(
            filter_frame,
            values=type_options,
            variable=self.filter_var,
            font=FONT_BODY,
            dropdown_font=FONT_BODY,
            corner_radius=8,
            border_width=1,
            border_color=COLOR_GRAY_300,
            button_color=COLOR_SECONDARY,
            button_hover_color=COLOR_SECONDARY_DARK,
            dropdown_hover_color=COLOR_SIDEBAR_ACTIVE,
            command=self.apply_filters
        )
        filter_dropdown.grid(row=0, column=1, padx=(0, 20), sticky="w")
        
        # Search entry
        search_label = ctk.CTkLabel(filter_frame, text="Search:", font=FONT_BODY, text_color=COLOR_TEXT_MUTED)
        search_label.grid(row=0, column=2, padx=(0, 10), sticky="w")
        
        search_entry = ctk.CTkEntry(
            filter_frame,
            textvariable=self.search_var,
            placeholder_text="Search items...",
            font=FONT_BODY,
            corner_radius=8,
            border_width=1,
            border_color=COLOR_GRAY_300,
            width=300
        )
        search_entry.grid(row=0, column=3, padx=(0, 10), sticky="ew")
        search_entry.bind("<KeyRelease>", lambda e: self.apply_filters())
        
        # Search button
        search_btn = AnimatedButton(
            filter_frame,
            text="🔍",
            font=("Segoe UI", 16),
            fg_color=COLOR_SECONDARY,
            hover_color=COLOR_SECONDARY_DARK,
            corner_radius=8,
            width=40,
            height=32,
            command=self.apply_filters
        )
        search_btn.grid(row=0, column=4, sticky="w")

    def create_category_tabs(self, parent):
        """Create category filter tabs"""
        tabs_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tabs_frame.grid(row=2, column=0, sticky="ew", padx=25, pady=(10, 20))
        
        categories = ["All", "Fruits", "Vegetables", "Condiments and Sauces", "Staples", "Condiments", "Dairy"]
        self.active_category = "All"
        self.category_buttons = {}
        
        for i, category in enumerate(categories):
            is_active = category == "All"
            
            btn = AnimatedButton(
                tabs_frame,
                text=category,
                font=FONT_BODY,
                fg_color=COLOR_PRIMARY if is_active else "transparent",
                hover_color=COLOR_PRIMARY_HOVER if is_active else COLOR_SIDEBAR_ACTIVE,
                text_color=COLOR_WHITE if is_active else COLOR_TEXT_SECONDARY,
                corner_radius=8,
                height=35,
                border_width=0 if is_active else 1,
                border_color=COLOR_GRAY_300,
                command=lambda c=category: self.set_active_category(c)
            )
            btn.pack(side="left", padx=(0, 10))
            self.category_buttons[category] = btn

    def create_items_table(self, parent):
        """Create the items table with scrollable content"""
        # Table container
        table_container = ctk.CTkFrame(parent, fg_color="transparent")
        table_container.grid(row=3, column=0, sticky="nsew", padx=25, pady=(0, 25))
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)
        
        # Scrollable frame for table
        self.table_scroll = ctk.CTkScrollableFrame(table_container, fg_color="transparent", height=400)
        self.table_scroll.grid(row=0, column=0, sticky="nsew")
        self.table_scroll.grid_columnconfigure(0, weight=1)
        
        # Table header
        self.create_table_header()
        
        # Table rows
        self.create_table_rows()

    def create_table_header(self):
        """Create table header with uniform columns"""
        header_frame = ctk.CTkFrame(self.table_scroll, fg_color=COLOR_SECONDARY, corner_radius=8, height=50)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        header_frame.grid_propagate(False)
        
        # Set column configurations
        header_frame.grid_columnconfigure(0, weight=1, uniform="col1", minsize=80)   # Item No.
        header_frame.grid_columnconfigure(1, weight=2, uniform="col2", minsize=150)  # Item Name
        header_frame.grid_columnconfigure(2, weight=1, uniform="col3", minsize=80)   # Image
        header_frame.grid_columnconfigure(3, weight=1, uniform="col4", minsize=100)  # Type
        header_frame.grid_columnconfigure(4, weight=1, uniform="col5", minsize=80)   # Unit
        header_frame.grid_columnconfigure(5, weight=2, uniform="col6", minsize=120)  # Storage Location
        
        headers = ["Item No.", "Item Name", "Image", "Type", "Unit", "Storage Location"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(weight="bold", size=14),
                text_color=COLOR_WHITE
            )
            header_label.grid(row=0, column=i, padx=8, pady=15, sticky="nsew")

    def create_table_rows(self):
        """Create table rows based on filtered data"""
        # Clear existing rows
        for widget in self.table_scroll.winfo_children()[1:]:  # Skip header
            widget.destroy()
        
        for i, item in enumerate(self.filtered_data):
            self.create_table_row(item, i + 1)

    def create_table_row(self, item, row_index):
        """Create a single table row"""
        row_color = COLOR_WHITE if row_index % 2 == 0 else COLOR_GRAY_50
        row_frame = ctk.CTkFrame(self.table_scroll, fg_color=row_color, corner_radius=8, height=60)
        row_frame.grid(row=row_index, column=0, sticky="ew", pady=2)
        row_frame.grid_propagate(False)
        
        # Use same column configuration as header
        row_frame.grid_columnconfigure(0, weight=1, uniform="col1", minsize=80)   # Item No.
        row_frame.grid_columnconfigure(1, weight=2, uniform="col2", minsize=150)  # Item Name
        row_frame.grid_columnconfigure(2, weight=1, uniform="col3", minsize=80)   # Image
        row_frame.grid_columnconfigure(3, weight=1, uniform="col4", minsize=100)  # Type
        row_frame.grid_columnconfigure(4, weight=1, uniform="col5", minsize=80)   # Unit
        row_frame.grid_columnconfigure(5, weight=2, uniform="col6", minsize=120)  # Storage Location
        
        data = [
            item["item_no"],
            item["item_name"],
            "🖼️",  # Placeholder for image
            item["type"],
            item["unit"],
            item["storage_location"]
        ]
        
        for i, cell_data in enumerate(data):
            if i == 2:  # Image column
                image_label = ctk.CTkLabel(
                    row_frame,
                    text=cell_data,
                    font=("Segoe UI", 20),
                    text_color=COLOR_TEXT_SECONDARY
                )
                image_label.grid(row=0, column=i, padx=8, pady=10, sticky="nsew")
            else:
                cell_label = ctk.CTkLabel(
                    row_frame,
                    text=cell_data,
                    font=FONT_BODY,
                    text_color=COLOR_TEXT_PRIMARY,
                    anchor="w" if i == 1 else "center"  # Left align item names, center others
                )
                cell_label.grid(row=0, column=i, padx=8, pady=10, sticky="nsew")

    def set_active_category(self, category):
        """Set active category and update button styles"""
        # Reset all buttons
        for cat, btn in self.category_buttons.items():
            is_active = cat == category
            btn.configure(
                fg_color=COLOR_PRIMARY if is_active else "transparent",
                hover_color=COLOR_PRIMARY_HOVER if is_active else COLOR_SIDEBAR_ACTIVE,
                text_color=COLOR_WHITE if is_active else COLOR_TEXT_SECONDARY,
                border_width=0 if is_active else 1
            )
        
        self.active_category = category
        self.apply_filters()

    def apply_filters(self):
        """Apply search and filter to items data"""
        search_term = self.search_var.get().lower()
        filter_type = self.filter_var.get()
        
        self.filtered_data = []
        
        for item in ITEMS_DATA:
            # Apply type filter
            if filter_type != "All" and item["type"] != filter_type:
                continue
            
            # Apply category filter from tabs
            if self.active_category != "All":
                if self.active_category == "Condiments and Sauces" and item["type"] != "Condiment":
                    continue
                elif self.active_category == "Fruits" and item["type"] != "Fruit":
                    continue
                elif self.active_category == "Vegetables" and item["type"] != "Vegetable":
                    continue
                elif self.active_category == "Staples" and item["type"] != "Staple":
                    continue
                elif self.active_category in ["Condiments", "Dairy"] and item["type"] != self.active_category.rstrip('s'):
                    continue
            
            # Apply search filter
            if search_term and search_term not in item["item_name"].lower():
                continue
            
            self.filtered_data.append(item)
        
        # Recreate table rows
        self.create_table_rows()

    def add_item(self):
        """Add new item dialog"""
        messagebox.showinfo("Add Item", "Add new item dialog coming soon!")

    def show_notifications(self):
        """Show notifications dialog"""
        messagebox.showinfo("Notifications", "You have 3 low stock alerts!")

    def show_user_menu(self):
        """Show user menu"""
        messagebox.showinfo("User Menu", "User menu options coming soon!")


class ItemsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("StockSmart - Items Management")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        self.configure(bg=COLOR_MAIN_BG)
        
        self.setup_ui()

    def setup_ui(self):
        # Modern sidebar
        self.sidebar = ModernSidebar(self)
        self.sidebar.pack(side="left", fill="y")

        # Main items page
        self.items_page = ItemsPage(self)
        self.items_page.pack(side="left", fill="both", expand=True)


# Test the items page with sidebar
if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    
    app = ItemsApp()
    app.mainloop()