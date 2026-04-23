import os
import cv2
import numpy as np
from ui_palette_extractor import extract_palette

def create_test_image(filename, color_func, size=(300, 300)):
    """Generates a test image using a custom color function."""
    img = np.zeros((size[0], size[1], 3), dtype=np.uint8)
    for y in range(size[0]):
        for x in range(size[1]):
            img[y, x] = color_func(y, x, size)
    cv2.imwrite(filename, img)
    return filename

def generate_test_images():
    """Generate various edge-case and standard test images."""
    os.makedirs("test_images", exist_ok=True)
    images = {}

    # 1. Dark Image (Midnight Blue / Purple vibe)
    images["Dark"] = create_test_image(
        "test_images/dark.jpg", 
        lambda y, x, s: [40 + (y//10), 20, 50] # BGR format for cv2
    )
    
    # 2. Bright Image (Yellow / Orange vibe)
    images["Bright"] = create_test_image(
        "test_images/bright.jpg",
        lambda y, x, s: [100, 200 + (x//10), 250]
    )

    # 3. High Contrast (Black and Red stripes)
    images["High_Contrast"] = create_test_image(
        "test_images/contrast.jpg",
        lambda y, x, s: [0, 0, 255] if (x//20)%2==0 else [0, 0, 0]
    )

    # 4. Washed out (Pastels)
    images["Washed_Out"] = create_test_image(
        "test_images/washed.jpg",
        lambda y, x, s: [200, 220, 210]
    )

    # 5. All White
    images["All_White"] = create_test_image(
        "test_images/white.jpg",
        lambda y, x, s: [255, 255, 255]
    )
    
    # 6. All Black
    images["All_Black"] = create_test_image(
        "test_images/black.jpg",
        lambda y, x, s: [0, 0, 0]
    )

    return images

def generate_html_report(results):
    html = """
    <html>
    <head>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #111; color: #fff; padding: 20px; }
            .container { display: flex; flex-wrap: wrap; gap: 20px; }
            .card { border-radius: 12px; overflow: hidden; box-shadow: 0 10px 20px rgba(0,0,0,0.5); width: 350px; }
            .img-container { height: 150px; background-size: cover; background-position: center; }
            .ui-mockup { padding: 20px; }
            .title { font-size: 1.2em; font-weight: bold; margin-bottom: 5px; }
            .subtitle { font-size: 0.9em; opacity: 0.8; margin-bottom: 15px; }
            .btn { padding: 10px 15px; border-radius: 6px; border: none; font-weight: bold; cursor: pointer; width: 100%; text-align: center; margin-bottom: 15px; }
            .palette-strip { display: flex; height: 30px; margin-top: 10px; border-radius: 4px; overflow: hidden; }
            .color-block { flex: 1; }
            h1 { text-align: center; }
        </style>
    </head>
    <body>
        <h1>UI Color Palette Extractor Tests</h1>
        <div class="container">
    """

    for name, data in results.items():
        roles = data['roles']
        raw = data['raw_palette']
        img_path = data['img']
        
        strip_html = "".join([f'<div class="color-block" style="background: {c};" title="{c}"></div>' for c in raw])
        
        html += f"""
        <div class="card" style="background: {roles['background']}; color: {roles['text']}; border: 1px solid {roles['primary']};">
            <div class="img-container" style="background-image: url('{img_path}');"></div>
            <div class="ui-mockup">
                <div class="title" style="color: {roles['primary']};">{name} Test</div>
                <div class="subtitle">Mockup using extracted palette</div>
                <div class="btn" style="background: {roles['accent']}; color: #fff;">Accent Action</div>
                <div class="btn" style="background: {roles['secondary']}; color: {roles['text']}; border: 1px solid {roles['text']};">Secondary Action</div>
                
                <div style="font-size: 0.8em; margin-top: 20px; opacity: 0.7;">Raw Palette:</div>
                <div class="palette-strip">{strip_html}</div>
            </div>
        </div>
        """

    html += """
        </div>
    </body>
    </html>
    """
    
    with open("test_report.html", "w") as f:
        f.write(html)
    print("Report generated at: test_report.html")

if __name__ == "__main__":
    print("Generating test images...")
    images = generate_test_images()
    
    results = {}
    print("Running extractor...")
    for name, path in images.items():
        try:
            palette = extract_palette(path, k=5)
            palette['img'] = path
            results[name] = palette
            print(f"[OK] {name} parsed successfully")
        except Exception as e:
            print(f"[FAIL] {name} failed: {e}")

    generate_html_report(results)
