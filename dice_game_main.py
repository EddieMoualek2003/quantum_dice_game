# dice_game_main.py

import sys
import os
import atexit

GIF_PATH = "resource_folder/schrodinger_dice_wavefunction_collapse.gif"

def is_gui_available():
    return os.environ.get("DISPLAY", "") != ""

def cleanup():
    """Delete the generated GIF when the program exits."""
    try:
        if os.path.exists(GIF_PATH):
            os.remove(GIF_PATH)
            print(f"[INFO] Deleted temporary file: {GIF_PATH}")
    except Exception as e:
        print(f"[WARNING] Failed to delete GIF: {e}")

# Register the cleanup function to run at exit
atexit.register(cleanup)

def main():
    # Command-line overrides
    if "--terminal" in sys.argv:
        from display_terminal import run_terminal
        run_terminal()
        return
    elif "--gui" in sys.argv:
        from display_gui import run_gui
        run_gui()
        return

    # Auto-detect environment
    if is_gui_available():
        try:
            from display_gui import run_gui
            run_gui()
        except Exception as e:
            print(f"[WARNING] GUI failed with error: {e}")
            print("[INFO] Falling back to terminal mode...")
            from display_terminal import run_terminal
            run_terminal()
    else:
        print("[INFO] No GUI detected. Defaulting to terminal mode.")
        from display_terminal import run_terminal
        run_terminal()

if __name__ == "__main__":
    main()
