import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from PIL import Image
from customtkinter import CTkImage

# Colors (Enhanced palette from the second file)
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
        logo_image = Image.open("LOGO2.png")
        logo_ctk = CTkImage(light_image=logo_image, size=(60, 60))
        logo_icon = ctk.CTkLabel(logo_frame, image=logo_ctk, text="")
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
            ("Inventory", "📦", True),  # This is now active
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
        
        
        title_label = ctk.CTkLabel(title_frame, text=" Inventory", 
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
                                command=self.show_user_menu)
        user_btn.pack(side="left", padx=10)

    def create_search_filter_bar(self, parent):
        """Create search and filter controls"""
        filter_frame = ctk.CTkFrame(parent, fg_color="transparent")
        filter_frame.grid(row=1, column=0, sticky="ew", padx=25, pady=(0, 20))
        filter_frame.grid_columnconfigure(1, weight=1)
        
        # Filter dropdown
        filter_label = ctk.CTkLabel(filter_frame, text="Filter:", font=FONT_BODY, text_color=COLOR_TEXT_MUTED)
        filter_label.grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        status_options = ["All", "Good", "Low Stock", "Out of Stock"]
        filter_dropdown = ctk.CTkComboBox(
            filter_frame,
            values=status_options,
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

    def create_inventory_table(self, parent):
        """Create the inventory table with scrollable content"""
        # Table container
        table_container = ctk.CTkFrame(parent, fg_color="transparent")
        table_container.grid(row=2, column=0, sticky="nsew", padx=25, pady=(0, 25))
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)
        
        # Scrollable frame for table
        self.table_scroll = ctk.CTkScrollableFrame(table_container, fg_color="transparent", height=450)
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
        
        # Set column configurations with different weights for better text visibility
        header_frame.grid_columnconfigure(0, weight=1, uniform="col1", minsize=80)   # Item No.
        header_frame.grid_columnconfigure(1, weight=2, uniform="col2", minsize=150)  # Item Name (wider)
        header_frame.grid_columnconfigure(2, weight=1, uniform="col3", minsize=80)   # Quantity
        header_frame.grid_columnconfigure(3, weight=1, uniform="col4", minsize=60)   # Unit
        header_frame.grid_columnconfigure(4, weight=1, uniform="col5", minsize=80)   # Price
        header_frame.grid_columnconfigure(5, weight=1, uniform="col6", minsize=100)  # Status
        header_frame.grid_columnconfigure(6, weight=1, uniform="col7", minsize=100)  # Last Updated
        header_frame.grid_columnconfigure(7, weight=2, uniform="col8", minsize=180)  # Actions (wider for buttons)
        
        headers = ["Item No.", "Item Name", "Quantity", "Unit", "Price", "Status", "Last Updated", "Actions"]
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
        """Create a single table row with uniform columns and improved action buttons"""
        row_color = COLOR_WHITE if row_index % 2 == 0 else COLOR_GRAY_50
        row_frame = ctk.CTkFrame(self.table_scroll, fg_color=row_color, corner_radius=8, height=60)
        row_frame.grid(row=row_index, column=0, sticky="ew", pady=2)
        row_frame.grid_propagate(False)
        
        # Use same column configuration as header for consistency
        row_frame.grid_columnconfigure(0, weight=1, uniform="col1", minsize=80)   # Item No.
        row_frame.grid_columnconfigure(1, weight=2, uniform="col2", minsize=150)  # Item Name (wider)
        row_frame.grid_columnconfigure(2, weight=1, uniform="col3", minsize=80)   # Quantity
        row_frame.grid_columnconfigure(3, weight=1, uniform="col4", minsize=60)   # Unit
        row_frame.grid_columnconfigure(4, weight=1, uniform="col5", minsize=80)   # Price
        row_frame.grid_columnconfigure(5, weight=1, uniform="col6", minsize=100)  # Status
        row_frame.grid_columnconfigure(6, weight=1, uniform="col7", minsize=100)  # Last Updated
        row_frame.grid_columnconfigure(7, weight=2, uniform="col8", minsize=180)  # Actions (wider for buttons)
        
        data = [
            item["item_no"],
            item["item_name"],
            str(item["quantity"]),
            item["unit"],
            f"₱{item['price']:.2f}",
            item["status"],
            item["last_updated"],
            ""  # Actions column
        ]
        
        status_colors = {
            "Good": COLOR_ACCENT_SUCCESS,
            "Low Stock": COLOR_ACCENT_WARNING,
            "Out of Stock": COLOR_ACCENT_ERROR
        }
        
        for i, cell_data in enumerate(data[:-1]):  # Exclude actions for now
            if i == 5:  # Status column
                status_label = ctk.CTkLabel(
                    row_frame,
                    text=cell_data,
                    font=ctk.CTkFont(weight="bold", size=12),
                    text_color=status_colors.get(cell_data, COLOR_TEXT_PRIMARY)
                )
                status_label.grid(row=0, column=i, padx=8, pady=10, sticky="nsew")
            else:
                cell_label = ctk.CTkLabel(
                    row_frame,
                    text=cell_data,
                    font=FONT_BODY,
                    text_color=COLOR_TEXT_PRIMARY,
                    anchor="w" if i == 1 else "center"  # Left align item names, center others
                )
                cell_label.grid(row=0, column=i, padx=8, pady=10, sticky="nsew")
        
        # Actions column with improved uniform button layout
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=7, padx=8, pady=8, sticky="nsew")
        
        # Create a centered container for buttons
        button_container = ctk.CTkFrame(actions_frame, fg_color="transparent")
        button_container.pack(expand=True)
        
        # Button configuration
        btn_width = 36
        btn_height = 36
        btn_spacing = 4
        
        # Edit button
        edit_btn = AnimatedButton(
            button_container,
            text="📝",
            font=("Segoe UI", 14),
            fg_color=COLOR_SECONDARY,
            hover_color=COLOR_SECONDARY_DARK,
            text_color=COLOR_WHITE,
            corner_radius=8,
            width=btn_width,
            height=btn_height,
            border_width=0,
            command=lambda: self.edit_item(item)
        )
        edit_btn.pack(side="left", padx=(0, btn_spacing))

        # Delete button
        delete_btn = AnimatedButton(
            button_container,
            text="🗑",
            font=("Segoe UI", 14),
            fg_color=COLOR_ACCENT_ERROR,
            hover_color="#5a1f1f",
            text_color=COLOR_WHITE,
            corner_radius=8,
            width=btn_width,
            height=btn_height,
            border_width=0,
            command=lambda: self.delete_item(item)
        )
        delete_btn.pack(side="left", padx=(0, btn_spacing))

        if item["quantity"] > 0:
            minus_btn = AnimatedButton(
                button_container,
                text="➖",
                font=("Segoe UI", 14),
                fg_color=COLOR_ACCENT_WARNING,
                hover_color="#6b5410",
                text_color=COLOR_WHITE,
                corner_radius=8,
                width=btn_width,
                height=btn_height,
                border_width=0,
                command=lambda: self.adjust_stock(item, -1)
            )
            minus_btn.pack(side="left", padx=(0, btn_spacing))

        plus_btn = AnimatedButton(
            button_container,
            text="➕",
            font=("Segoe UI", 14),
            fg_color=COLOR_ACCENT_SUCCESS,
            hover_color="#1f3f1c",
            text_color=COLOR_WHITE,
            corner_radius=8,
            width=btn_width,
            height=btn_height,
            border_width=0,
            command=lambda: self.adjust_stock(item, 1)
        )
        plus_btn.pack(side="left", padx=(0, btn_spacing))

    def apply_filters(self):
        """Apply search and filter to inventory data"""
        search_term = self.search_var.get().lower()
        filter_status = self.filter_var.get()
        
        self.filtered_data = []
        
        for item in INVENTORY_DATA:
            # Apply status filter
            if filter_status != "All" and item["status"] != filter_status:
                continue
            
            # Apply search filter
            if search_term and search_term not in item["item_name"].lower():
                continue
            
            self.filtered_data.append(item)
        
        # Recreate table rows
        self.create_table_rows()

    def edit_item(self, item):
        """Edit item dialog"""
        messagebox.showinfo("Edit Item", f"Edit {item['item_name']} dialog coming soon!")

    def delete_item(self, item):
        """Delete item with confirmation"""
        result = messagebox.askyesno("Delete Item", f"Are you sure you want to delete {item['item_name']}?")
        if result:
            # Remove from data
            INVENTORY_DATA.remove(item)
            self.apply_filters()  # Refresh table
            messagebox.showinfo("Deleted", f"{item['item_name']} has been deleted!")

    def adjust_stock(self, item, adjustment):
        """Adjust stock quantity"""
        new_quantity = max(0, item["quantity"] + adjustment)
        item["quantity"] = new_quantity
        
        # Update status based on new quantity
        if new_quantity == 0:
            item["status"] = "Out of Stock"
        elif new_quantity <= 5:  # Low stock threshold
            item["status"] = "Low Stock"
        else:
            item["status"] = "Good"
        
        # Update last updated date
        item["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        
        # Refresh table
        self.apply_filters()
        
        action = "Added" if adjustment > 0 else "Removed"
        messagebox.showinfo("Stock Updated", f"{action} {abs(adjustment)} unit(s) from {item['item_name']}")

    def show_notifications(self):
        """Show notifications dialog"""
        messagebox.showinfo("Notifications", "You have 3 low stock alerts!")

    def show_user_menu(self):
        """Show user menu"""
        messagebox.showinfo("User Menu")


class InventoryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("StockSmart - Inventory Management")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        self.configure(bg=COLOR_MAIN_BG)
        
        self.setup_ui()

    def setup_ui(self):
        # Modern sidebar
        self.sidebar = ModernSidebar(self)
        self.sidebar.pack(side="left", fill="y")

        # Main inventory page
        self.inventory_page = InventoryPage(self)
        self.inventory_page.pack(side="left", fill="both", expand=True)


# Test the inventory page with sidebar
if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    
    app = InventoryApp()
    app.mainloop()