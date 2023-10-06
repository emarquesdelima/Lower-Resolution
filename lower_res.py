import tkinter as tk
from tkinter import filedialog, messagebox
import ffmpeg

def reduce_resolution(input_file, output_file, height=480):
    try:
        stream = ffmpeg.input(input_file)
        # First scale to desired height, keeping aspect ratio
        stream = ffmpeg.filter(stream, 'scale', '-1', str(height))
        # Then round width to nearest even number
        stream = ffmpeg.filter(stream, 'scale', 'trunc(iw/2)*2', 'ih')
        stream = ffmpeg.output(stream, output_file)
        ffmpeg.run(stream)
        return True
    except Exception as e:
        print(e)
        return False


def select_input_file():
    filepath = filedialog.askopenfilename(title="Select Video File", filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))
    input_file_var.set(filepath)

def compress_video():
    input_file = input_file_var.get()
    output_file = filedialog.asksaveasfilename(title="Save Compressed Video", defaultextension=".mp4", filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))
    
    if not input_file or not output_file:
        return
    
    height = resolution_var.get()
    success = reduce_resolution(input_file, output_file, height)
    
    if success:
        messagebox.showinfo("Success", "Video compressed successfully!")
    else:
        messagebox.showerror("Error", "Failed to compress video. Please try again.")

# Create the main window
root = tk.Tk()
root.title("Video Compressor")

# Variables
input_file_var = tk.StringVar()
resolution_var = tk.IntVar(value=480)

# Layout
tk.Label(root, text="Select Video:").pack(pady=10)
tk.Entry(root, textvariable=input_file_var, width=40).pack(padx=20, pady=5)
tk.Button(root, text="Browse", command=select_input_file).pack(pady=10)

tk.Label(root, text="Desired Height (e.g., 480 for 480p):").pack(pady=10)
tk.Entry(root, textvariable=resolution_var, width=10).pack(pady=5)

tk.Button(root, text="Compress Video", command=compress_video).pack(pady=20)

root.mainloop()
