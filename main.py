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

        # Progress bar
        self.progress = ctk.CTkProgressBar(self, orientation="horizontal", mode="indeterminate", height=20)
        self.progress.pack(padx=10, pady=10, fill="x")

        # Frame for Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(side="bottom", padx=10, pady=10, anchor="ne")

        # Close button
        self.closeButton = ctk.CTkButton(self.button_frame, text="Close")
        self.closeButton.grid(row=0, column=2, padx=10)
        
        # Next button
        self.nextButton = ctk.CTkButton(self.button_frame, text="Next", state="disabled", command=self.next_clicked)
        self.nextButton.grid(row=0, column=1, padx=10)
            
        # Capture button
        self.captureButton = ctk.CTkButton(self.button_frame, text="Capture!", command=self.capture_clicked)
        self.captureButton.grid(row=0, column=0, padx=10)

    def next_clicked(self):
        self.nextButton.configure(state="disabled")
        next_wind = window2()
        next_wind.mainloop()

    def capture_clicked(self):
        self.captureButton.configure(state="disabled")
        file_path = dump_ram()
        messagebox.showinfo("Message", "Process Completed!") # display a popup message
        self.nextButton.configure(state="normal")

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
        
        # Frame for Case details
        self.casedetails = ctk.CTkFrame(self, fg_color="transparent")
        self.casedetails.pack(padx=50, pady=10, anchor="nw")

        # Frame for Questions
        self.casequiz = ctk.CTkFrame(self.casedetails, fg_color="transparent")
        self.casequiz.grid(row=0, column=0)

        # Frame for answers
        self.caseans = ctk.CTkFrame(self.casedetails, fg_color="transparent")
        self.caseans.grid(row=0, column=1, padx=10)

        self.caseid = ctk.CTkLabel(self.casequiz, text="Case Number:")
        self.caseid.pack(anchor="nw")
        
        self.caseid_holder = ctk.CTkEntry(self.caseans)
        self.caseid_holder.pack()
        
        self.casename = ctk.CTkLabel(self.casequiz, text="Case Name:")
        self.casename.pack(pady="5", anchor="nw")
        
        self.casename_holder = ctk.CTkEntry(self.caseans)
        self.casename_holder.pack(pady="5")
        
        self.casedesc = ctk.CTkLabel(self.casequiz, text="Case Description:")
        self.casedesc.pack(anchor="nw")
        
        self.casedesc_holder = ctk.CTkEntry(self.caseans)
        self.casedesc_holder.pack()
        
        #------------------- Examiner Details Session ----------------------------------------------
        
        # Examiner Details Lable
        self.examiner_detail = ctk.CTkLabel(self, text="Examiner Details:")
        self.examiner_detail.pack(anchor="nw", padx=10)
        
        # Frame for Examiner details
        self.examinerdetails = ctk.CTkFrame(self, fg_color="transparent")
        self.examinerdetails.pack(padx=50, pady=10, anchor="nw")
        
        # Frame for Examiner Questions
        self.examinerquiz = ctk.CTkFrame(self.examinerdetails, fg_color="transparent")
        self.examinerquiz.grid(row=0, column=0)

        # Frame for Examiner Answers
        self.examinerans = ctk.CTkFrame(self.examinerdetails, fg_color="transparent")
        self.examinerans.grid(row=0, column=1, padx=10)

        self.examinername = ctk.CTkLabel(self.examinerquiz, text="Name:")
        self.examinername.pack(anchor="nw")
        
        self.examinername_holder = ctk.CTkEntry(self.examinerans)
        self.examinername_holder.pack()
        
        self.examinerphone = ctk.CTkLabel(self.examinerquiz, text="Phone Number:")
        self.examinerphone.pack(pady="5", anchor="nw")
        
        self.examinerphone_holder = ctk.CTkEntry(self.examinerans)
        self.examinerphone_holder.pack(pady="5")
        
        self.examineremail = ctk.CTkLabel(self.examinerquiz, text="Email Id:")
        self.examineremail.pack(anchor="nw")
        
        self.examineremail_holder = ctk.CTkEntry(self.examinerans)
        self.examineremail_holder.pack()
        
        self.examinerorg = ctk.CTkLabel(self.examinerquiz, text="Organization:")
        self.examinerorg.pack(pady="5", anchor="nw")
        
        self.examinerorg_holder = ctk.CTkEntry(self.examinerans)
        self.examinerorg_holder.pack(pady="5")
        
if __name__ == "__main__":
    app = window1()
    # Runs the app
    app.mainloop()
