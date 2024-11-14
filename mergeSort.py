#MERGE sort
import pygame
import random
import time
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 255, 255)
WHITE = (255, 255, 255)

# Column settings
COLUMN_WIDTH = 12
COLUMN_GAP = 2

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sorting Algorithm Visualization")

# Font for labels
font = pygame.font.SysFont('Arial', 12)

# Function to draw a column/bar with a label at the bottom
def draw_column(height, x_pos, value, max_height, highlight=False):
    column_color = WHITE if highlight else BLUE
    column_height = height / max_height * (SCREEN_HEIGHT - 100)  # Scale height to fit screen
    pygame.draw.rect(screen, column_color, (x_pos, SCREEN_HEIGHT - column_height - 50, COLUMN_WIDTH, column_height))
    label = font.render(str(value), True, WHITE)
    label_rect = label.get_rect(center=(x_pos + COLUMN_WIDTH // 2, SCREEN_HEIGHT - 20))
    screen.blit(label, label_rect)

# Function to update columns with highlighting
def update_columns(arr, positions, max_height, highlight_indices=None):
    screen.fill(BLACK)
    for i, (height, x_pos) in enumerate(zip(arr, positions)):
        highlight = highlight_indices and (i in highlight_indices)
        draw_column(height, x_pos, height, max_height, highlight=highlight)
    pygame.display.update()

# Function to play a sound note based on frequency
def play_sound_note(frequency):
    sample_rate = 44100
    duration = 0.1  # Duration of the sound note in seconds
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    note = np.sin(2 * np.pi * frequency * t)
    
    # Convert to 16-bit format for Pygame mixer
    audio_data = note * (2**15 - 1)
    audio_data = audio_data.astype(np.int16)
    
    # Initialize and play sound
    pygame.mixer.init(sample_rate, -16, 1, 1024)  # Mono sound
    sound = pygame.mixer.Sound(audio_data)
    sound.play()

# Merge sort algorithm with visualization and sound
def merge_sort(arr, positions, max_height, left, right):
    if left < right:
        mid = (left + right) // 2

        # Recursively sort the first half
        merge_sort(arr, positions, max_height, left, mid)

        # Recursively sort the second half
        merge_sort(arr, positions, max_height, mid + 1, right)

        # Merge the sorted halves
        merge(arr, positions, max_height, left, mid, right)

# Function to merge two halves
def merge(arr, positions, max_height, left, mid, right):
    # Temporary arrays
    left_half = arr[left:mid + 1]
    right_half = arr[mid + 1:right + 1]

    i = j = 0
    k = left

    while i < len(left_half) and j < len(right_half):
        if left_half[i] <= right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        k += 1

        # Update columns and play sound
        update_columns(arr, positions, max_height, highlight_indices=list(range(left, right + 1)))
        frequency = base_frequency + (arr[k - 1] / max(arr)) * octave_range * base_frequency
        play_sound_note(frequency)
        time.sleep(0.05)

    # Copy any remaining elements of left_half
    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1

        # Update columns and play sound
        update_columns(arr, positions, max_height, highlight_indices=list(range(left, right + 1)))
        frequency = base_frequency + (arr[k - 1] / max(arr)) * octave_range * base_frequency
        play_sound_note(frequency)
        time.sleep(0.05)

    # Copy any remaining elements of right_half
    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1

        # Update columns and play sound
        update_columns(arr, positions, max_height, highlight_indices=list(range(left, right + 1)))
        frequency = base_frequency + (arr[k - 1] / max(arr)) * octave_range * base_frequency
        play_sound_note(frequency)
        time.sleep(0.05)

# Generate data from 1 to 20
arr = list(range(1, 41))

# Shuffle the array for visualization
random.shuffle(arr)

# Initial positions of columns
positions = [(x * (COLUMN_WIDTH + COLUMN_GAP) + 50) for x in range(len(arr))]

# Draw initial columns
update_columns(arr, positions, max(arr))

# Sound parameters
base_frequency = 440  # Base frequency for lowest number
octave_range = 2  # Number of octaves to span

time.sleep(2)
# Run merge sort and visualize
merge_sort(arr, positions, max(arr), 0, len(arr) - 1)

# Highlight all columns from 1 to N one by one
for i in range(1, len(arr) + 1):
    # Play sound note for the current column
    frequency = base_frequency + (arr[i - 1] / max(arr)) * octave_range * base_frequency
    play_sound_note(frequency)
    
    # Highlight the current column
    update_columns(arr, positions, max(arr), highlight_indices=list(range(i)))
    time.sleep(0.05)  # Delay before highlighting next column
time.sleep(0.25)
update_columns(arr, positions, max(arr))

# Event loop to keep the window open
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
