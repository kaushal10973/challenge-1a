import os
import json
import pdfplumber
from collections import Counter

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def classify_font_levels(words):
    """Assign H1, H2, H3 to top 3 font sizes dynamically."""
    font_sizes = [round(float(w['size']), 1) for w in words]
    common_sizes = [fs for fs, _ in Counter(font_sizes).most_common(3)]

    # Sort descending to map H1 > H2 > H3
    sorted_sizes = sorted(common_sizes, reverse=True)
    size_to_level = {}
    levels = ["H1", "H2", "H3"]

    for i, size in enumerate(sorted_sizes):
        if i < len(levels):
            size_to_level[size] = levels[i]

    return size_to_level

def extract_outline(pdf_path):
    outline = []
    title = None

    with pdfplumber.open(pdf_path) as pdf:
        all_words = []
        for page in pdf.pages:
            words = page.extract_words(extra_attrs=["size", "fontname"])
            all_words.extend(words)

        # Determine font size -> H1/H2/H3 mapping
        size_to_level = classify_font_levels(all_words)

        for page_num, page in enumerate(pdf.pages, start=1):
            words = page.extract_words(extra_attrs=["size", "fontname"])
            for word in words:
                text = word["text"].strip()
                size = round(float(word["size"]), 1)
                font = word["fontname"]

                # Dynamically determine heading level
                level = size_to_level.get(size)

                # First large bold text on page 1 = Title
                if title is None and page_num == 1 and level == "H1" and "Bold" in font:
                    title = text

                if level:
                    outline.append({
                        "level": level,
                        "text": text,
                        "page": page_num
                    })

    if title is None:
        title = "Unknown Title"

    return {
        "title": title,
        "outline": outline
    }

def main():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            print(f"Processing {filename}...")

            result = extract_outline(pdf_path)

            output_file = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"Saved: {output_file}")

if __name__ == "__main__":
    main()
