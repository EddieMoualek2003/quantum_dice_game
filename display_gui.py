# display_gui.py

import pygame
import sys
import os
from PIL import Image, ImageSequence
from engine import dice_game_main

FIGURE_PATH = "resource_folder/schrodinger_dice_wavefunction_collapse.gif"

def run_gui():
    pygame.init()
    WIDTH, HEIGHT = 800, 480
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Schrödinger's Dice Game")

    COLORS = {
        "BACKGROUND": (233, 206, 255),
        "TEXT": (26, 0, 71),
        "BUTTON": (148, 189, 242),
        "EXIT_BTN": (177, 193, 254),
        "FIGURE_BOX": (255, 255, 255)
    }

    def get_fonts():
        return pygame.font.SysFont(None, int(HEIGHT * 0.045)), pygame.font.SysFont(None, int(HEIGHT * 0.065))

    FONT, BIG_FONT = get_fonts()

    def get_layout():
        return {
            "exit_button": pygame.Rect(WIDTH * 0.02, HEIGHT * 0.03, WIDTH * 0.08, HEIGHT * 0.06),
            "roll_button": pygame.Rect(WIDTH * 0.12, HEIGHT * 0.03, WIDTH * 0.1, HEIGHT * 0.06),
            "figure_box": pygame.Rect(WIDTH * 0.6, HEIGHT * 0.25, WIDTH * 0.35, HEIGHT * 0.5),
            "title_pos": (WIDTH * 0.35, HEIGHT * 0.07),
            "message_pos": (WIDTH * 0.1, HEIGHT * 0.23),
            "label_pos": (WIDTH * 0.6 + WIDTH * 0.05, HEIGHT * 0.22)
        }

    gif_frames = []
    gif_frame_index = 0
    gif_last_update = 0
    gif_frame_delay = 100  # milliseconds
    message = "Click 'Roll Dice' to begin!"

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
        nonlocal gif_frame_index, gif_last_update, FONT, BIG_FONT
        FONT, BIG_FONT = get_fonts()
        layout = get_layout()
        exit_button = layout["exit_button"]
        roll_button = layout["roll_button"]
        figure_box = layout["figure_box"]
        title_pos = layout["title_pos"]
        message_pos = layout["message_pos"]
        label_pos = layout["label_pos"]

        screen.fill(COLORS["BACKGROUND"])

        # Draw Buttons
        pygame.draw.rect(screen, COLORS["EXIT_BTN"], exit_button, border_radius=10)
        pygame.draw.rect(screen, COLORS["BUTTON"], roll_button, border_radius=10)
        screen.blit(FONT.render("Exit", True, COLORS["TEXT"]), (exit_button.x + 10, exit_button.y + 5))
        screen.blit(FONT.render("Roll Dice", True, COLORS["TEXT"]), (roll_button.x + 10, roll_button.y + 5))

        # Draw Text
        screen.blit(BIG_FONT.render("Schrödinger's Dice", True, COLORS["TEXT"]), title_pos)
        screen.blit(FONT.render(message, True, COLORS["TEXT"]), message_pos)
        screen.blit(FONT.render("Simulation Output", True, COLORS["TEXT"]), label_pos)

        # Draw Figure Box
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
        WIDTH, HEIGHT = screen.get_size()
        draw_interface()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                layout = get_layout()
                if layout["exit_button"].collidepoint(event.pos):
                    running = False
                elif layout["roll_button"].collidepoint(event.pos):
                    message = "Rolling quantum dice..."
                    draw_interface()
                    pygame.display.flip()
                    dice_game_main()
                    load_and_display_gif()
                    message = "Quantum dice rolled!"

            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        clock.tick(30)

    pygame.quit()
    sys.exit()
