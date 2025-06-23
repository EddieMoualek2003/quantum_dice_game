# dice_game_main.py

import sys
import os
import atexit

GIF_PATH = "resource_folder/schrodinger_dice_wavefunction_collapse.gif"

def is_terminal():
    return sys.stdin.isatty() and sys.stdout.isatty()

def is_gui_available():
    return os.environ.get("DISPLAY", "") != ""

def cleanup():
    try:
        if os.path.exists(GIF_PATH):
            os.remove(GIF_PATH)
            print(f"[INFO] Deleted temporary file: {GIF_PATH}")
    except Exception as e:
        print(f"[WARNING] Failed to delete GIF: {e}")

# Ensure the GIF is always deleted when the program exits
atexit.register(cleanup)

def main():
    # Command-line override
    if "--terminal" in sys.argv:
        from display_terminal import run_terminal
        run_terminal()
        return
    elif "--gui" in sys.argv:
        from display_gui import run_gui
        run_gui()
        return

    # Auto-detection: Prefer GUI
    if is_gui_available():
        try:
            from display_gui import run_gui
            run_gui()
        except Exception as e:
            print(f"[WARNING] GUI failed with error: {e}")
            print("[INFO] Falling back to terminal mode...")
            from display_terminal import run_terminal
            run_terminal()
    elif is_terminal():
        print("[INFO] No GUI detected. Running in terminal mode.")
        from display_terminal import run_terminal
        run_terminal()
    else:
        print("[ERROR] No GUI or terminal detected. Headless mode not supported.")

if __name__ == "__main__":
    main()
