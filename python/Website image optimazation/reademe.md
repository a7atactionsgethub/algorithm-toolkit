# ⚡ WebOptimizer — Batch Image Optimizer for Web

Compress and convert images of **any format** into web-ready files with a simple GUI.
Built with Python + Pillow. No internet required.

---

## 📦 Requirements

- **Python 3.8+** — [Download](https://www.python.org/downloads/)
- **Pillow** (auto-installed on first run, or install manually):

```
pip install Pillow
```

---

## 🚀 How to Run

### Windows (easiest)
Double-click **`start.bat`** — it installs Pillow automatically and launches the app.

### Manual
```bash
python image_optimizer.py
```

---

## 🖼️ Supported Input Formats

| Format | Extension |
|--------|-----------|
| JPEG   | `.jpg`, `.jpeg` |
| PNG    | `.png` |
| WebP   | `.webp` |
| GIF    | `.gif` |
| BMP    | `.bmp` |
| TIFF   | `.tiff`, `.tif` |
| Icon   | `.ico` |
| HEIC / HEIF | `.heic`, `.heif` |
| AVIF   | `.avif` |
| Portable bitmap | `.ppm`, `.pgm` |

---

## ⚙️ Settings Guide

### Output Format
| Format | Best For | Transparency |
|--------|----------|--------------|
| **WebP** *(recommended)* | All web images, smallest file size | ✅ Yes |
| **JPEG** | Photos, no transparency needed | ❌ No |
| **PNG** | Logos, icons, lossless quality | ✅ Yes |

> WebP is supported by all modern browsers (Chrome, Firefox, Edge, Safari 14+).

### Quality
- **85–95** → Near-lossless, large files
- **75–85** → Sweet spot for web (recommended: **82**)
- **50–75** → Smaller files, slight quality loss
- **Below 50** → Noticeable compression, very small files

### Max Width
Resizes images proportionally so no image exceeds the chosen width.

| Option | Use Case |
|--------|----------|
| No resize | Keep original dimensions |
| 1920px | Full-screen hero images |
| 1280px | Blog headers, banners |
| 800px | Article body images, cards |
| 480px | Mobile thumbnails |

---

## 📋 How to Use

1. **Add Images** — click to select individual image files, or
2. **Add Folder** — scans the entire folder (and subfolders) for images
3. **Choose Output Folder** — where optimized files will be saved
4. **Set your options** — format, quality, max width
5. **Click ⚡ OPTIMIZE IMAGES** — watch the live log and progress bar
6. **Check the output folder** — all optimized files are there

> Original files are **never modified**. Output is always written to the folder you choose.

---

## 📊 Typical Size Savings

| Input | Output (WebP, Q=82) | Savings |
|-------|---------------------|---------|
| PNG (800×600) | WebP | ~65% |
| JPEG (1200×900) | WebP | ~85% |
| TIFF (large) | WebP | ~90% |

---

## 📁 Project Files

```
WebOptimizer/
├── image_optimizer.py   ← Main app
├── start.bat            ← Windows launcher
└── README.md            ← This file
```

---

## ❓ Troubleshooting

**"Python is not recognized"**
→ Install Python from [python.org](https://www.python.org/downloads/) and check **"Add Python to PATH"** during setup.

**HEIC / AVIF files not opening**
→ Install the extra codec: `pip install pillow-heif`

**App window doesn't open**
→ Make sure Tkinter is installed. On Linux: `sudo apt install python3-tk`

---

## 📄 License

Free to use and modify for personal or commercial projects.