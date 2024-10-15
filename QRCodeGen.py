import qrcode
from tkinter import *
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw

# Global variable to store the generated QR image
qr_img = None

def generate_qr():
    global qr_img
    
    # Get user inputs
    url = url_entry.get()
    version = int(version_entry.get())
    box_size = int(box_size_entry.get())
    border = int(border_entry.get())
    
    # Validate the URL
    if not url.strip():
        messagebox.showerror("Input Error", "Please enter a valid URL.")
        return
    
    # Select colors
    fill_color = fill_color_button["bg"]  # Get selected foreground color
    back_color = back_color_button["bg"]  # Get selected background color

    # Create the QR code
    qr = qrcode.QRCode(
        version=version,
        box_size=box_size,
        border=border
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Generate the image with custom colors
    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")
    
    # Create rounded edges for the QR code
    qr_img = add_rounded_edges(qr_img, radius=20)

    # Display QR code in the UI
    img_display = ImageTk.PhotoImage(qr_img)  # Use the modified image with rounded edges
    qr_label.config(image=img_display)
    qr_label.image = img_display  # Keep a reference to avoid garbage collection

    # Show the "Save" button after generating the QR code
    save_button.grid(row=5, column=0, pady=10)  # Position it in the grid layout

def add_rounded_edges(image, radius):
    """Add rounded edges to an image."""
    width, height = image.size
    # Create a mask for rounded corners
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=255)

    # Create a new image with transparent background
    rounded_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    
    # Paste the original image onto the rounded mask
    rounded_image.paste(image, (0, 0), mask)
    
    return rounded_image

def save_qr():
    if qr_img:
        # Open save dialog
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png", 
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if save_path:
            try:
                # Save the image as PNG
                qr_img.save(save_path)
                messagebox.showinfo("Success", f"QR Code saved as {save_path}!")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save QR Code: {e}")
        else:
            messagebox.showwarning("Save Cancelled", "Save operation was cancelled.")
    else:
        messagebox.showerror("Error", "No QR Code generated to save.")

def choose_fill_color():
    color_code = colorchooser.askcolor(title="Choose QR Code Color")[1]
    if color_code:
        fill_color_button.config(bg=color_code)

def choose_back_color():
    color_code = colorchooser.askcolor(title="Choose Background Color")[1]
    if color_code:
        back_color_button.config(bg=color_code)

# Create the main window
window = Tk()
window.title("QR Code Generator")
window.geometry("600x500")
window.columnconfigure(0, weight=1)  # Make the window resizable

# Create a frame to hold the input fields (URL row)
input_frame_1 = Frame(window)
input_frame_1.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
input_frame_1.columnconfigure(1, weight=1)  # Make the input field expand with window resize

# Label and input for URL (displayed in one row)
Label(input_frame_1, text="Enter URL:").grid(row=0, column=0, padx=10)
url_entry = Entry(input_frame_1, width=40)
url_entry.grid(row=0, column=1, padx=10, sticky="ew")

# Create a second frame for version, box size, and border size (second row)
input_frame_2 = Frame(window)
input_frame_2.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
input_frame_2.columnconfigure(0, weight=1)  # Spacer column for centering
input_frame_2.columnconfigure(7, weight=1)  # Spacer column for centering

# Version, box size, and border size centered in one row
Label(input_frame_2, text="QR Version (1-40):").grid(row=0, column=1, padx=10)
version_entry = Entry(input_frame_2, width=5)
version_entry.insert(0, "5")  # Default value
version_entry.grid(row=0, column=2, padx=10)

Label(input_frame_2, text="Box Size:").grid(row=0, column=3, padx=10)
box_size_entry = Entry(input_frame_2, width=5)
box_size_entry.insert(0, "5")  # Default value
box_size_entry.grid(row=0, column=4, padx=10)

Label(input_frame_2, text="Border Size:").grid(row=0, column=5, padx=10)
border_entry = Entry(input_frame_2, width=5)
border_entry.insert(0, "7")  # Default value
border_entry.grid(row=0, column=6, padx=10)

# Color customization options (displayed below the inputs)
color_frame = Frame(window)
color_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
color_frame.columnconfigure(0, weight=1)
color_frame.columnconfigure(1, weight=1)

# Button to select fill (QR code) color
fill_color_button = Button(color_frame, text="Select QR Code Color", bg="black", fg="white", command=choose_fill_color)
fill_color_button.grid(row=0, column=0, padx=20)

# Button to select background color
back_color_button = Button(color_frame, text="Select Background Color", bg="white", fg="black", command=choose_back_color)
back_color_button.grid(row=0, column=1, padx=20)

# Button to generate the QR code
generate_button = Button(window, text="Generate QR Code", command=generate_qr)
generate_button.grid(row=3, column=0, pady=20)

# Label to display the QR code image
qr_label = Label(window)
qr_label.grid(row=4, column=0, pady=10)

# Button to save the QR code (initially hidden)
save_button = Button(window, text="Save QR Code", command=save_qr)

# Don't display the "Save" button initially
save_button.grid(row=5, column=0)  # Position it in the grid layout but don't display yet.
save_button.grid_remove()  # Ensure it is not displayed until QR code is generated.

# Run the application
window.mainloop()
