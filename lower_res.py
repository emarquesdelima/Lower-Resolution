import tkinter as tk
from tkinter import filedialog, messagebox
import ffmpeg
import py7zr

def compress_video(input_file, output_file, height=480):
    try:
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.filter(stream, 'scale', '-1', str(height))
        stream = ffmpeg.output(stream, output_file)
        ffmpeg.run(stream)
        return True
    except Exception as e:
        print(e)
        return False

def compress_7z(source, output):
    try:
        with py7zr.SevenZipFile(output, mode='w') as z:
            z.writeall(source)
        return True
    except Exception as e:
        print(e)
        return False

def decompress_7z(source, output_dir):
    try:
        with py7zr.SevenZipFile(source, mode='r') as z:
            z.extractall(path=output_dir)
        return True
    except Exception as e:
        print(e)
        return False

def handle_action():
    input_file = input_file_var.get()
    if not input_file:
        return

    action = action_var.get()
    if action == "Compress Video":
        output_file = filedialog.asksaveasfilename(title="Save Compressed Video", defaultextension=".mp4", filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))
        if not output_file:
            return
        height = resolution_var.get()
        success = compress_video(input_file, output_file, height)
    elif action == "Compress to 7z":
        output_file = filedialog.asksaveasfilename(title="Save as 7z", defaultextension=".7z", filetypes=(("7z files", "*.7z"), ("All files", "*.*")))
        if not output_file:
            return
        success = compress_7z(input_file, output_file)
    elif action == "Decompress from 7z":
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return
        success = decompress_7z(input_file, output_dir)

    if success:
        messagebox.showinfo("Success", f"{action} successful!")
    else:
        messagebox.showerror("Error", f"Failed to {action}. Please try again.")

root = tk.Tk()
root.title("Video & 7z Handler")

input_file_var = tk.StringVar()
resolution_var = tk.IntVar(value=480)
action_var = tk.StringVar(value="Compress Video")

tk.Label(root, text="Select File/Folder:").pack(pady=10)
tk.Entry(root, textvariable=input_file_var, width=40).pack(padx=20, pady=5)
tk.Button(root, text="Browse", command=lambda: input_file_var.set(filedialog.askopenfilename())).pack(pady=10)

tk.Label(root, text="Action:").pack(pady=10)
actions = ["Compress Video", "Compress to 7z", "Decompress from 7z"]
tk.OptionMenu(root, action_var, *actions).pack(pady=5)

tk.Label(root, text="Desired Height (only for video compression, e.g., 480 for 480p):").pack(pady=10)
tk.Entry(root, textvariable=resolution_var, width=10).pack(pady=5)

tk.Button(root, text="Execute", command=handle_action).pack(pady=20)

root.mainloop()
