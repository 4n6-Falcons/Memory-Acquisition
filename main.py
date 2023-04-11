import customtkinter as ctk
from Ram_Dump import dump_ram, output

# System Settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

appwidth, appheight = 550, 350

# Create App class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("4n6 Dump")
        self.iconbitmap("RAM Icon.ico")
        self.geometry(f"{appwidth}x{appheight}")
        self.resizable(False,False)

        # Destination Folder Lable
        self.destLable = ctk.CTkLabel(self, text="Destination Folder:")
        self.destLable.pack(anchor="nw", padx=10)

        # Destination Folder Entry
        self.destEntry = ctk.CTkEntry(self)
        self.destEntry.pack(fill="x", padx=10, pady=10)
        self.destEntry.insert(0, output)
        self.destEntry.configure(state="readonly")

        # --------------------------------------------------------------------------------------------------
        # Status Lable
        #self.statusLable = ctk.CTkLabel(self, text="Status:")
        #self.statusLable.pack(padx=10, anchor="nw")
        # --------------------------------------------------------------------------------------------------

        # Progress bar
        self.progress = ctk.CTkProgressBar(self, orientation="horizontal", mode="indeterminate", height=20)
        self.progress.pack(padx=10, pady=10, fill="x")

        # Frame for Buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(padx=10, pady=10, anchor="ne")

        # Close button
        self.closeButton = ctk.CTkButton(self.button_frame, text="Close")
        self.closeButton.grid(row=0, column=2, padx=10)

        # Next button
        self.nextButton = ctk.CTkButton(self.button_frame, text="Next", state="Disabled")
        self.nextButton.grid(row=0, column=1, padx=10)

        # Capture button
        self.captureButton = ctk.CTkButton(self.button_frame, text="Capture!", command=dump_ram)
        self.captureButton.grid(row=0, column=0, padx=10)

if __name__ == "__main__":
    app = App()
    # Runs the app
    app.mainloop()