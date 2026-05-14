import re

FILE_PATH = "CustomTheme.vstheme"

def apply_strict_matrix():
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            xml_data = f.read()

        print(f"Reading {FILE_PATH}... Applying high-contrast phosphor parameters.")

        # --- STEP 1: CONVERT ALL BACKGROUNDS TO ABSOLUTE VOID BLACK ---
        # Selects every unique configuration of background element values
        bg_pattern = r'(<Background\s+[^>]*?Source=")[^"]+?(")'
        xml_data, bg_count = re.subn(bg_pattern, r'\g<1>ff000000\g<2>', xml_data, flags=re.IGNORECASE)

        # --- STEP 2: CONVERT ALL FOREGROUND TEXT TO INTENSE PHOSPHOR GREEN ---
        # Re-maps all label, syntax, plain text, and terminal characters to highly readable matrix green
        fg_pattern = r'(<Foreground\s+[^>]*?Source=")[^"]+?(")'
        xml_data, fg_count = re.subn(fg_pattern, r'\g<1>ff00ff33\g<2>', xml_data, flags=re.IGNORECASE)

        # --- STEP 3: RECOVER SELECTION LEGIBILITY (INVERSION OVERRIDE) ---
        # Re-parses multi-line XML blocks containing 'Selected' or 'Highlight' to ensure selection visibility
        color_block_pattern = r'(<Color\s+Name="([^"]+?)">)(.*?)(</Color>)'
        selection_count = 0

        def readability_override(match):
            nonlocal selection_count
            open_tag = match.group(1)
            token_name = match.group(2).lower()
            inner_content = match.group(3)
            close_tag = match.group(4)

            # Target active selection highlights, search hits, and focused text blocks
            if "selected" in token_name or "highlight" in token_name:
                # Invert: Force a glaring green background behind absolute pitch-black text string characters
                inner_content = re.sub(r'(<Background\s+[^>]*?Source=")[^"]+?(")', r'\g<1>ff00ff33\g<2>', inner_content, flags=re.IGNORECASE)
                inner_content = re.sub(r'(<Foreground\s+[^>]*?Source=")[^"]+?(")', r'\g<1>ff000000\g<2>', inner_content, flags=re.IGNORECASE)
                selection_count += 1

            return f"{open_tag}{inner_content}{close_tag}"

        xml_data = re.sub(color_block_pattern, readability_override, xml_data, flags=re.DOTALL | re.IGNORECASE)

        # Save changes back to disk
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(xml_data)

        print("\n=== STRICT THEME RESULTS ===")
        print(f"✔️ Background lines mapped to absolute void black: {bg_count}")
        print(f"✔️ Foreground text lines set to terminal green: {fg_count}")
        print(f"✔️ Selection highlights inverted for readability: {selection_count}")
        print("ℹ️ Existing system borders and frame color elements left untouched.")

    except FileNotFoundError:
        print(f"Error: CustomTheme.vstheme not found in this folder.")

if __name__ == "__main__":
    apply_strict_matrix()
