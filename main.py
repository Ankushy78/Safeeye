import tkinter as tk
import subprocess
import sys
import os


current_process = None


BASE_DIR = "C:\\Users\\PRANAY\\OneDrive\\Desktop\\SAFEEYE"
SCRIPT_PATHS = {
    "Face Detection": os.path.join(BASE_DIR, "face_detection.py"),
    "Laser Sensor": os.path.join(BASE_DIR, "laser.py"),
    "Thermal Sensor": os.path.join(BASE_DIR, "thermal.py"),
    "Turbalnce Sensor": os.path.join(BASE_DIR, "turbalnce.py")  
}

def run_python_file(filename):
    global current_process

    if current_process:
        current_process.terminate()

  
    if not os.path.exists(filename):
        print(f"Error: {filename} not found!")
        return

    
    try:
        current_process = subprocess.Popen([sys.executable, filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = current_process.communicate()

        if error:
            print(f"Error in {filename}:\n{error.decode()}")
        else:
            print(f"{filename} started successfully.")

    except Exception as e:
        print(f"Failed to run {filename}: {str(e)}")

def on_option_selected(option):
    if option in SCRIPT_PATHS:
        run_python_file(SCRIPT_PATHS[option])
    else:
        print(f"Error: {option} script not found!")

def create_main_window():
    window = tk.Tk()
    window.title("Sensor Script Runner")
    window.geometry("300x300")

    label = tk.Label(window, text="Choose a sensor option:", font=("Arial", 12))
    label.pack(pady=10)

    for option in SCRIPT_PATHS.keys():
        button = tk.Button(window, text=option, command=lambda opt=option: on_option_selected(opt), width=25)
        button.pack(pady=5)
    
    window.mainloop()

if __name__ == "__main__":
    create_main_window()
