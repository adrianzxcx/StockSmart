import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

app = ctk.CTk()
app.geometry("800x600")
app.title("Add Item")
app.resizable(False, False)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app.configure(fg_color="#F9F5EB")
app.grid_columnconfigure(0, weight=2)  
app.grid_columnconfigure(1, weight=3)

# Configure main app grid
app.grid_rowconfigure(0, weight=1)

# Global variable to store the selected image path
selected_image_path = None

def browse_file():
    """Function to handle file browsing and image display"""
    global selected_image_path
    
    # Open file dialog
    file_path = filedialog.askopenfilename(
        title="Select Image File",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("All files", "*.*")
        ],
        initialdir=os.getcwd()
    )
    
    if file_path:
        try:
            # Store the selected image path
            selected_image_path = file_path
            
            # Load and resize the image
            image = Image.open(file_path)
            
            # Calculate the size to fit within the frame while maintaining aspect ratio
            frame_width = 260  # Slightly smaller than frame width to account for padding
            frame_height = 130  # Slightly smaller than frame height
            
            # Calculate scaling factor
            width_ratio = frame_width / image.width
            height_ratio = frame_height / image.height
            scale_factor = min(width_ratio, height_ratio)
            
            # Calculate new dimensions
            new_width = int(image.width * scale_factor)
            new_height = int(image.height * scale_factor)
            
            # Resize the image
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(resized_image)
            
            # Update the image label
            image_label.configure(image=photo, text="")
            image_label.image = photo  # Keep a reference to prevent garbage collection
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
            print(f"Error loading image: {e}")

def get_selected_image_path():
    """Function to get the currently selected image path"""
    return selected_image_path

def validate_and_add_item():
    """Function to validate form data and add the item"""
    # Get all form values
    item_name = item_name_entry.get().strip()
    item_type = type_dropdown.get()
    quantity = quantity_entry.get().strip()
    unit = unit_dropdown.get()
    storage = storage_dropdown.get()
    brand = brand_entry.get().strip()
    expiry = expiry_entry.get().strip()
    supplier = supplier_entry.get().strip()
    contact_person = contact_person_entry.get().strip()
    contact_number = contact_number_entry.get().strip()
    email = email_entry.get().strip()
    
    # Basic validation
    if not item_name:
        messagebox.showerror("Validation Error", "Item Name is required!")
        return
    
    if not item_type:
        messagebox.showerror("Validation Error", "Type is required!")
        return
    
    if not quantity:
        messagebox.showerror("Validation Error", "Quantity is required!")
        return
    
    try:
        float(quantity)  # Check if quantity is a valid number
    except ValueError:
        messagebox.showerror("Validation Error", "Quantity must be a valid number!")
        return
    
    if not unit:
        messagebox.showerror("Validation Error", "Unit is required!")
        return
    
    if not storage:
        messagebox.showerror("Validation Error", "Storage Location is required!")
        return
    
    # If validation passes, show success message
    messagebox.showinfo("Success", f"Item '{item_name}' has been added successfully!")
    
    # Here you would typically save the data to a database or file
    # For now, we'll just print the collected data
    print(f"Added Item: {item_name}, Type: {item_type}, Quantity: {quantity} {unit}")
    print(f"Storage: {storage}, Brand: {brand}, Expiry: {expiry}")
    print(f"Supplier: {supplier}, Contact: {contact_person}, Phone: {contact_number}, Email: {email}")
    print(f"Image: {selected_image_path}")

# Left frame
left_frame = ctk.CTkFrame(master=app, fg_color="#F9F5EB")
left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
left_frame.grid_columnconfigure(0, weight=1)

# Right frame
right_frame = ctk.CTkFrame(master=app, fg_color="#F9F5EB")
right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
right_frame.grid_columnconfigure(0, weight=1)

# Title
title = ctk.CTkLabel(
    left_frame,
    text="Add Item",
    font=ctk.CTkFont(family="Instrument Sans", size=25, weight="bold"),
    text_color="#112250"
)
title.grid(row=0, column=0, sticky="w", padx=(10,0), pady=(5,10))

# Item Name
item_name_label = ctk.CTkLabel(
    left_frame,
    text="Item Name",
    text_color="black",
    font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
)
item_name_label.grid(row=1, column=0, padx=(10,0), pady=(5, 4), sticky="w")

