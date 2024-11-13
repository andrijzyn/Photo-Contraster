from PIL import Image, ImageDraw
import numpy as np

# Constants
MARGIN_SIZE = 10
LINE_WIDTH = 5


def load_and_prepare_images(image1_path, image2_path):
    """Load images and resize the second image if sizes do not match."""
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)
    if img1.size != img2.size:
        img2 = img2.resize(img1.size)
    return img1, img2


def create_combined_image(img1, img2):
    """Create a new white background image and paste the two images with a margin."""
    width = img1.width + img2.width + MARGIN_SIZE
    height = max(img1.height, img2.height)
    combined_image = Image.new('RGB', (width, height), (255, 255, 255))
    combined_image.paste(img1, (0, 0))
    combined_image.paste(img2, (img1.width + MARGIN_SIZE, 0))
    return combined_image


def draw_separator_line(image, img1_width, height):
    """Draw a vertical black line between the two pasted images."""
    draw = ImageDraw.Draw(image)
    draw.line((img1_width + MARGIN_SIZE // 2, 0, img1_width + MARGIN_SIZE // 2, height),
              fill=(0, 0, 0), width=LINE_WIDTH)


def create_diff_image(image1_path, image2_path, output_path):
    """Main function to create a diff image by combining two images with a separator line."""
    img1, img2 = load_and_prepare_images(image1_path, image2_path)
    combined_image = create_combined_image(img1, img2)
    draw_separator_line(combined_image, img1.width, combined_image.height)
    combined_image.save(output_path)


# Usage
image1_path = 'image1.png'
image2_path = 'image2.png'
output_path = 'diff_image.png'
create_diff_image(image1_path, image2_path, output_path)
print(f'Результат збережено як {output_path}')