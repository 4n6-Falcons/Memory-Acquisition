import customtkinter as ctk
from tkinter import messagebox
from Ram_Dump import dump_ram, output

# System Settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Created Window1
class window1(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        appwidth, appheight = 550, 350

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
        
        def next_clicked():
            self.nextButton.configure(state="disable")
            next_wind = window2()
            next_wind.mainloop()

        # Next button
        self.nextButton = ctk.CTkButton(self.button_frame, text="Next", state="Disabled", command=next_clicked)
        self.nextButton.grid(row=0, column=1, padx=10)

        def capture_clicked():
            self.captureButton.configure(state="disable")
            dump_ram()
            messagebox.showinfo("Message", "Process Completed!")
            self.nextButton.configure(state="enable") # display a popup message
            
        # Capture button
        self.captureButton = ctk.CTkButton(self.button_frame, text="Capture!", command=capture_clicked)
        self.captureButton.grid(row=0, column=0, padx=10)

#Created Window2
class window2(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        appwidth, appheight = 850, 550 #Temporary
        
        self.title("Evidence Information")
        self.iconbitmap("Evidence-Folder Icon.ico")
        self.geometry(f"{appwidth}x{appheight}")
        self.resizable(False,False)
        
        #------------------- Case Details Session --------------------------------------------------
        
        # Case Details Lable
        self.case_detail = ctk.CTkLabel(self, text="Case Details:")
        self.case_detail.pack(anchor="nw", padx=10)
        
        # Frame for Case Id
        self.caseid_frame = ctk.CTkFrame(self)
        self.caseid_frame.pack(padx=10, pady=10, anchor="nw")
        
        self.caseid = ctk.CTkLabel(self.caseid_frame, text="Case Number:")
        self.caseid.grid(row=0, column=0, padx=10)
        
        self.caseid_holder = ctk.CTkEntry(self.caseid_frame)
        self.caseid_holder.grid(row=0, column=1, padx=10, pady=10,)
        
        # Frame for Case Name
        self.casename_frame = ctk.CTkFrame(self)
        self.casename_frame.pack(padx=10, pady=10, anchor="nw")
        
        self.casename = ctk.CTkLabel(self.casename_frame, text="Case Name:")
        self.casename.grid(row=0, column=0, padx=10)
        
        self.casename_holder = ctk.CTkEntry(self.casename_frame)
        self.casename_holder.grid(row=0, column=1, padx=10, pady=10,)
        
        # Frame for Case Description
        self.casedesc_frame = ctk.CTkFrame(self)
        self.casedesc_frame.pack(padx=10, pady=10, anchor="nw")
        
        self.casedesc = ctk.CTkLabel(self.casedesc_frame, text="Case Description:")
        self.casedesc.grid(row=0, column=0, padx=10)
        
        self.casedesc_holder = ctk.CTkEntry(self.casedesc_frame)
        self.casedesc_holder.grid(row=0, column=1, padx=10, pady=10,)
        
        #------------------- Case Details Session --------------------------------------------------
        
        #------------------- Examiner Details Session ----------------------------------------------
        
        # Examiner Details Lable
        self.examiner_detail = ctk.CTkLabel(self, text="Examiner Details:")
        self.examiner_detail.pack(anchor="nw", padx=10)
        
        # Frame for Examiner Name
        self.examinername_frame = ctk.CTkFrame(self)
        self.examinername_frame.pack(padx=10, pady=10, anchor="nw")
        
        self.examinername = ctk.CTkLabel(self.examinername_frame, text="Name:")
        self.examinername.grid(row=0, column=0, padx=10)
        
        self.examinername_holder = ctk.CTkEntry(self.examinername_frame)
        self.examinername_holder.grid(row=0, column=1, padx=10, pady=10,)
        
        # Frame for Examiner Phone Number
        self.examinerphone_frame = ctk.CTkFrame(self)
        self.examinerphone_frame.pack(padx=10, pady=10, anchor="nw")
        
        self.examinerphone = ctk.CTkLabel(self.examinerphone_frame, text="Phone Number:")
        self.examinerphone.grid(row=0, column=0, padx=10)
        
        self.examinerphone_holder = ctk.CTkEntry(self.examinerphone_frame)
        self.examinerphone_holder.grid(row=0, column=1, padx=10, pady=10,)
        
        # Frame for Examiner Email ID
        self.examineremail_frame = ctk.CTkFrame(self)
        self.examineremail_frame.pack(padx=10, pady=10, anchor="nw")
        
        self.examineremail = ctk.CTkLabel(self.examineremail_frame, text="Email Id:")
        self.examineremail.grid(row=0, column=0, padx=10)
        
        self.examineremail_holder = ctk.CTkEntry(self.examineremail_frame)
        self.examineremail_holder.grid(row=0, column=1, padx=10, pady=10,)
        
        # Frame for Examiner Organization
        self.examinerorg_frame = ctk.CTkFrame(self)
        self.examinerorg_frame.pack(padx=10, pady=10, anchor="nw")
        
        self.examinerorg = ctk.CTkLabel(self.examinerorg_frame, text="Organization:")
        self.examinerorg.grid(row=0, column=0, padx=10)
        
        self.examinerorg_holder = ctk.CTkEntry(self.examinerorg_frame)
        self.examinerorg_holder.grid(row=0, column=1, padx=10, pady=10,)       
        
if __name__ == "__main__":
    app = window1()
    # Runs the app
    app.mainloop()
