# PDF Editor

A robust and simple Python script to merge multiple PDF files into a single document using the `pypdf` library.

## Features

- **Sequential Merging:** Joins files in the exact order provided in the command line.
- **Error Handling:** Gracefully skips missing files with a warning instead of crashing.
- **Dependency Check:** Automatically detects if the required library is missing and provides installation instructions.
- **CLI Support:** Easy-to-use Command Line Interface.

## Prerequisites

- **Python 3.6+** installed on your system.
- **pypdf** library.

## Installation

1.  Download or save the `pdf_joiner.py` script.
2.  Install the required Python dependency by running the following command in your terminal:

    ```bash
    pip install pypdf
    ```

## Usage

Use the UI or CLI:

### CLI

```bash

python pdf_joiner.py <output_filename.pdf> <input_file1.pdf> <input_file2.pdf> ...

### UI

<img width="917" height="815" alt="image" src="https://github.com/user-attachments/assets/c500eb87-9627-47dc-ab93-12ae47bc20a0" />
