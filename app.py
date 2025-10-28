# Sai

from customtkinter import *
from PIL import Image
from tkinter import filedialog, messagebox
from main import predict
from camera_module import gemini_search


class FlorAIApp(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x630")
        self.title("FlorAI_V1")
        self.resizable(True, True)

        set_appearance_mode("Dark")

        # Load assets once
        self.side_image = CTkImage(Image.open("./Images/main_page.jpg"), size=(400, 630))
        self.icon_upload = CTkImage(Image.open("./Images/upload-icon.png"), size=(20, 20))
        self.icon_camera = CTkImage(Image.open("./Images/camera_icon.png"), size=(20, 20))

        # Layout
        self.setup_ui()

    def setup_ui(self):
        # Left panel
        CTkLabel(self, image=self.side_image, text="").pack(expand=True, side="left")

        # Right frame
        self.frame = CTkFrame(self, width=500, height=630)
        self.frame.pack_propagate(False)
        self.frame.pack(expand=True, side="right")

        # Image placeholder
        self.image_label = CTkLabel(self.frame, text="")
        self.image_label.place(relx=0.5, rely=0.32, anchor="center")

        # Result label for prediction
        self.result_label = CTkLabel(self.frame, text="", font=("Arial", 15, "bold"))
        self.result_label.place(relx=0.5, rely=0.48, anchor="center")

        # Scrollable Gemini text output
        self.gemini_output = CTkTextbox(
            self.frame, wrap="word", font=("Consolas", 14), height=150, width=400
        )
        self.gemini_output.place(relx=0.5, rely=0.80, anchor="center")
        self.gemini_output.insert("1.0", "AI output will appear here.")
        self.gemini_output.configure(state="disabled")

        # Buttons
        text_color, hover_color, border_color = self.get_theme_colors()

        CTkButton(
            self.frame, text="Upload image", text_color=text_color,
            font=("Arial", 18), corner_radius=32, hover_color=hover_color,
            border_color=border_color, border_width=1, width=150, height=40,
            image=self.icon_upload, compound="left", command=self.upload_image
        ).place(relx=0.5, rely=0.55, anchor="center")

        CTkButton(
            self.frame, text="Open Camera", text_color=text_color,
            font=("Arial", 18), corner_radius=32, hover_color=hover_color,
            border_color=border_color, border_width=1, width=150, height=40,
            image=self.icon_camera, compound="left", command=self.open_camera
        ).place(relx=0.5, rely=0.63, anchor="center")

        # Theme switch
        self.theme_switch = CTkSwitch(
            self.frame, text="Theme", font=("Arial", 18),
            command=self.toggle_theme
        )
        self.theme_switch.place(relx=0.2, rely=0.05, anchor="center")

        # Quit button
        CTkButton(
            self.frame, text=">>>", fg_color="transparent",
            text_color=text_color, font=("Arial", 22),
            border_color=border_color, border_width=1, corner_radius=32,
            width=50, command=self.destroy
        ).place(relx=0.9, rely=0.955, anchor="center")

    def get_theme_colors(self):
        current = get_appearance_mode()
        if current == "Light":
            return "#000000", "#dcf1ff", "#74faff"
        return "#ffffff", "#1a1a1a", "#5ae2ff"

    def toggle_theme(self):
        new_mode = "Dark" if get_appearance_mode() == "Light" else "Light"
        set_appearance_mode(new_mode)
        text_color, hover_color, border_color = self.get_theme_colors()
        self.update_colors(text_color, hover_color, border_color)

    def update_colors(self, text_color, hover_color, border_color):
        for widget in self.frame.winfo_children():
            if isinstance(widget, CTkButton):
                widget.configure(text_color=text_color, hover_color=hover_color, border_color=border_color)

    def upload_image(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Select an image",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp")]
            )
            if not file_path:
                return

            img = CTkImage(Image.open(file_path), size=(200, 200))
            self.image_label.configure(image=img)
            self.image_label.image = img

            label, confidence = predict(file_path)
            if label:
                self.result_label.configure(text=f"Prediction: {label} ({confidence:.2f}%)")
            else:
                self.result_label.configure(text="Prediction failed")
        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {str(e)}")

    def open_camera(self):
        try:
            result = gemini_search()  # Returns Gemini's text output
            if result:
                self.display_gemini_result(result)
            else:
                messagebox.showinfo("Info", "No result received from Gemini.")
        except Exception as e:
            messagebox.showerror("Camera Error", str(e))

    def display_gemini_result(self, text):
        self.gemini_output.configure(state="normal")
        self.gemini_output.delete("1.0", "end")
        self.gemini_output.insert("1.0", text.strip())
        self.gemini_output.configure(state="disabled")


if __name__ == "__main__":
    app = FlorAIApp()
    app.mainloop()