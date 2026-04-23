# Algo Foundry ⚒️

A personal standard library and experimental lab. This repository goes beyond just "learning algorithms"—it bridges the gap between fundamental computer science and production-ready applied systems, mirrored across multiple languages to build muscle memory across different programming paradigms.

---

## 🧠 Layers

### 1. Core Algorithms
Fundamental building blocks. Clean, generic, and strictly documented implementations of searching, sorting, and core data structures.

### 2. Applied Systems
Real-world implementations built on top of core algorithms.
- **UI Color Extraction Engine** (Built on K-Means clustering)

---

## 🎨 Dynamic UI Color Extraction (Preview)

**Input** → Raw Image  
**Output** → Auto-generated, WCAG-compliant UI theme

*   Extracts dominant colors using K-Means clustering.
*   Assigns UI roles (Primary, Accent, Background) mathematically based on frequency, vibrancy (HSV), and relative luminance.
*   Ensures contrast-safe text (WCAG).

### Example Output:
```text
[Input: Vibrant Synthwave Sunset Image]
↓
Primary:    #8b2f96  ██████████ (Most dominant tone)
Secondary:  #2f1556  ██████████ (Supporting tone)
Accent:     #ff007c  ██████████ (Highest saturation/vibrancy)
Background: #1a0b2e  ██████████ (Lowest luminance for Dark Mode)
Text:       #ffffff  ██████████ (Contrast safe against Background)
```
*(Run `tools/color_palette/python/test_palette.py` to generate real HTML UI mockups from synthetic images!)*

---

## 📂 Detailed Project Structure

### Applied Systems
- **`/tools/color_palette`**
  - `/python` - Production-ready UI theme extractor using OpenCV and scikit-learn.
  - `/typescript` *(Planned - VERY useful for frontend)*
  - `/java` *(Planned)*

### Core Algorithms
The core is divided by language, ensuring clean separation of environments and paradigms.

#### `python/` (Python 3)
*Focus: Readability and rapid prototyping.*
- `/searching` - Binary Search.
- `/sorting` - Quicksort, Mergesort.
- `/data_structures` - Linked List.

#### `java/` (Java)
*Focus: Robust static typing, object-oriented principles, and generics.*
- `/searching` - Binary Search.
- `/sorting` - Quicksort, Mergesort.
- `/data_structures` - Linked List `<T>`.

#### `c/` (C)
*Focus: Memory efficiency and low-level understanding.*
- `/searching` - Binary Search.
- `/sorting` - Quicksort, Mergesort.
- `/data_structures` - Linked List.

#### `typescript/` (TypeScript / Node.js)
*Focus: Modern web development and strict type-checking.*
- `/src` - Searching, Sorting, Data Structures, Patterns (Sliding Window).

---

## ⚙️ The "Mirrored" Discipline

Every core algorithm implementation follows these rules:
1. **Sync**: If a fundamental algorithm is added to one language, it must be added to all others.
2. **Context First**: Every file begins with Time/Space complexity analysis and usage notes (When to use / Avoid).
3. **Self-Testing**: Every file includes a `main` block containing basic assertion tests.
4. **Deterministic Output**: Algorithms must produce consistent results for the same input. (Crucial for tools relying on stochastic processes like K-Means clustering; random seeds must be fixed).

---

## 🧪 Robust Testing Pipeline

Testing here isn't just about passing assertions. It's about validating systemic output.

For example, the Color Palette testing pipeline (`test_palette.py`):
- **Generates synthetic images** on the fly (solid black, pure white, noisy gradients, high contrast).
- **Produces real HTML UI previews** so you can physically *see* the extracted palette in a mock interface.
- **Validates contrast ratios automatically** to ensure the generated UI is actually readable and WCAG-compliant.

---

## ⚠️ IDE & Environment Setup Guide

### Resolving IDE Warnings (Python)
If your IDE reports **"Cannot find module `cv2` or `numpy`"**, it is using the wrong Python interpreter.
1. Navigate to `tools/color_palette/python/`.
2. Install dependencies: `pip install -r requirements.txt`
3. Point your IDE's Python interpreter to the environment where pip installed these packages.

---

## 🚀 Future Roadmap
- [ ] Multi-language implementation of color extraction (TS / Java).
- [ ] Real-time UI preview (web-based visualizer for the extractor).
- [ ] Gradient & theme generation system.

---
*Created by Antigravity*
