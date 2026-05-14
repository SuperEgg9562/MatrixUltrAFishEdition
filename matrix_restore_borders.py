import re

FILE_PATH = "CustomTheme.vstheme"

def apply_strict_matrix_with_borders():
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            xml_data = f.read()

        print(f"Parsing {FILE_PATH}... Injecting high-contrast rules while preserving all borders.")

        # Match every individual multi-line <Color Name="...">...</Color> block
        color_block_pattern = r'(<Color\s+Name="([^"]+?)">)(.*?)(</Color>)'
        
        bg_count = 0
        fg_count = 0
        skipped_borders = 0

        def process_block(match):
            nonlocal bg_count, fg_count, skipped_borders
            open_tag = match.group(1)
            color_name = match.group(2)
            inner_content = match.group(3)
            close_tag = match.group(4)
            
            name_lower = color_name.lower()

            # --- CRITICAL RULE: IF IT IS A BORDER, SKIP IT COMPLETELY ---
            if any(k in name_lower for k in ["border", "line", "grid", "splitter", "separator", "margin"]):
                skipped_borders += 1
                return match.group(0) # Returns the exact original block without modifications

            # --- RULE A: CONVERT SELECTION BLOCKS TO REVERSED HIGH-CONTRAST ---
            # Resolves the text unreadability bug inside highlighted states
            if "selected" in name_lower or "highlight" in name_lower:
                inner_content, b_sub = re.subn(r'(<Background\s+[^>]*?Source=")[^"]+?(")', r'\g<1>ff00ff33\g<2>', inner_content, flags=re.IGNORECASE)
                inner_content, f_sub = re.subn(r'(<Foreground\s+[^>]*?Source=")[^"]+?(")', r'\g<1>ff000000\g<2>', inner_content, flags=re.IGNORECASE)
                bg_count += b_sub
                fg_count += f_sub
                return f"{open_tag}{inner_content}{close_tag}"

            # --- RULE B: CORE ELEMENT OVERRIDES ---
            # Force background fields to pitch black and foreground text to phosphor green
            inner_content, b_sub = re.subn(r'(<Background\s+[^>]*?Source=")[^"]+?(")', r'\g<1>ff000000\g<2>', inner_content, flags=re.IGNORECASE)
            inner_content, f_sub = re.subn(r'(<Foreground\s+[^>]*?Source=")[^"]+?(")', r'\g<1>ff00ff33\g<2>', inner_content, flags=re.IGNORECASE)
            
            bg_count += b_sub
            fg_count += f_sub

            return f"{open_tag}{inner_content}{close_tag}"

        # Execute the regex transformation across the 11,000+ line document
        updated_xml = re.sub(color_block_pattern, process_block, xml_data, flags=re.DOTALL | re.IGNORECASE)

        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(updated_xml)

        print("\n=== MATRIX REWRITE SUCCESSFUL ===")
        print(f"✔️ Background containers updated to pure black: {bg_count}")
        print(f"✔️ Text & labels switched to phosphor green: {fg_count}")
        print(f"🛡️ Structural framework border items left untouched: {skipped_borders}")
        print("\nClose and reload the file inside Visual Studio to view changes.")

    except FileNotFoundError:
        print(f"Error: Could not locate '{FILE_PATH}' in the current folder.")

if __name__ == "__main__":
    apply_strict_matrix_with_borders()
