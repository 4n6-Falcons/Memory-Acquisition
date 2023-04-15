import customtkinter as ctk
from tkinter import messagebox
from threading import Thread
from os import path, remove
import time
from psutil import virtual_memory
from Ram_Dump import dump_ram, output, get_dump_file_path
import config

ctk.set_appearance_mode("System") # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue") # Themes: "blue" (standard), "green", "dark-blue"

class InfoBox(ctk.CTkFrame):
    def __init__(self, parent, title, title_anchor="center", info="", info_fill="none", title_font=("Arial", 14, "bold")):
        super().__init__(parent, fg_color="transparent")

        # Create the title label
        title_label = ctk.CTkLabel(self, text=title, font=title_font)
        title_label.pack(side="top", anchor=title_anchor)

        # Create the info Entry
        info_Entry = ctk.CTkEntry(self)
        info_Entry.pack(side="bottom", fill=info_fill)
        info_Entry.insert(0, info)
        info_Entry.configure(state="readonly")

class QAForm(ctk.CTkFrame):
    def __init__(self, parent, qa_dict, header_name, padx_details=0):
        super().__init__(parent, fg_color="transparent")

        self.labels = {}
        self.entries = {}

        self.header = ctk.CTkLabel(self, text=header_name, font=("Arial", 14, "bold"))
        self.header.grid(row=0, column=0, sticky="w")

        for i, (q, a) in enumerate(qa_dict.items()):
            self.labels[q] = ctk.CTkLabel(self, text=q + ":")
            self.labels[q].grid(row=i+1, column=0, padx=20, pady=2, sticky="w")
            self.entries[q] = ctk.CTkEntry(self, width=config.En_width)
            self.entries[q].grid(row=i+1, column=1, padx=padx_details, pady=2)
            if a:
                self.entries[q].insert(0, a)

    def get_answers(self):
        return {q: e.get() for q, e in self.entries.items()}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        appwidth, appheight = 550, 380
        title = ctk.CTkFont(weight="bold")

        self.title("4n6 Dump")
        self.iconbitmap("RAM Icon.ico")
        self.geometry(f"{appwidth}x{appheight}")
        self.resizable(False,False)

        self.total_ram = virtual_memory().total
        # --------------------------------------------------Window1 Frame-----------------------------------------------------------

        self.Window1 = ctk.CTkFrame(self, fg_color="transparent")
        self.Window1.pack(fill="x", anchor="nw", padx=10)

        self.Window1.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.DestFolder = InfoBox(self.Window1, title="Destination Folder:", title_anchor="nw", info=output, info_fill="x")
        self.DestFolder.grid(row=0, column=0, columnspan=4, sticky="ew")

        self.file_name = InfoBox(self.Window1, title="Specify File Name:", info_fill="x")
        self.file_name.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Specify File Name and Specify File Format Frame
        self.file_frame = ctk.CTkFrame(self.Window1, fg_color="transparent")
        self.file_frame.grid(row=1, column=2, columnspan=2)

        self.filefmtLable = ctk.CTkLabel(self.file_frame, text="Specify File Format: ", font=title)
        self.filefmtLable.pack()
        
        self.filefmt = ctk.CTkOptionMenu(self.file_frame, anchor="center", values=["Default (.raw)", ".dd", ".bin"], width=180)
        self.filefmt.pack()

        # Status Frame
        self.status_frame = ctk.CTkFrame(self.Window1, fg_color="transparent")
        self.status_frame.grid(row=2, column=0, columnspan=2, sticky="nw")

        # Status Lable
        self.status_label = ctk.CTkLabel(self.status_frame, text="Status:", font=title)
        self.status_label.grid(row=0, column=0)

        # Current Status
        self.status = ctk.CTkLabel(self.status_frame, text="Not Started Yet")
        self.status.grid(row=0, column=1, padx=10)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.Window1, orientation="horizontal", mode="determinate", height=20)
        self.progress_bar.grid(row=3, column=0, columnspan=4, sticky="ew")
        self.progress_bar.set(0)

        self.starttime = InfoBox(self.Window1, title="Start Time:")
        self.starttime.grid(row=4, column=0)

        self.endtime = InfoBox(self.Window1, title="End Time:")
        self.endtime.grid(row=4, column=1)

        self.elapsedtime = InfoBox(self.Window1, title="Elapsed Time:")
        self.elapsedtime.grid(row=4, column=2)

        self.osdect = InfoBox(self.Window1, title="Detected OS:")
        self.osdect.grid(row=4, column=3)

        # --------------------------------------------------Window2 Frame-----------------------------------------------------------
        
        self.Window2 = ctk.CTkFrame(self, fg_color="transparent")

        self.QAForm_Case = QAForm(self.Window2, config.case_details, header_name="Case Details:")
        self.QAForm_Case.pack(anchor="nw")

        self.QAForm_Examiner = QAForm(self.Window2, config.examiner_details, header_name="Examiner Details:", padx_details=10)
        self.QAForm_Examiner.pack(anchor="nw")

        # --------------------------------------------------Button Frame-----------------------------------------------------------

        # Frame for Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(side="bottom", pady=10, anchor="ne")

        # Close button
        self.closeButton = ctk.CTkButton(self.button_frame, text="Close", command=self.close_clicked)
        self.closeButton.grid(padx="10", row=0, column=2)
        
        # Next button
        self.nextButton = ctk.CTkButton(self.button_frame, text="Next", state="disabled", command=self.next_clicked)
        self.nextButton.grid(row=0, column=1)
            
        # Capture button
        self.captureButton = ctk.CTkButton(self.button_frame, text="Capture!", command=self.capture_clicked)
        self.captureButton.grid(padx="10", row=0, column=0)
        
        # Cancel button
        self.cancelButton = ctk.CTkButton(self.button_frame, text="Cancel", command=self.cancel_clicked )
        
        # Finish button
        self.finishButton = ctk.CTkButton(self.button_frame, text="Finish!", command=self.finish_clicked)

    def switch_frame(self):
        self.Window1.pack_forget()
        self.Window2.pack(padx=20, pady=10, anchor="nw", fill="x")
        
    def progress(self):
        if config.reset:
            self.progress_bar.set(0)
            self.status.configure(text="Cancelled.., Ready to Start Again")
        elif self.dump.is_alive():
            current_size = path.getsize(config.file_path)
            progress = current_size / self.total_ram
            if progress >= 0.95:
                progress = 0.95
            progress_perct = int(progress * 100)
            self.progress_bar.set(progress)
            self.status.configure(text=f"Dumping.., Please Wait... [ {progress_perct} % ]")
            self.update_idletasks()
            self.after(100)
            self.progress()
        else:
            self.progress_bar.set(1)
            self.status.configure(text=f"Dump Created Successfully!")
            messagebox.showinfo("Message", "Process Completed!") # display a popup message
            self.nextButton.configure(state="normal")
            self.cancelButton.grid_forget()
            self.closeButton.grid(row=0, column=2, padx=10)
            self.closeButton.configure(state="disabled")
    
    def capture_clicked(self):
        self.captureButton.configure(state="disabled")
        config.reset = False
        self.closeButton.grid_forget()
        self.cancelButton.grid(row=0, column=2, padx=10)
        config.file_path = get_dump_file_path()
        self.dump = Thread(target=dump_ram, args=(config.file_path,))
        self.dump.start()
        time.sleep(1)
        self.pro = Thread(target=self.progress)
        self.pro.start()

    def next_clicked(self):
        self.switch_frame()
        self.nextButton.grid_forget()
        self.captureButton.grid_forget()
        self.closeButton.grid_forget()
        self.finishButton.grid(row=0, column=2, padx="10")
        
    def cancel_clicked(self):
        
        result = messagebox.askyesno("Confirmation", "Do you want to Cancel?")
        if result:
            # Stop any running Processes
            config.reset = True

            # Delete any created files
            time.sleep(1)
            if path.exists(config.file_path):
                remove(config.file_path)

            # Reset GUI components to initial state
            self.captureButton.configure(state="normal")
            self.nextButton.configure(state="disabled")
            self.cancelButton.grid_forget()
            self.closeButton.grid(padx="10", row=0, column=2)
        else:
            pass
        
    def close_clicked(self):
        self.destroy()
    
    def finish_clicked(self):
        config.case_details = self.QAForm_Case.get_answers()
        config.examiner_details = self.QAForm_Examiner.get_answers()                                                 
        messagebox.showinfo("Message", f"Report Generated! \n \n Location: \n {output}") 
        self.destroy()
        
if __name__ == "__main__":
    app = App()
    # Runs the app
    app.mainloop()
