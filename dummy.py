import customtkinter as ctk
from tkinter import messagebox
import os
import subprocess
import re  # <-- Add this at the top of your file if not already present

# --- Configuration ---
# Use color values similar to the web design image
DARK_PURPLE = "#1a0b36"
PRIMARY_DARK = "#1E1E2F"
ACCENT_PINK = "#FF33A1"
TEXT_COLOR = "white"

# --- Main App Class ---
class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure the main window
        self.title("Futuristic Login System")
        self.geometry("800x600")
        self.resizable(False, False)
        
        # Set the appearance mode and default color
        ctk.set_appearance_mode("dark")  # Modes: "system" (default), "dark", "light"
        ctk.set_default_color_theme("blue") # Themes: "blue" (default), "green", "dark-blue"
        
        # Set the main background color for the overall window
        self.configure(fg_color=DARK_PURPLE) 
        
        # Initialize Login variables
        self.username_var = ctk.StringVar(value="")
        self.password_var = ctk.StringVar(value="")
        self.show_password_var = ctk.BooleanVar(value=False)
        
        # Initialize Registration variables (for Toplevel window)
        self.register_username_var = ctk.StringVar(value="")
        self.register_password_var = ctk.StringVar(value="")
        self.register_confirm_password_var = ctk.StringVar(value="")
        self.register_show_password_var = ctk.BooleanVar(value=False)

        # Reference to the register window
        self.register_window = None 
        
        self.create_widgets()

    def create_widgets(self):
        # 1. Main container frame (mimics the large rounded card)
        # Use a slightly lighter dark color to give depth
        main_frame = ctk.CTkFrame(self, fg_color=PRIMARY_DARK, 
                                  corner_radius=20, border_width=1, border_color="#3c3c54")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.85)

        # 2. Grid setup for the split layout
        main_frame.grid_columnconfigure(0, weight=1) # Left (Form)
        main_frame.grid_columnconfigure(1, weight=2) # Right (Welcome)
        main_frame.grid_rowconfigure(0, weight=1)

        # --- Left Side: Login Form ---
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent", corner_radius=0)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Set up inner grid for vertical alignment of form elements
        form_frame.grid_columnconfigure(0, weight=1)

        # Avatar Placeholder (Using a simplified symbol)
        avatar_label = ctk.CTkLabel(form_frame, text="👤", font=("Arial", 60), 
                                    text_color=TEXT_COLOR)
        avatar_label.grid(row=0, column=0, pady=(20, 10))

        # Title
        title_label = ctk.CTkLabel(form_frame, text="User Login", 
                                   font=ctk.CTkFont(family="Inter", size=24, weight="bold"),
                                   text_color=TEXT_COLOR)
        title_label.grid(row=1, column=0, pady=10)

        # --- User Friendly Username Input ---
        # Guidance Label for Username
        ctk.CTkLabel(form_frame, text="👤 Username:", font=("Inter", 12), 
                     text_color="#9fa3aa").grid(row=2, column=0, sticky="w", padx=45)

        # Username Entry
        self.username_entry = ctk.CTkEntry(form_frame, textvariable=self.username_var, 
                                           placeholder_text="Enter your unique username",
                                           width=250, height=45, corner_radius=10, 
                                           fg_color="#12121e", text_color=TEXT_COLOR,
                                           border_color="#3c3c54", border_width=2,
                                           font=ctk.CTkFont(family="Inter", size=14))
        self.username_entry.grid(row=3, column=0, pady=(5, 10))
        
        # --- User Friendly Password Input ---
        # Guidance Label for Password
        ctk.CTkLabel(form_frame, text="🔑 Password:", font=("Inter", 12), 
                     text_color="#9fa3aa").grid(row=4, column=0, sticky="w", padx=45)

        # Password Entry
        self.password_entry = ctk.CTkEntry(form_frame, textvariable=self.password_var, 
                                           placeholder_text="Enter your secure password", show="*",
                                           width=250, height=45, corner_radius=10, 
                                           fg_color="#12121e", text_color=TEXT_COLOR,
                                           border_color="#3c3c54", border_width=2,
                                           font=ctk.CTkFont(family="Inter", size=14))
        self.password_entry.grid(row=5, column=0, pady=(5, 10))
        
        # View Password Checkbox
        view_pass_check = ctk.CTkCheckBox(form_frame, text="View Password", 
                                          variable=self.show_password_var,
                                          command=self.toggle_password,
                                          text_color=TEXT_COLOR,
                                          hover_color=ACCENT_PINK,
                                          fg_color=ACCENT_PINK)
        view_pass_check.grid(row=6, column=0, sticky="w", padx=45, pady=5)


        # Login Button (Pink accent)
        login_button = ctk.CTkButton(form_frame, text="LOGIN", 
                                     command=self.login_verify,
                                     width=250, height=50, corner_radius=10,
                                     fg_color=ACCENT_PINK, hover_color="#e0208c", 
                                     text_color=PRIMARY_DARK,
                                     font=ctk.CTkFont(family="Inter", size=16, weight="bold"))
        login_button.grid(row=7, column=0, pady=20)
        
        # Registration Link
        register_link = ctk.CTkLabel(form_frame, text="Don't have an account? Register Now", 
                                     font=ctk.CTkFont(family="Inter", size=12),
                                     text_color="#9fa3aa", cursor="hand2")
        # Bind the label click to open the registration window
        register_link.bind("<Button-1>", lambda e: self.open_register_window())
        register_link.grid(row=8, column=0, pady=5)


        # --- Right Side: Welcome Banner and Blurred Art ---
        welcome_frame = ctk.CTkFrame(main_frame, fg_color="transparent", corner_radius=0)
        welcome_frame.grid(row=0, column=1, sticky="nsew")
        
        welcome_frame.grid_columnconfigure(0, weight=1)
        welcome_frame.grid_rowconfigure(0, weight=1)

        # Custom canvas for the abstract blur effect (simulates the blob art)
        self.blur_canvas = ctk.CTkCanvas(welcome_frame, bg=PRIMARY_DARK, highlightthickness=0)
        self.blur_canvas.grid(row=0, column=0, sticky="nsew")
        self.blur_canvas.bind("<Configure>", self.draw_blur_art) # Redraw on resize

        # Place the 'Welcome' text over the canvas
        welcome_text = ctk.CTkLabel(welcome_frame, text="Welcome.", 
                                    font=ctk.CTkFont(family="Inter", size=48, weight="bold"),
                                    text_color=TEXT_COLOR)
        welcome_text.place(relx=0.5, rely=0.5, anchor="center")

        subtitle_text = ctk.CTkLabel(welcome_frame, 
                                     text="Secure access to the Criminal Detection System.\nYour privacy is paramount.", 
                                     font=ctk.CTkFont(family="Inter", size=14),
                                     text_color="#9fa3aa", justify="right")
        subtitle_text.place(relx=0.9, rely=0.9, anchor="se")


    def draw_blur_art(self, event=None):
        """Draws simple geometric shapes on the canvas to simulate the blurred gradient."""
        # ... (Blur art logic remains the same) ...
        if event:
            width = event.width
            height = event.height
        else:
            width = self.blur_canvas.winfo_width()
            height = self.blur_canvas.winfo_height()

        self.blur_canvas.delete("all")
    
    # --- Registration Window Methods ---

    def open_register_window(self):
        """Creates and shows the registration Toplevel window."""
        if self.register_window is None or not self.register_window.winfo_exists():
            self.register_window = ctk.CTkToplevel(self) 
            self.register_window.title("Register New Account")
            self.register_window.geometry("400x640")  # Slightly taller to fit rules
            self.register_window.resizable(False, False)
            self.register_window.configure(fg_color=PRIMARY_DARK)
            self.register_window.attributes('-topmost', True)  # Keep on top of main window
                        # ensure a controlled close to clear references safely
            self.register_window.protocol("WM_DELETE_WINDOW", self.close_register_window)

            # --- Registration Form Setup ---
            ctk.CTkLabel(self.register_window, text="✍️", font=("Arial", 60), 
                         text_color=TEXT_COLOR).pack(pady=(20, 10))

            ctk.CTkLabel(self.register_window, text="Create Account", 
                         font=ctk.CTkFont(family="Inter", size=20, weight="bold")).pack(pady=5)
            
            # Username
            ctk.CTkLabel(self.register_window, text="👤 Username:", font=("Inter", 12), 
                         text_color="#9fa3aa").pack(pady=(15, 0), padx=50, anchor="w")

            self.reg_username_entry = self._create_entry(
                self.register_window, self.register_username_var, "e.g., john_doe_123"
            )
            self.reg_username_entry.pack(pady=(0, 10), padx=50)

            # Password
            ctk.CTkLabel(self.register_window, text="🔑 Password:", font=("Inter", 12), 
                         text_color="#9fa3aa").pack(pady=(10, 0), padx=50, anchor="w")

            self.reg_password_entry = self._create_entry(
                self.register_window, self.register_password_var, "Type your secret password", show="*"
            )
            self.reg_password_entry.pack(pady=(0, 5), padx=50)

            # --- Password Rules Display ---
            rules_text = (
                "Password must contain:\n"
                "• At least 8 characters\n"
                "• At least one uppercase letter\n"
                "• At least one special symbol (@, #, $, %, &, etc.)"
            )
            ctk.CTkLabel(
                self.register_window, text=rules_text,
                text_color="#FFB6C1",  # soft pink color
                font=ctk.CTkFont(family="Inter", size=11),
                justify="left"
            ).pack(pady=(0, 15), padx=50, anchor="w")

            # Confirm Password
            ctk.CTkLabel(self.register_window, text="🔒 Confirm Password:", font=("Inter", 12), 
                         text_color="#9fa3aa").pack(pady=(10, 0), padx=50, anchor="w")

            self.reg_confirm_password_entry = self._create_entry(
                self.register_window, self.register_confirm_password_var, "Re-type password for confirmation", show="*"
            )
            self.reg_confirm_password_entry.pack(pady=(0, 10), padx=50)
            
            # View Password Checkbox`-=56jkl;l;./1234`6jkl;.56jkl;./1`-=56jkl;`-=56jkl;/1234`-=534`-=56jk
            reg_view_pass_check = ctk.CTkCheckBox(
                self.register_window, text="View Passwords",
                variable=self.register_show_password_var,
                command=self.toggle_register_passwords,
                text_color=TEXT_COLOR,
                hover_color=ACCENT_PINK,
                fg_color=ACCENT_PINK
            )
            reg_view_pass_check.pack(pady=5)

            # Register Button
            ctk.CTkButton(
                self.register_window, text="REGISTER", 
                command=self.register_user,
                width=250, height=45, corner_radius=10,
                fg_color=ACCENT_PINK, hover_color="#e0208c", 
                text_color=PRIMARY_DARK,
                font=ctk.CTkFont(family="Inter", size=14, weight="bold")
            ).pack(pady=30)
        else:
            self.register_window.focus()  # Bring it to front if already exists
    def close_register_window(self):
        """Safely close the register window and clear callbacks/vars so traces don't run."""
        try:
            # Clear text variables first to avoid callbacks referencing destroyed widgets
            try:
                self.register_username_var.set("")
                self.register_password_var.set("")
                self.register_confirm_password_var.set("")
            except Exception:
                pass

            # Destroy the window if it exists
            if self.register_window is not None and self.register_window.winfo_exists():
                self.register_window.destroy()
        finally:
            # Remove reference so future calls recreate window cleanly
            self.register_window = None


    def _create_entry(self, master, textvariable, placeholder_text, show=None):
        """Helper function to create styled CustomTkinter entry fields."""
        return ctk.CTkEntry(master, textvariable=textvariable, 
                            placeholder_text=placeholder_text, show=show,
                            width=300, height=40, corner_radius=10, 
                            fg_color="#12121e", text_color=TEXT_COLOR,
                            border_color="#3c3c54", border_width=2,
                            font=ctk.CTkFont(family="Inter", size=14))
    
    def safe_configure(self, widget, **kwargs):
        """
        Safely configure a widget if it exists and hasn't been destroyed.
        """
        try:
            # Check if widget exists and is not destroyed
            if widget is not None and hasattr(widget, "winfo_exists") and widget.winfo_exists():
                widget.configure(**kwargs)
            else:
                # widget destroyed or missing — silently skip
                pass
        except Exception as e:
            print(f"safe_configure: failed to configure widget ({e})")



    def toggle_register_passwords(self):
        """Toggles visibility of both password fields in the registration window."""
        show_char = '' if self.register_show_password_var.get() else '*'
        self.safe_configure(getattr(self, "reg_password_entry", None), show=show_char)
        self.safe_configure(getattr(self, "reg_confirm_password_entry", None), show=show_char)



    def register_user(self):
        username = self.register_username_var.get()
        password = self.register_password_var.get()
        confirm_password = self.register_confirm_password_var.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required!", parent=self.register_window)
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!", parent=self.register_window)
            return
        
        # --- Password Strength Validation ---
        if len(password) < 8:
            messagebox.showerror("Weak Password", "Password must be at least 8 characters long.", parent=self.register_window)
            return
        if not re.search(r"[A-Z]", password):
            messagebox.showerror("Weak Password", "Password must contain at least one uppercase letter.", parent=self.register_window)
            return
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            messagebox.showerror("Weak Password", "Password must contain at least one special symbol.", parent=self.register_window)
            return

        if os.path.exists(username):
            messagebox.showerror("Error", "Username already exists!", parent=self.register_window)
            return

        # --- Save Credentials to File ---
        try:
            with open(username, "w") as file:
                file.write(username + "\n")
                file.write(password)
            
            messagebox.showinfo("Success", "Registration Successful! You can now log in.", parent=self.register_window)

            # --- SAFELY unlink textvariables before destroying window ---
            try:
                # Disconnect each entry from its StringVar
                if hasattr(self, "reg_username_entry"):
                    self.reg_username_entry.configure(textvariable=None)
                if hasattr(self, "reg_password_entry"):
                    self.reg_password_entry.configure(textvariable=None)
                if hasattr(self, "reg_confirm_password_entry"):
                    self.reg_confirm_password_entry.configure(textvariable=None)
            except Exception as e:
                print(f"Warning: Failed to unlink register entries: {e}")

            # Clear StringVar values (optional, prevents traces from firing)
            self.register_username_var.set("")
            self.register_password_var.set("")
            self.register_confirm_password_var.set("")

            # --- Now destroy the registration window ---
            self.register_window.destroy()
            
            self.register_username_var.set("")
            self.register_password_var.set("")
            self.register_confirm_password_var.set("")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to register user: {e}", parent=self.register_window)

            
    # --- Login Window Methods ---

    def toggle_password(self):
        """Toggles the visibility of the password entry field in the main login window."""
        show_char = '' if self.show_password_var.get() else '*'
        # Use safe_configure
        try:
            self.password_entry.configure(show=show_char)
        except Exception as e:
            print(f"Warning: failed to configure password entry ({e})")


    

    def login_verify(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Check against local file system (based on original file storage)
        if os.path.exists(username):
            try:
                with open(username, "r") as file1:
                    verify = file1.read().splitlines()
                    # verify[1] should be the stored password
                    if len(verify) > 1 and password == verify[1]:
                        messagebox.showinfo("Success", f"Login Successful! Welcome, {username}!")

                        # --- SAFELY remove traces and then destroy ---
                        try:
                        # Step 1: Unlink traces (prevents CustomTkinter callbacks)
                            if hasattr(self.username_var, "_tk") and self.username_var._tk is not None:
                                self.username_var.trace_vdelete("w", self.username_var.trace_info()[0][1]) if self.username_var.trace_info() else None
                            if hasattr(self.password_var, "_tk") and self.password_var._tk is not None:
                                self.password_var.trace_vdelete("w", self.password_var.trace_info()[0][1]) if self.password_var.trace_info() else None
                        except Exception:
                            pass

                        try:
                            # Step 2: Disconnect from entries (extra safety)
                            if hasattr(self, "username_entry"):
                                self.username_entry.configure(textvariable=None)
                            if hasattr(self, "password_entry"):
                                self.password_entry.configure(textvariable=None)
                        except Exception as e:
                            print(f"Debug: unlink failed: {e}")

                        # Step 3: Clear variables (not strictly needed but safe)
                        self.username_var.set("")
                        self.password_var.set("")

                        # Step 4: Destroy window cleanly
                        self.destroy()

                        # Step 5: Launc window
                        subprocess.Popen(["python", r"C:\Users\Microsoft\Desktop\major project\Facial-Recognition-for-Crime-Detection-master\home.py"])

                        # In a real app, you would destroy this window and open the main app window
                    else:
                        messagebox.showerror("Error", "Invalid Password")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read user file: {e}")
        else:
            # Fallback to the hardcoded admin for testing if no file found
            if username == "admin" and password == "1234":
                 messagebox.showinfo("Success", "Login Successful! Welcome, admin!")
            else:
                messagebox.showerror("Error", "User Not Found")
            
        try:
            self.username_var.set("")
            self.password_var.set("")
            self.safe_configure(self.password_entry, show="*")
            self.show_password_var.set(False)
        except Exception:
            pass




if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
