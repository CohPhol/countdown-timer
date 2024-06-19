import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def generate_frame(hours, minutes, seconds, width=640, height=480, font_size=200):
    # Change the background color as needed
    image = Image.new('RGB', (width, height), color=(255,219,172))
    draw = ImageDraw.Draw(image)
    
    script_dir = os.path.dirname(__file__)
    font_path = os.path.join(script_dir, '..', 'assets', 'fonts', 'Ginerin-Regular.otf')
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Font at {font_path} not found. Using default font.")
        font = ImageFont.load_default()
    
    text = f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours > 0 else f"{minutes:02d}:{seconds:02d}"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 3
    # Change the text color as needed
    draw.text((text_x, text_y), text, font=font, fill=(201,162,104)) 
    
    frame = np.array(image)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    return frame

def create_countdown_video(duration, unit, output_path, width=640, height=480, fps=30):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    total_seconds = duration * 60 if unit == "minutes" else duration * 3600
    for total_seconds_left in range(total_seconds, -1, -1):
        hours_left = total_seconds_left // 3600
        minutes_left = (total_seconds_left % 3600) // 60
        seconds_left = total_seconds_left % 60
        frame = generate_frame(hours_left, minutes_left, seconds_left, width, height)
        for _ in range(fps):
            out.write(frame)
    
    out.release()

# Parameters
duration = 1  # Countdown duration
unit = "minutes"  # "minutes" or "hours"
output_folder = 'timer_video'

output_filename = f"{duration}{unit}timer.mp4"
output_file = os.path.join(output_folder, output_filename)

create_folder(output_folder)


create_countdown_video(duration, unit, output_file)

print(f"Countdown video saved to {output_file}")
