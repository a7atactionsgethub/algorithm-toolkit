"""
UI Palette Extractor
Time Complexity: O(N * I * K * d) where N=pixels, I=iterations, K=clusters, d=dimensions(3)
Space Complexity: O(N) for storing pixel data

Description:
Extracts a highly usable UI color palette from an image using K-Means clustering.
Groups similar colors, sorts by dominance, and assigns specific UI roles based on 
vibrancy and contrast rules (WCAG).

Use when:
- Dynamically generating themes based on user-uploaded images (e.g., Album covers, profile banners).

Avoid when:
- The image is purely noise or heavily distorted (might yield muddy colors without pre-processing).
"""

import cv2
import numpy as np
from sklearn.cluster import KMeans
import colorsys

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def get_luminance(rgb):
    """Calculate WCAG relative luminance."""
    r, g, b = [x / 255.0 for x in rgb]
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def get_contrast_ratio(rgb1, rgb2):
    """Calculate contrast ratio between two colors."""
    l1 = get_luminance(rgb1)
    l2 = get_luminance(rgb2)
    bright = max(l1, l2)
    dark = min(l1, l2)
    return (bright + 0.05) / (dark + 0.05)

def extract_palette(image_path, k=5):
    """
    Extracts a UI-ready color palette from an image.
    Returns a dictionary of colors mapped to UI roles.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image at {image_path}")
    
    # Step 1: Load + downscale image (faster + reduces noise)
    img = cv2.resize(img, (100, 100))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Step 2: Extract pixels
    pixels = img.reshape(-1, 3)

    # Step 3: Reduce colors (K-Means clustering)
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_.astype(int)
    counts = np.bincount(kmeans.labels_)

    # Step 4: Find dominant colors
    sorted_indices = np.argsort(-counts)
    sorted_colors = colors[sorted_indices]

    # Step 5: Assign UI roles
    primary = sorted_colors[0]
    secondary = sorted_colors[1] if len(sorted_colors) > 1 else primary
    
    # Accent: Find the most vibrant color (highest saturation * value in HSV)
    hsv_colors = [colorsys.rgb_to_hsv(c[0]/255, c[1]/255, c[2]/255) for c in sorted_colors]
    vibrancy = [s * v for h, s, v in hsv_colors]
    accent_idx = np.argmax(vibrancy)
    accent = sorted_colors[accent_idx]
    
    # Background: Darkest color for a sleek dark mode look
    luminances = [get_luminance(c) for c in sorted_colors]
    bg_idx = np.argmin(luminances)
    background = sorted_colors[bg_idx]
    
    # Step 6: Ensure readability (WCAG Contrast check)
    white = np.array([255, 255, 255])
    black = np.array([0, 0, 0])
    
    # Test white and black text against background
    if get_contrast_ratio(background, white) >= 4.5:
        text = white
    elif get_contrast_ratio(background, black) >= 4.5:
        text = black
    else:
        # Fallback to the highest contrast option
        text = white if get_luminance(background) < 0.5 else black

    return {
        "roles": {
            "primary": rgb_to_hex(primary),
            "secondary": rgb_to_hex(secondary),
            "accent": rgb_to_hex(accent),
            "background": rgb_to_hex(background),
            "text": rgb_to_hex(text)
        },
        "raw_palette": [rgb_to_hex(c) for c in sorted_colors]
    }

if __name__ == "__main__":
    print("UI Palette Extractor ready. Run tests to see it in action.")
