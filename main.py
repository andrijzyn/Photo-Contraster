from PIL import Image, ImageDraw
import numpy as np

# Constants
LINE_WIDTH = 1
BACKGROUND_COLOR = (255, 255, 255)
SEPARATOR_COLOR = (0, 0, 0)


def load_and_prepare_images(image1_path, image2_path):
    """Load images and resize the second image if sizes do not match."""
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)
    if img1.size != img2.size:
        img2 = img2.resize(img1.size)
    return img1, img2


def crop_image_to_half(img, is_left_half):
    """Crop the image to its left or right half."""
    width = img.width
    half_width = width // 2

    if is_left_half:
        return img.crop((0, 0, half_width, img.height))
    else:
        return img.crop((half_width, 0, width, img.height))


def create_combined_image(img1, img2):
    """Create a new image by combining the two halves without margin."""
    # Get the cropped halves
    left_half = crop_image_to_half(img1, True)
    right_half = crop_image_to_half(img2, False)

    # Create new image with exact width needed for both halves
    width = left_half.width + right_half.width
    height = max(img1.height, img2.height)
    combined_image = Image.new('RGB', (width, height), BACKGROUND_COLOR)

    # Paste the halves side by side
    combined_image.paste(left_half, (0, 0))
    combined_image.paste(right_half, (left_half.width, 0))

    return combined_image


def draw_separator_line(image, line_color=SEPARATOR_COLOR, line_width=LINE_WIDTH):
    """Draw a vertical line exactly in the middle of the image."""
    draw = ImageDraw.Draw(image)
    center_x = image.width // 2

    # Draw line in the exact center
    draw.line(
        [(center_x, 0), (center_x, image.height)],
        fill=line_color,
        width=line_width
    )


def create_diff_image(image1_path, image2_path, output_path):
    """Create a diff image without margin between halves."""
    # Load and prepare images
    img1, img2 = load_and_prepare_images(image1_path, image2_path)

    # Create combined image without margin
    combined_image = create_combined_image(img1, img2)

    # Draw separator line
    draw_separator_line(combined_image)

    # Save result
    combined_image.save(output_path)
    return combined_image


# Usage
image1_path = 'image1.png'
image2_path = 'image2.png'
output_path = 'diff_image.png'

try:
    result = create_diff_image(image1_path, image2_path, output_path)
    print(f'Saved as {output_path}')
except Exception as e:
    print(f'Error: {str(e)}')