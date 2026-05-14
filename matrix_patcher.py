import re

FILE_PATH = "CustomTheme.vstheme"

def apply_readable_matrix_patch():
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            xml_data = f.read()

        print(f"Parsing {FILE_PATH} to correct text contrast hierarchies...")

        # --- STEP 1: DEFINE STRUCTURAL MATRIX PALETTES ---
        VOID_BLACK    = "ff000000"  # Core canvas spaces
        DEEP_CHARCOAL = "ff1a1512"  # Tool panels / Menu backdrops
        MATRIX_GREEN  = "ff33ff00"  # Standard readable phosphor text
        GLOW_ACCENT   = "ff66ff33"  # Active structural border highlights

        # --- STEP 2: BLANKET BASE CONVERSIONS ---
        # Map raw structural foundations first
        xml_data = re.sub(r'(<Background\s+[^>]*?Source=")[^"]+?(")', r'\g<1>' + VOID_BLACK + r'\g<2>', xml_data, flags=re.IGNORECASE)
        xml_data = re.sub(r'(<Foreground\s+[^>]*?Source=")[^"]+?(")', r'\g<1>' + MATRIX_GREEN + r'\g<2>', xml_data, flags=re.IGNORECASE)

        # --- STEP 3: CONTRAST RECOVERY LOOP FOR INTERACTIVE NODES ---
        # Parse individual blocks to split foreground text from background highlights
        color_block_pattern = r'(<Color\s+Name="([^"]+?)">)(.*?)(</Color>)'
        
        def contrast_callback(match):
            full_tag = match.group(1)
            color_name = match.group(2)
            inner_content = match.group(3)
            close_tag = match.group(4)
            
            name_lower = color_name.lower()

            # A. Fix Selected Text & Highlighted Code Blocks (Invert colors so it is readable)
            if "selected" in name_lower or "highlight" in name_lower or "accent" in name_lower:
                # Force a bright green background fill block behind pitch-black text
                inner_content = re.sub(r'(<Background\s+[^>]*?Source=")[^"]+?(")', r'\g<1>' + GLOW_ACCENT + r'\g<2>', inner_content, flags=re.IGNORECASE)
                inner_content = re.sub(r'(<Foreground\s+[^>]*?Source=")[^"]+?(")', r'\g<1>' + VOID_BLACK + r'\g<2>', inner_content, flags=re.IGNORECASE)
            
            # B. Fix Tool Windows, Menus, Popups & Lists (Avoid blending into the main code background)
            elif any(k in name_lower for k in ["toolwindow", "menu", "popup", "listbox", "combobox", "dropdown", "commandbar"]):
                inner_content = re.sub(r'(<Background\s+[^>]*?Source=")[^"]+?(")', r'\g<1>' + DEEP_CHARCOAL + r'\g<2>', inner_content, flags=re.IGNORECASE)
                inner_content = re.sub(r'(<Foreground\s+[^>]*?Source=")[^"]+?(")', r'\g<1>' + MATRIX_GREEN + r'\g<2>', inner_content, flags=re.IGNORECASE)

            # C. Fix Floating Diagnostic Text (Compiler warnings, Tooltips, IntelliSense popups)
            elif "tooltip" in name_lower or "completion" in name_lower or "intellisense" in name_lower:
                inner_content = re.sub(r'(<Background\s+[^>]*?Source=")[^"]+?(")', r'\g<1>' + VOID_BLACK + r'\g<2>', inner_content, flags=re.IGNORECASE)
                inner_content = re.sub(r'(<Foreground\s+[^>]*?Source=")[^"]+?(")', r'\g<1>' + GLOW_ACCENT + r'\g<2>', inner_content, flags=re.IGNORECASE)

            # D. Apply Glowing Accent States to Framework Borders
            if any(k in name_lower for k in ["border", "line", "grid", "splitter"]):
                inner_content = re.sub(r'(<Background\s+[^>]*?Source=")[^"]+?(")', r'\g<1>' + GLOW_ACCENT + r'\g<2>', inner_content, flags=re.IGNORECASE)

            return f"{full_tag}{inner_content}{close_tag}"

        xml_data = re.sub(color_block_pattern, contrast_callback, xml_data, flags=re.DOTALL | re.IGNORECASE)

        # Write the high-contrast configuration back to disk
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(xml_data)

        print("✔️ Clean high-contrast contrast rules injected successfully.")
        print("✔️ Selection highlights, popups, and nested menu elements optimized.")

    except FileNotFoundError:
        print(f"Error: Could not locate '{FILE_PATH}'.")

if __name__ == "__main__":
    apply_readable_matrix_patch()
