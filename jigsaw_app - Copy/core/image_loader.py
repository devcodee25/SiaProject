from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from PIL import Image

def load_pixmap(path: str, target_w: int, target_h: int) -> QPixmap:
    """
    Loads an image from the given path, resizes it using Pillow to cover 
    the target area (KeepAspectRatioByExpanding), and converts it to QPixmap.
    """
    try:
        # 1. Load the image using PIL (Pillow)
        pil_image = Image.open(path)
    except FileNotFoundError:
        # Mas mahusay na error handling
        # I-return ang isang empty QPixmap o mag-raise ng error
        return QPixmap()
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return QPixmap()

    original_w, original_h = pil_image.size
    
    # Check kung 0 ang target dimensions para maiwasan ang ZeroDivisionError
    if target_w <= 0 or target_h <= 0:
        return QPixmap()

    # 2. Calculate scaling ratio to cover the target area (KeepAspectRatioByExpanding)
    ratio_w = target_w / original_w
    ratio_h = target_h / original_h
    
    # Scale to the LARGER ratio to ensure it covers the target area
    if ratio_w > ratio_h:
        new_w = target_w
        new_h = int(original_h * ratio_w)
    else:
        new_w = int(original_w * ratio_h)
        new_h = target_h
        
    # Resize the image using high-quality filter
    pil_image = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # 3. Center Crop to the exact target size
    left = (new_w - target_w) / 2
    top = (new_h - target_h) / 2
    right = (new_w + target_w) / 2
    bottom = (new_h + target_h) / 2
    
    pil_image = pil_image.crop((left, top, right, bottom))
    
    # 4. Convert PIL image to QPixmap
    # Ensure correct format for QImage conversion
    if pil_image.mode != "RGBA":
        pil_image = pil_image.convert("RGBA")
        
    data = pil_image.tobytes("raw", "RGBA")
    
    # Create QImage from bytes
    q_image = QImage(data, target_w, target_h, QImage.Format_RGBA8888)
    
    # Create QPixmap
    pm = QPixmap.fromImage(q_image)

    return pm