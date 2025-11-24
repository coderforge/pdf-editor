# Copyright - CoderForge.org Ltd
import sys
import os

# specific check for dependency
try:
    from pypdf import PdfWriter
except ImportError:
    print("\n[!] Error: The required library 'pypdf' is not installed.")
    print("To fix this, please run the following command in your terminal:\n")
    print("    pip install pypdf\n")
    sys.exit(1)

def merge_pdfs(input_paths, output_path):
    """
    Merges a list of PDF files into a single PDF file.
    
    Args:
        input_paths (list): List of strings, paths to the input PDF files.
        output_path (str): Path where the merged PDF will be saved.
    """
    # Initialize the writer object
    merger = PdfWriter()
    
    files_merged_count = 0

    try:
        print(f"--- Starting PDF Merge ---")
        print("Copyright - CoderForge.org Ltd")
        
        for path in input_paths:
            # specific check to ensure file exists before trying to read
            if not os.path.exists(path):
                print(f"[!] Warning: File not found and skipped: {path}")
                continue
            
            try:
                print(f"Processing: {path}")
                merger.append(path)
                files_merged_count += 1
            except Exception as e:
                print(f"[!] Error reading {path}: {str(e)}")

        # Only write if we actually added files
        if files_merged_count > 0:
            print(f"Writing merged file to: {output_path}")
            merger.write(output_path)
            merger.close()
            print(f"--- Success! Merged {files_merged_count} files. ---")
        else:
            print("--- Operation failed: No valid files to merge. ---")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        merger.close()

if __name__ == "__main__":
    # Simple command line interface
    # Usage: python pdf_joiner.py <output_name> <input1> <input2> ...
    
    args = sys.argv[1:]
    
    if len(args) < 2:
        print("Usage Error.")
        print("Correct syntax: python pdf_joiner.py <output_file.pdf> <input1.pdf> <input2.pdf> ...")
        print("Example: python pdf_joiner.py my_merged_doc.pdf chapter1.pdf chapter2.pdf")
    else:
        output_filename = args[0]
        input_files = args[1:]
        
        merge_pdfs(input_files, output_filename)