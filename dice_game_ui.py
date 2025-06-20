# dice_game_ui.py

import pygame
import sys
import os
import time
import queue
from PIL import Image, ImageSequence
from dice_game_functions import dice_game_main

FIGURE_PATH = "resource_folder/schrodinger_dice_wavefunction_collapse.gif"

def run_dice_gui_controlled(command_queue: queue.Queue):
    # Initialization
    pygame.init()
    WIDTH, HEIGHT = 1000, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Schroedinger's Dice Game")

    # UI
    COLORS = {
        "BACKGROUND": (233, 206, 255),
        "TEXT": (26, 0, 71),
        "BUTTON": (148, 189, 242),
        "EXIT_BTN": (177, 193, 254),
        "FIGURE_BOX": (255, 255, 255)
    }
    FONT = pygame.font.SysFont(None, 36)
    BIG_FONT = pygame.font.SysFont(None, 48)

    exit_button = pygame.Rect(20, 20, 80, 36)
    figure_box = pygame.Rect(600, 150, 360, 320)

    # Animation
    gif_frames = []
    gif_frame_index = 0
    gif_last_update = 0
    gif_frame_delay = 100  # ms

    message = "Waiting for dice command..."

    def load_and_display_gif():
        nonlocal gif_frames, gif_frame_index, gif_last_update
        if os.path.exists(FIGURE_PATH):
            gif_frames.clear()
            pil_img = Image.open(FIGURE_PATH)
            for frame in ImageSequence.Iterator(pil_img):
                frame = frame.convert("RGBA")
                pg_frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                gif_frames.append(pg_frame)
            gif_frame_index = 0
            gif_last_update = pygame.time.get_ticks()
            print(f"[INFO] Loaded {len(gif_frames)} frames from GIF.")
        else:
            print(f"[WARNING] GIF not found at: {FIGURE_PATH}")

    def draw_interface():
        nonlocal gif_frame_index, gif_last_update
        screen.fill(COLORS["BACKGROUND"])

        pygame.draw.rect(screen, COLORS["EXIT_BTN"], exit_button, border_radius=10)
        screen.blit(FONT.render("Exit", True, COLORS["TEXT"]), (exit_button.x + 10, exit_button.y + 5))
        screen.blit(BIG_FONT.render("Schrodinger's Dice", True, COLORS["TEXT"]), (WIDTH // 2 - 100, 40))
        screen.blit(FONT.render(message, True, COLORS["TEXT"]), (100, 140))

        screen.blit(FONT.render("Simulation Output", True, COLORS["TEXT"]), (figure_box.x + 50, figure_box.y - 35))
        pygame.draw.rect(screen, COLORS["FIGURE_BOX"], figure_box, border_radius=15)
        pygame.draw.rect(screen, COLORS["TEXT"], figure_box, 2, border_radius=15)

        if gif_frames:
            current_time = pygame.time.get_ticks()
            if current_time - gif_last_update > gif_frame_delay:
                gif_frame_index = (gif_frame_index + 1) % len(gif_frames)
                gif_last_update = current_time
            frame = gif_frames[gif_frame_index]
            scaled = pygame.transform.smoothscale(frame, (figure_box.width, figure_box.height))
            screen.blit(scaled, (figure_box.x, figure_box.y))

        pygame.display.flip()

    clock = pygame.time.Clock()
    running = True

    while running:
        draw_interface()

        # Handle internal events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    running = False

        # Handle external commands
        try:
            command = command_queue.get_nowait()
            if command == "exit":
                print("[INFO] Exiting dice GUI.")
                running = False
            elif command == "roll":
                print("[INFO] Rolling dice via game logic.")
                message = "Rolling..."  # Update here immediately
                draw_interface()        # Force a redraw before the delay
                pygame.display.flip()   # Ensure it shows on screen

                dice_game_main()
                load_and_display_gif()
                message = "Quantum dice rolled!"  # Final message after done
            else:
                print(f"[WARNING] Unknown command: {command}")
        except queue.Empty:
            pass

        clock.tick(30)

    pygame.quit()
    sys.exit()
