# MIT License
#
# Copyright (c) 2026 CoderForge.org Ltd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox  # Fixed: removed space in 'messagebox'

# --- Dependency Check ---
missing_libs = []

try:
    from pypdf import PdfWriter
except ImportError:
    missing_libs.append("pypdf")

try:
    # We use tkinterdnd2 for the drag-and-drop functionality
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    # Only strictly required if running in GUI mode
    if "no-gui" not in sys.argv:
        missing_libs.append("tkinterdnd2")

if missing_libs:
    print("\n[!] Error: Missing required libraries.")
    print("To fix this, please run the following command in your terminal:\n")
    print(f"    pip install {' '.join(missing_libs)}\n")
    sys.exit(1)


# --- Core Logic ---

def merge_pdfs(input_paths, output_path):
    """
    Merges a list of PDF files into a single PDF file.
    """
    merger = PdfWriter()
    files_merged_count = 0

    try:
        print(f"--- Starting PDF Merge ---")
        print("Copyright - CoderForge.org Ltd")
        
        for path in input_paths:
            # Clean up path if it comes from drag-and-drop (sometimes has curly braces)
            path = path.strip('{}')
            
            if not os.path.exists(path):
                print(f"[!] Warning: File not found and skipped: {path}")
                continue
            
            try:
                print(f"Processing: {path}")
                merger.append(path)
                files_merged_count += 1
            except Exception as e:
                print(f"[!] Error reading {path}: {str(e)}")

        if files_merged_count > 0:
            print(f"Writing merged file to: {output_path}")
            merger.write(output_path)
            merger.close()
            print(f"--- Success! Merged {files_merged_count} files. ---")
            return True
        else:
            print("--- Operation failed: No valid files to merge. ---")
            return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        merger.close()
        return False


# --- GUI Implementation ---

class PDFMergerApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("CoderForge.org - PDF Merger")
        self.geometry("600x500")
        self.configure(bg="#f0f0f0")

        # Copyright Label
        lbl_copy = tk.Label(self, text="Copyright © CoderForge.org Ltd (MIT License)", 
                           bg="#f0f0f0", fg="#666666", font=("Arial", 8))
        lbl_copy.pack(side=tk.BOTTOM, pady=5)

        # Header
        lbl_instr = tk.Label(self, text="Drag & Drop PDFs here, or use the 'Add Files' button.", 
                             bg="#f0f0f0", font=("Arial", 11, "bold"))
        lbl_instr.pack(pady=10)

        # Main Listbox Frame
        frame_list = tk.Frame(self, bg="#f0f0f0")
        frame_list.pack(fill=tk.BOTH, expand=True, padx=10)

        # Scrollbar
        scrollbar = tk.Scrollbar(frame_list)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox (The Drop Target)
        self.file_listbox = tk.Listbox(frame_list, selectmode=tk.SINGLE, 
                                       yscrollcommand=scrollbar.set, font=("Courier", 10))
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)

        # Register Drag and Drop
        self.file_listbox.drop_target_register(DND_FILES)
        self.file_listbox.dnd_bind('<<Drop>>', self.drop_files)

        # Buttons Frame
        frame_btns = tk.Frame(self, bg="#f0f0f0")
        frame_btns.pack(fill=tk.X, padx=10, pady=10)

        # Left side buttons (Add/Remove)
        btn_add = tk.Button(frame_btns, text="Add Files...", command=self.add_files)
        btn_add.pack(side=tk.LEFT, padx=5)
        
        btn_remove = tk.Button(frame_btns, text="Remove Selected", command=self.remove_selected)
        btn_remove.pack(side=tk.LEFT, padx=5)

        # Right side buttons (Merge)
        btn_merge = tk.Button(frame_btns, text="MERGE PDFs", bg="#4CAF50", fg="white", 
                              font=("Arial", 10, "bold"), command=self.save_and_merge)
        btn_merge.pack(side=tk.RIGHT, padx=5)

        # Center buttons (Ordering)
        btn_down = tk.Button(frame_btns, text="▼ Down", command=self.move_down)
        btn_down.pack(side=tk.RIGHT, padx=5)
        
        btn_up = tk.Button(frame_btns, text="▲ Up", command=self.move_up)
        btn_up.pack(side=tk.RIGHT, padx=5)

        self.pdf_files = []

    def drop_files(self, event):
        # Handle Drag and Drop event
        files = self.tk.splitlist(event.data)
        for f in files:
            if f.lower().endswith('.pdf'):
                if f not in self.pdf_files:
                    self.pdf_files.append(f)
                    self.file_listbox.insert(tk.END, os.path.basename(f))

    def add_files(self):
        # Handle Manual Add button
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        for f in files:
            if f not in self.pdf_files:
                self.pdf_files.append(f)
                self.file_listbox.insert(tk.END, os.path.basename(f))

    def remove_selected(self):
        sel = self.file_listbox.curselection()
        if not sel: return
        index = sel[0]
        self.file_listbox.delete(index)
        self.pdf_files.pop(index)

    def move_up(self):
        sel = self.file_listbox.curselection()
        if not sel: return
        i = sel[0]
        if i == 0: return # Already at top
        
        # Swap logic
        text = self.file_listbox.get(i)
        self.file_listbox.delete(i)
        self.file_listbox.insert(i-1, text)
        
        path = self.pdf_files.pop(i)
        self.pdf_files.insert(i-1, path)
        
        self.file_listbox.selection_set(i-1)

    def move_down(self):
        sel = self.file_listbox.curselection()
        if not sel: return
        i = sel[0]
        if i == len(self.pdf_files) - 1: return # Already at bottom

        # Swap logic
        text = self.file_listbox.get(i)
        self.file_listbox.delete(i)
        self.file_listbox.insert(i+1, text)
        
        path = self.pdf_files.pop(i)
        self.pdf_files.insert(i+1, path)
        
        self.file_listbox.selection_set(i+1)

    def save_and_merge(self):
        if not self.pdf_files:
            messagebox.showwarning("Warning", "No PDF files selected!")
            return

        output_file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save Merged PDF As"
        )
        
        if output_file:
            success = merge_pdfs(self.pdf_files, output_file)
            if success:
                messagebox.showinfo("Success", "PDFs merged successfully!")
            else:
                messagebox.showerror("Error", "Check console for details.")


# --- Main Entry Point ---

if __name__ == "__main__":
    # Check for CLI bypass flag
    is_cli_mode = False
    clean_args = []
    
    # Filter out 'no-gui' from arguments to see if we have valid file args
    for arg in sys.argv[1:]:
        if arg.lower() == 'no-gui':
            is_cli_mode = True
        else:
            clean_args.append(arg)
            
    if is_cli_mode:
        # CLI MODE: python pdf_joiner.py no-gui <out> <in1> <in2>
        if len(clean_args) < 2:
            print("Usage Error (CLI Mode).")
            print("Correct syntax: python script.py no-gui <output_file.pdf> <input1.pdf> <input2.pdf> ...")
        else:
            output_filename = clean_args[0]
            input_files = clean_args[1:]
            merge_pdfs(input_files, output_filename)
    else:
        # GUI MODE
        app = PDFMergerApp()
        app.mainloop()