item_name_entry = ctk.CTkEntry(
    left_frame,
    height=30,
    width=280,
    corner_radius=8,
    fg_color="#F9F5EB",
    font=ctk.CTkFont(family="Lexend", size=16),
    border_width=2,
    border_color="black"
)
item_name_entry.grid(row=2, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
item_name_entry.insert(0, "")

# Type
type_label = ctk.CTkLabel(
    left_frame,
    text="Type",
    text_color="black",
    font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
)
type_label.grid(row=3, column=0, padx=(10,0), pady=(5, 4), sticky="w")

type_dropdown = ctk.CTkComboBox(
    left_frame,
    height=30,
    width=280,
    corner_radius=8,
    fg_color="#F9F5EB",
    font=ctk.CTkFont(family="Lexend", size=16),
    border_width=2,
    border_color="black",
    values=["Condiments", "Dairy", "Meat", "Vegetables", "Fruits", "Beverages"]
)
type_dropdown.grid(row=4, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
type_dropdown.set("")

# Quantity & Unit - Wrapped in a frame with 2 columns
qty_unit_frame = ctk.CTkFrame(left_frame, fg_color="#F9F5EB")
qty_unit_frame.grid(row=5, column=0, sticky="ew", padx=(10, 10), pady=(0, 8))
qty_unit_frame.grid_columnconfigure(0, weight=1)
qty_unit_frame.grid_columnconfigure(1, weight=1)

# Quantity Label
quantity_label = ctk.CTkLabel(
    qty_unit_frame,
    text="Quantity",
    text_color="black",
    font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
)
quantity_label.grid(row=0, column=0, padx=(0, 5), pady=(5, 4), sticky="w")

# Unit Label
unit_label = ctk.CTkLabel(
    qty_unit_frame,
    text="Unit",
    text_color="black",
    font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
)
unit_label.grid(row=0, column=1, padx=(5, 0), pady=(5, 4), sticky="w")

# Quantity Entry
quantity_entry = ctk.CTkEntry(
    qty_unit_frame,
    height=30,
    corner_radius=8,
    fg_color="#F9F5EB",
    font=ctk.CTkFont(family="Lexend", size=16),
    border_width=2,
    border_color="black"
)
quantity_entry.grid(row=1, column=0, padx=(0, 5), pady=(0, 0), sticky="ew")
quantity_entry.insert(0, "")

# Unit Dropdown
unit_dropdown = ctk.CTkComboBox(
    qty_unit_frame,
    height=30,
    corner_radius=8,
    fg_color="#F9F5EB",
    font=ctk.CTkFont(family="Lexend", size=16),
    border_width=2,
    border_color="black",
    values=["pack", "piece", "kg", "lbs", "liters", "ml"]
)
unit_dropdown.grid(row=1, column=1, padx=(5, 0), pady=(0, 0), sticky="ew")
unit_dropdown.set("")

# Storage Location
storage_label = ctk.CTkLabel(
    left_frame,
    text="Storage Location",
    text_color="black",
    font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
)
storage_label.grid(row=7, column=0, padx=(10,0), pady=(5, 4), sticky="w")

storage_dropdown = ctk.CTkComboBox(
    left_frame,
    height=30,
    width=280,
    corner_radius=8,
    fg_color="#F9F5EB",
    font=ctk.CTkFont(family="Lexend", size=16),
    border_width=2,
    border_color="black",
    values=["Pantry", "Refrigerator", "Freezer", "Cabinet"]
)
storage_dropdown.grid(row=8, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
storage_dropdown.set("")

# Brand
brand_label = ctk.CTkLabel(
    left_frame,
    text="Brand",
    text_color="black",
    font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
)
brand_label.grid(row=9, column=0, padx=(10,0), pady=(5, 4), sticky="w")

brand_entry = ctk.CTkEntry(
    left_frame,
    height=30,
    width=280,
    corner_radius=8,
    fg_color="#F9F5EB",
    font=ctk.CTkFont(family="Lexend", size=16),
    border_width=2,
    border_color="black"
)
brand_entry.grid(row=10, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
brand_entry.insert(0, "")

# Expiry Date
expiry_label = ctk.CTkLabel(
    left_frame,
    text="Expiry Date",
    text_color="black",
    font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
)
expiry_label.grid(row=11, column=0, padx=(10,0), pady=(5, 4), sticky="w")

expiry_entry = ctk.CTkEntry(
    left_frame,
    height=30,
    width=280,
    corner_radius=8,
    fg_color="#F9F5EB",
    font=ctk.CTkFont(family="Lexend", size=16),
    border_width=2,
    border_color="black"
)
expiry_entry.grid(row=12, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
expiry_entry.insert(0, "")

# RIGHT FRAME CONTENT

# Upload File
upload_label = ctk.CTkLabel(
    right_frame,
    text="Upload File",
    text_color="black",
    font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
)
upload_label.grid(row=0, column=0, padx=(10,0), pady=(15, 4), sticky="w")

# Image display area
image_frame = ctk.CTkFrame(
    right_frame,
    height=150,
    width=280,
    corner_radius=8,
    fg_color="#E8E8E8",
    border_width=2,
    border_color="black"
)
image_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
image_frame.grid_propagate(False)

image_label = ctk.CTkLabel(
    image_frame,
    text="📸\nNo Image Selected",
    font=ctk.CTkFont(family="Lexend", size=18),
    text_color="#666666"
)
image_label.place(relx=0.5, rely=0.5, anchor="center")

# Browse File Button (now with functionality)
browse_btn = ctk.CTkButton(
    right_frame,
    text="Browse File",
    text_color="white",
    height=25,
    width=120,
    corner_radius=15,
    fg_color="#112250",
    hover_color="#1A2E6B",
    font=ctk.CTkFont(family="Lexend", size=12, weight="bold"),
    command=browse_file  # Added the command to call browse_file function
)
browse_btn.grid(row=2, column=0, pady=(0, 15), padx=(160), sticky="ew")

# Supplier
supplier_label = ctk.CTkLabel(
    right_frame,
    text="Supplier",
    text_color="black",
    font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
)
supplier_label.grid(row=3, column=0, padx=(10,0), pady=(5, 4), sticky="w")

supplier_entry = ctk.CTkEntry(
    right_frame,
    height=30,
    width=280,
    corner_radius=8,
    fg_color="#F9F5EB",
    font=ctk.CTkFont(family="Lexend", size=16),
    border_width=2,
    border_color="black"
)
supplier_entry.grid(row=4, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
supplier_entry.insert(0, "")

# Contact Person
contact_person_label = ctk.CTkLabel(
    right_frame,
    text="Contact Person",
    text_color="black",
    font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
)
contact_person_label.grid(row=5, column=0, padx=(10,0), pady=(5, 4), sticky="w")

contact_person_entry = ctk.CTkEntry(
    right_frame,
    height=30,
    width=280,
    corner_radius=8,
    fg_color="#F9F5EB",
    font=ctk.CTkFont(family="Lexend", size=16),
    border_width=2,
    border_color="black"
)
contact_person_entry.grid(row=6, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
contact_person_entry.insert(0, "")

# Contact Number
contact_number_label = ctk.CTkLabel(
    right_frame,
    text="Contact Number",
    text_color="black",
    font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
)
contact_number_label.grid(row=7, column=0, padx=(10,0), pady=(5, 4), sticky="w")

contact_number_entry = ctk.CTkEntry(
    right_frame,
    height=30,
    width=280,
    corner_radius=8,
    fg_color="#F9F5EB",
    font=ctk.CTkFont(family="Lexend", size=16),
    border_width=2,
    border_color="black"
)
contact_number_entry.grid(row=8, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
contact_number_entry.insert(0, "")

# Email
email_label = ctk.CTkLabel(
    right_frame,
    text="Email",
    text_color="black",
    font=ctk.CTkFont(family="Lexend", size=16, weight="bold")
)
email_label.grid(row=9, column=0, padx=(10,0), pady=(5, 4), sticky="w")

email_entry = ctk.CTkEntry(
    right_frame,
    height=30,
    width=280,
    corner_radius=8,
    fg_color="#F9F5EB",
    font=ctk.CTkFont(family="Lexend", size=16),
    border_width=2,
    border_color="black"
)
email_entry.grid(row=10, column=0, sticky="ew", pady=(0, 8), padx=(10,0))
email_entry.insert(0, "")

# BUTTONS inside left_frame
button_frame = ctk.CTkFrame(left_frame, fg_color="#F9F5EB")
button_frame.grid(row=13, column=0, pady=(10, 10))  # Centered by default in column 0

# Center buttons using grid with internal column configuration
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)

# Add Item Button (now with validation functionality)
save_btn = ctk.CTkButton(
    button_frame,
    text="Add Item",
    text_color="white",
    height=40,
    width=150,
    corner_radius=15,
    fg_color="#112250",
    hover_color="#1A2E6B",
    font=ctk.CTkFont(family="Lexend", size=20, weight="bold"),
    command=validate_and_add_item  # Added validation function
)
save_btn.grid(row=0, column=1, padx=10)

app.mainloop()