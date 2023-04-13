import customtkinter as ctk
from tkinter import messagebox
from Ram_Dump import dump_ram, output

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

        # --------------------------------------------------Window1 Frame-----------------------------------------------------------

        self.Window1 = ctk.CTkFrame(self, fg_color="transparent")
        self.Window1.pack(fill="x", anchor="nw", padx=10)

        # Destination Folder Lable
        self.destLable = ctk.CTkLabel(self.Window1, text="Destination Folder:", font=title)
        self.destLable.pack(anchor="nw")

        # Destination Folder Entry
        self.destEntry = ctk.CTkEntry(self.Window1)
        self.destEntry.pack(fill="x", pady=10)
        self.destEntry.insert(0, output)
        self.destEntry.configure(state="readonly")

        # Progress bar
        self.progress = ctk.CTkProgressBar(self.Window1, orientation="horizontal", mode="indeterminate", height=20)
        self.progress.pack(pady=10, fill="x")

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
        self.closeButton.grid(row=0, column=2)
        
        # Next button
        self.nextButton = ctk.CTkButton(self.button_frame, text="Next", state="disabled", command=self.next_clicked)
        self.nextButton.grid(padx="10", row=0, column=1)
            
        # Capture button
        self.captureButton = ctk.CTkButton(self.button_frame, text="Capture!", command=self.capture_clicked)
        self.captureButton.grid(row=0, column=0)
        
        # Cancel button
        self.cancelButton = ctk.CTkButton(self.button_frame, text="Cancel", command=self.cancel_clicked )
        
        # Finish button
        self.finishButton = ctk.CTkButton(self.button_frame, text="Finish!", command=self.finish_clicked)

    def switch_frame(self):
        self.Window1.pack_forget()
        self.Window2.pack(padx=20, pady=10, anchor="nw", fill="x")
    
    def capture_clicked(self):
        self.captureButton.configure(state="disabled")
        self.closeButton.grid_forget()
        self.cancelButton.grid(row=0, column=2)
        file_path = dump_ram()
        messagebox.showinfo("Message", "Memory Acquisition Completed!") # display a popup message
        self.nextButton.configure(state="normal")
        self.cancelButton.grid_forget()
        self.closeButton.grid(row=0, column=2)
        self.closeButton.configure(state="disabled")

    def next_clicked(self):
        self.nextButton.configure(state="disabled")
        self.switch_frame()
        self.closeButton.grid_forget()
        self.finishButton.grid(row=0, column=2)
        
    def cancel_clicked(self):                                             #This is not defined properly
        
        result = messagebox.askyesno("Confirmation", "Do you want to Cancel?")
        if result:
            self.captureButton.configure(state="enabled")
            self.closeButton.configure(state="enabled")
            self.nextButton.configure(state="disabled")
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
