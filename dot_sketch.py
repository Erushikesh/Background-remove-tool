import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, colorchooser
from rembg import remove
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageChops
import io

class BackgroundRemoverApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Background Remover")
        self.geometry("1000x800")
        self.configure(bg="#1e1e1e")
        
        # Global variables
        self.input_path = None
        self.bg_option = tk.StringVar(value="none")  # options: none, color, image
        self.bg_color = None
        self.bg_image_path = None
        
        self.outline_enabled = tk.BooleanVar(value=False)
        self.outline_color = None
        self.outline_thickness = tk.IntVar(value=5)
        
        self.glow_enabled = tk.BooleanVar(value=False)
        self.glow_intensity = tk.DoubleVar(value=5.0)
        
        self.blend_enabled = tk.BooleanVar(value=False)
        self.blend_image_path = None
        self.blend_mode = tk.StringVar(value="multiply")
        
        self.processed_image = None
        
        # Control frame (left panel)
        self.control_frame = ctk.CTkFrame(self, corner_radius=10)
        self.control_frame.pack(side="left", fill="y", padx=20, pady=20)
        
        self.upload_btn = ctk.CTkButton(self.control_frame, text="Upload Main Image", command=self.upload_main_image)
        self.upload_btn.pack(pady=10)
        
        self.bg_option_label = ctk.CTkLabel(self.control_frame, text="Background Option:")
        self.bg_option_label.pack(pady=5)
        
        self.none_rb = ctk.CTkRadioButton(self.control_frame, text="None", variable=self.bg_option, value="none")
        self.none_rb.pack(pady=2)
        self.color_rb = ctk.CTkRadioButton(self.control_frame, text="Color", variable=self.bg_option, value="color")
        self.color_rb.pack(pady=2)
        self.image_rb = ctk.CTkRadioButton(self.control_frame, text="Image", variable=self.bg_option, value="image")
        self.image_rb.pack(pady=2)
        
        self.choose_color_btn = ctk.CTkButton(self.control_frame, text="Choose BG Color", command=self.choose_bg_color)
        self.choose_color_btn.pack(pady=5)
        self.upload_bg_btn = ctk.CTkButton(self.control_frame, text="Upload BG Image", command=self.upload_bg_image)
        self.upload_bg_btn.pack(pady=5)
        
        self.outline_check = ctk.CTkCheckBox(self.control_frame, text="Add Outline", variable=self.outline_enabled)
        self.outline_check.pack(pady=5)
        self.outline_color_btn = ctk.CTkButton(self.control_frame, text="Choose Outline Color", command=self.choose_outline_color)
        self.outline_color_btn.pack(pady=5)
        self.outline_thickness_label = ctk.CTkLabel(self.control_frame, text="Outline Thickness:")
        self.outline_thickness_label.pack(pady=2)
        self.outline_thickness_slider = ctk.CTkSlider(self.control_frame, from_=1, to=20, variable=self.outline_thickness)
        self.outline_thickness_slider.pack(pady=5)
        
        self.glow_check = ctk.CTkCheckBox(self.control_frame, text="Add Glow", variable=self.glow_enabled)
        self.glow_check.pack(pady=5)
        self.glow_intensity_label = ctk.CTkLabel(self.control_frame, text="Glow Intensity:")
        self.glow_intensity_label.pack(pady=2)
        self.glow_intensity_slider = ctk.CTkSlider(self.control_frame, from_=1, to=20, variable=self.glow_intensity)
        self.glow_intensity_slider.pack(pady=5)
        
        self.blend_check = ctk.CTkCheckBox(self.control_frame, text="Blend with Image", variable=self.blend_enabled)
        self.blend_check.pack(pady=5)
        self.upload_blend_btn = ctk.CTkButton(self.control_frame, text="Upload Blend Image", command=self.upload_blend_image)
        self.upload_blend_btn.pack(pady=5)
        self.blend_mode_label = ctk.CTkLabel(self.control_frame, text="Blend Mode:")
        self.blend_mode_label.pack(pady=2)
        self.blend_mode_menu = ctk.CTkOptionMenu(self.control_frame, values=["multiply", "screen"], variable=self.blend_mode)
        self.blend_mode_menu.pack(pady=5)
        
        self.process_btn = ctk.CTkButton(self.control_frame, text="Process Image", command=self.process_image)
        self.process_btn.pack(pady=10)
        self.save_btn = ctk.CTkButton(self.control_frame, text="Save Image", command=self.save_image)
        self.save_btn.pack(pady=10)
        
        # Preview area (right panel) with moving gradient background for a modern look
        self.preview_label = ctk.CTkLabel(self, text="Image Preview", fg_color="#1e1e1e")
        self.preview_label.pack(side="right", padx=20, pady=20, expand=True)
        self.animate_gradient()
    
    def animate_gradient(self):
        # Simple gradient animation by cycling background colors
        colors = ["#1e1e1e", "#2a2a2a", "#333333", "#2a2a2a"]
        def cycle(i=0):
            self.preview_label.configure(fg_color=colors[i % len(colors)]) 
            self.after(1000, lambda: cycle(i+1))
        cycle()
    
    def upload_main_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if path:
            self.input_path = path
            img = Image.open(path)
            img.thumbnail((600, 600))
            self.display_image(img)
    
    def choose_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.bg_color = color
            self.bg_option.set("color")
    
    def upload_bg_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if path:
            self.bg_image_path = path
            self.bg_option.set("image")
    
    def choose_outline_color(self):
        color = colorchooser.askcolor(title="Choose Outline Color")[1]
        if color:
            self.outline_color = color
    
    def upload_blend_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if path:
            self.blend_image_path = path
    
    def process_image(self):
        if not self.input_path:
            return
        with open(self.input_path, "rb") as f:
            input_data = f.read()
        result_data = remove(input_data)
        img = Image.open(io.BytesIO(result_data)).convert("RGBA")
        
        if self.bg_option.get() == "color" and self.bg_color:
            bg = Image.new("RGBA", img.size, self.bg_color)
            img = Image.alpha_composite(bg, img)
        elif self.bg_option.get() == "image" and self.bg_image_path:
            bg = Image.open(self.bg_image_path).convert("RGBA").resize(img.size)
            img = Image.alpha_composite(bg, img)
        
        if self.outline_enabled.get() and self.outline_color:
            thickness = int(self.outline_thickness.get())
            img = ImageOps.expand(img, border=thickness, fill=self.outline_color)
        
        if self.glow_enabled.get():
            intensity = self.glow_intensity.get()
            glow = img.filter(ImageFilter.GaussianBlur(radius=intensity))
            img = ImageChops.screen(img, glow)
        
        if self.blend_enabled.get() and self.blend_image_path:
            blend_img = Image.open(self.blend_image_path).convert("RGBA").resize(img.size)
            mode = self.blend_mode.get()
            if mode == "multiply":
                img = ImageChops.multiply(img, blend_img)
            elif mode == "screen":
                img = ImageChops.screen(img, blend_img)
        
        self.processed_image = img
        self.display_image(img)
    
    def display_image(self, img):
        preview = img.copy()
        preview.thumbnail((600, 600))
        tk_img = ImageTk.PhotoImage(preview)
        self.preview_label.configure(image=tk_img)
        self.preview_label.image = tk_img
    
    def save_image(self):
        if self.processed_image:
            path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if path:
                self.processed_image.save(path)

if __name__ == "__main__":
    app = BackgroundRemoverApp()
    app.mainloop()
