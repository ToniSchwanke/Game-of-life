
# Game of Life using pygame

import pygame
import numpy as np
import time

# Setting up new colors
color_bg = (10, 10, 20)  # Darker background
color_grid = (30, 30, 60)  # Darker grid lines
color_die_next = (0, 0, 255)  # Blue for dying cells
color_alive_next = (0, 255, 0)  # Green for living cells next

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = color_bg if cells[row, col] == 0 else color_alive_next

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = color_die_next
                updated_cells[row, col] = 0  # Cell dies
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1  # Cell stays alive
                if with_progress:
                    color = color_alive_next
        else:
            if alive == 3:
                updated_cells[row, col] = 1  # Cell becomes alive
                if with_progress:
                    color = color_alive_next

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    cells = np.zeros((60, 80))
    # Initial screen fill removed from here to prevent overwriting cells on every frame

    pygame.display.flip()

    running = False
    clock = pygame.time.Clock()  # Add a clock to manage the frame rate

    while True:
        screen.fill(color_grid)  # Move the fill here to correctly redraw the grid each frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    # No need to update the screen here; let the loop handle it based on 'running'

            if not running and pygame.mouse.get_pressed()[0]:  # Only allow editing if not running
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1 - cells[pos[1] // 10, pos[0] // 10]  # Toggle cell state
                update(screen, cells, 10, with_progress=False)  # Draw the initial state without progress
                pygame.display.update()

        if running:
            cells = update(screen, cells, 10, with_progress=True)  # Update with progress when running
            pygame.display.update()

        clock.tick(10)  # Control the frame rate to make the simulation easier to observe

if __name__ == '__main__':
    main()

