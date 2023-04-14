import customtkinter as ctk
from tkinter import messagebox
from threading import Thread
from os import path, remove
import time
from psutil import virtual_memory
from Ram_Dump import dump_ram, output, get_dump_file_path
import config

# System Settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Created Window1
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        appwidth, appheight = 550, 350
        title = ctk.CTkFont(weight="bold")

        self.title("4n6 Dump")
        self.iconbitmap("RAM Icon.ico")
        self.geometry(f"{appwidth}x{appheight}")
        self.resizable(False,False)

        self.total_ram = virtual_memory().total
        # --------------------------------------------------Window1 Frame-----------------------------------------------------------

        self.Window1 = ctk.CTkFrame(self, fg_color="transparent")
        self.Window1.pack(fill="x", anchor="nw", padx=10)

        # Destination Folder Lable
        self.destLable = ctk.CTkLabel(self.Window1, text="Destination Folder:", font=title)
        self.destLable.pack(anchor="nw")

        # Destination Folder Entry
        self.destEntry = ctk.CTkEntry(self.Window1)
        self.destEntry.pack(fill="x", pady=5)
        self.destEntry.insert(0, output)
        self.destEntry.configure(state="readonly")
        
        # Specify File Name and Specify File Format Frame
        self.file_frame = ctk.CTkFrame(self.Window1, fg_color="transparent")
        self.file_frame.pack(anchor="nw", pady=20)
        
        # Specify File Name Label
        self.filename_Label = ctk.CTkLabel(self.file_frame, text="Specify File Name:", font=title)
        self.filename_Label.grid(row=0, column=0)
        
        # Specify File Name Entry Box
        self.filename = ctk.CTkEntry(self.file_frame, justify="center", state="readonly", width=250)
        self.filename.grid(row=1, column=0, padx=25)
        
        # Specify File Format Label
        self.filefmtLable = ctk.CTkLabel(self.file_frame, text="Specify File Format: ", font=title)
        self.filefmtLable.grid(row=0, column=1)
        
        # Specify File Format Option Menu
        self.filefmt = ctk.CTkOptionMenu(self.file_frame, anchor="center", values=["Default (.raw)", ".dd", ".bin"], width=180)
        self.filefmt.grid(row=1, column=1, padx=25)

        # Status Frame
        self.status_frame = ctk.CTkFrame(self.Window1, fg_color="transparent")
        self.status_frame.pack(anchor="nw")

        # Status Lable
        self.status_label = ctk.CTkLabel(self.status_frame, text="Status:", font=title)
        self.status_label.grid(row=0, column=0)

        # Current Status
        self.status = ctk.CTkLabel(self.status_frame, text="Not Started Yet")
        self.status.grid(row=0, column=1, padx=10)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.Window1, orientation="horizontal", mode="determinate", height=20)
        self.progress_bar.pack(pady=10, fill="x")
        self.progress_bar.set(0)
        
        # Times and OS Frame
        self.times_os_frame = ctk.CTkFrame(self.Window1, fg_color="transparent")
        self.times_os_frame.pack(anchor="nw")
        
        # Start Time Label
        self.starttime_label = ctk.CTkLabel(self.times_os_frame, text="Start Time:", font=title)
        self.starttime_label.grid(row=0, column=0)
        
        # Start Time Entry Box
        self.starttime = ctk.CTkEntry(self.times_os_frame, justify="center", state="readonly", width=100)
        self.starttime.grid(row=1, column=0, padx=5)
        
        # End Time Label
        self.endtime_label = ctk.CTkLabel(self.times_os_frame, text="End Time:", font=title)
        self.endtime_label.grid(row=0, column=1)
        
        # End Time Entry Box
        self.endtime = ctk.CTkEntry(self.times_os_frame, justify="center", state="readonly", width=100)
        self.endtime.grid(row=1, column=1, padx=5)
        
        # Elapsed Time Label
        self.starttime_label = ctk.CTkLabel(self.times_os_frame, text="Elapsed Time:", font=title)
        self.starttime_label.grid(row=0, column=2)
        
        # Elapsed Time Entry Box
        self.elapsedtime = ctk.CTkEntry(self.times_os_frame, justify="center", state="readonly", width=100)
        self.elapsedtime.grid(row=1, column=2, padx=5)
        
        # OS Detection Label
        self.osdectLabel = ctk.CTkLabel(self.times_os_frame, text="Detected OS: ", font=title)
        self.osdectLabel.grid(row=0, column=3)
        
        #OS Detection Entry Box
        self.osdetc = ctk.CTkEntry(self.times_os_frame, justify="center", state="readonly", width=180)
        self.osdetc.grid(row=1, column=3, padx=5)
        

        # --------------------------------------------------Window2 Frame-----------------------------------------------------------
        
        self.Window2 = ctk.CTkFrame(self, fg_color="transparent")

        # Variables
        En_width = 300

        #------------------- Case Details Session --------------------------------------------------

        # Case Details Lable
        self.case_detail = ctk.CTkLabel(self.Window2, text="Case Details:", font=title)
        self.case_detail.pack(anchor="nw")

        # Frame for Case details
        self.casedetails = ctk.CTkFrame(self.Window2, fg_color="transparent")
        self.casedetails.pack(padx=40, anchor="nw")

        # Frame for Questions
        self.casequiz = ctk.CTkFrame(self.casedetails, fg_color="transparent")
        self.casequiz.grid(row=0, column=0)

        # Frame for answers
        self.caseans = ctk.CTkFrame(self.casedetails, fg_color="transparent")
        self.caseans.grid(row=0, column=1, padx=10)

        self.caseid = ctk.CTkLabel(self.casequiz, text="Case Number:")
        self.caseid.pack(anchor="nw")
        
        self.caseid_holder = ctk.CTkEntry(self.caseans, width=En_width)
        self.caseid_holder.pack()
        
        self.casename = ctk.CTkLabel(self.casequiz, text="Case Name:")
        self.casename.pack(pady="5", anchor="nw")
        
        self.casename_holder = ctk.CTkEntry(self.caseans, width=En_width)
        self.casename_holder.pack(pady="5")
        
        self.casedesc = ctk.CTkLabel(self.casequiz, text="Case Description:")
        self.casedesc.pack(anchor="nw")
        
        self.casedesc_holder = ctk.CTkEntry(self.caseans, width=En_width)
        self.casedesc_holder.pack()
        
        #------------------- Examiner Details Session ----------------------------------------------
        
        # Examiner Details Lable
        self.examiner_detail = ctk.CTkLabel(self.Window2, text="Examiner Details:", font=title)
        self.examiner_detail.pack(anchor="nw")
        
        # Frame for Examiner details
        self.examinerdetails = ctk.CTkFrame(self.Window2, fg_color="transparent")
        self.examinerdetails.pack(padx=40, anchor="nw")
        
        # Frame for Examiner Questions
        self.examinerquiz = ctk.CTkFrame(self.examinerdetails, fg_color="transparent")
        self.examinerquiz.grid(row=0, column=0)

        # Frame for Examiner Answers
        self.examinerans = ctk.CTkFrame(self.examinerdetails, fg_color="transparent")
        self.examinerans.grid(row=0, column=1, padx=10)

        self.examinername = ctk.CTkLabel(self.examinerquiz, text="Name:")
        self.examinername.pack(anchor="nw")
        
        self.examinername_holder = ctk.CTkEntry(self.examinerans, width=En_width)
        self.examinername_holder.pack()
        
        self.examinerphone = ctk.CTkLabel(self.examinerquiz, text="Phone Number:    ")
        self.examinerphone.pack(pady="5", anchor="nw")
        
        self.examinerphone_holder = ctk.CTkEntry(self.examinerans, width=En_width)
        self.examinerphone_holder.pack(pady="5")
        
        self.examineremail = ctk.CTkLabel(self.examinerquiz, text="Email Id:")
        self.examineremail.pack(anchor="nw")
        
        self.examineremail_holder = ctk.CTkEntry(self.examinerans, width=En_width)
        self.examineremail_holder.pack()
        
        self.examinerorg = ctk.CTkLabel(self.examinerquiz, text="Organization:")
        self.examinerorg.pack(pady="5", anchor="nw")
        
        self.examinerorg_holder = ctk.CTkEntry(self.examinerans, width=En_width)
        self.examinerorg_holder.pack(pady="5")

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
            self.status.configure(text="Cancelled.., Ready to Start Again")
            self.closeButton.grid(padx="10", row=0, column=2)
        else:
            pass
        
    def close_clicked(self):
        self.destroy()
    
    def finish_clicked(self):                                                                  
        messagebox.showinfo("Message", f"Report Generated! \n \n Location: \n {output}") 
        self.destroy()
        
if __name__ == "__main__":
    app = App()
    # Runs the app
    app.mainloop()
