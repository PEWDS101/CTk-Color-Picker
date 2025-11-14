import os
import math
import customtkinter
from PIL import Image, ImageTk


# read the file path for images
PATH = os.path.dirname(os.path.realpath(__file__))


# root class
class ColorPicker(customtkinter.CTk):
    def __init__(self, color=(255, 255, 255)):
        super().__init__()
    
        self.title('Color Picker')
        self.iconbitmap(os.path.join(PATH, 'icons/color_wheel.ico'))
        self.geometry('300x450')
        self.resizable(False, False)
        self.attributes('-topmost', True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.default_color = [color[0], color[1], color[2]]
        self.rgb_color = self.default_color[:]
        self._font = customtkinter.CTkFont(weight='bold')
        
        self.initUI()
        
    # create initial widgets
    def initUI(self):
        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.grid(padx=20, pady=20, sticky='nswe')
          
        self.canvas = customtkinter.CTkCanvas(self.frame, height=200, width=200, highlightthickness=0, bg=self.frame._apply_appearance_mode(self.frame._fg_color))
        self.canvas.pack(pady=20)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)

        self.img1 = Image.open(os.path.join(PATH, 'icons/color_wheel.ico')).resize((200, 200), Image.Resampling.LANCZOS)
        self.img2 = Image.open(os.path.join(PATH, 'icons/target.png')).resize((20, 20), Image.Resampling.LANCZOS)
        
        self.cwheel = ImageTk.PhotoImage(self.img1)
        self.target = ImageTk.PhotoImage(self.img2)
        
        self.canvas.create_image(100, 100, image=self.cwheel)
        self.canvas.create_image(100, 100, image=self.target)
        
        self.brightness_slider_value = customtkinter.IntVar()
        self.brightness_slider_value.set(255)
        
        self.slider = customtkinter.CTkSlider(master=self.frame, height=20, border_width=1, button_length=15, progress_color='white', from_=0, to=255, variable=self.brightness_slider_value, number_of_steps=256, command=lambda x:self.update_colors())
        self.slider.pack(fill='both', pady=(0,15), padx=20)

        self.label = customtkinter.CTkLabel(master=self.frame, text='#ffffff', text_color='#000000', height=50, fg_color='#ffffff', corner_radius=24, font=self._font)
        self.label.pack(fill='both', padx=10)
        
        self.button = customtkinter.CTkButton(master=self.frame, text='Get Code', height=50, corner_radius=24, font=self._font, command=self.get_copy_event)
        self.button.pack(fill='both', padx=10, pady=20)
        
        self.after(150, lambda: self.label.focus())
        self.grab_set()
    
    # close and get copy of color code
    def get_copy_event(self, event=None):
        self._color = self.label._fg_color
        # clear and append tkinter clipboard
        self.clipboard_clear()
        self.clipboard_append(self._color)
        self.update()
        
        self.grab_release()
        self.destroy()
        
    # mouse drag event for get color code
    def on_mouse_drag(self, event=None):
        x = event.x
        y = event.y
        self.canvas.delete("all")
        self.canvas.create_image(100, 100, image=self.cwheel)
        
        d_from_center = math.sqrt((100-x)**2 + (100-y)**2)
        
        if d_from_center < 100: self.target_x, self.target_y = x, y
        else: self.target_x, self.target_y = self.projection_on_circle(x, y, 100, 100, 99)
            
        self.canvas.create_image(self.target_x, self.target_y, image=self.target)
        
        self.get_target_color()
        self.update_colors()

    # get target color code
    def get_target_color(self):
        try:
            self.rgb_color = self.img1.getpixel((self.target_x, self.target_y))
            r = self.rgb_color[0]
            g = self.rgb_color[1]
            b = self.rgb_color[2]    
            self.rgb_color = [r, g, b]
        except AttributeError:
            self.rgb_color = self.default_color
    
    # update color code
    def update_colors(self):
        brightness = self.brightness_slider_value.get()
        self.get_target_color()

        r = int(self.rgb_color[0] * (brightness/255))
        g = int(self.rgb_color[1] * (brightness/255))
        b = int(self.rgb_color[2] * (brightness/255))
        
        self.rgb_color = [r, g, b]
        self.hex_color = "#{:02x}{:02x}{:02x}".format(*self.rgb_color)
        
        self.slider.configure(progress_color=self.hex_color)
        self.label.configure(fg_color=self.hex_color)
        self.label.configure(text=str(self.hex_color))
        
        if self.brightness_slider_value.get() < 70:
            self.label.configure(text_color='white')
        else: self.label.configure(text_color='black')
            
        if str(self.label._fg_color)=='black':
            self.label.configure(text_color='white')
            
    # handle of circle for code code
    def projection_on_circle(self, point_x, point_y, circle_x, circle_y, radius):
        angle = math.atan2(point_y - circle_y, point_x - circle_x)
        projection_x = circle_x + radius * math.cos(angle)
        projection_y = circle_y + radius * math.sin(angle)

        return projection_x, projection_y


# root
if __name__ == '__main__':
    app = ColorPicker()               
    app.mainloop()