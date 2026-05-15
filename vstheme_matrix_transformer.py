import os
import re
import xml.etree.ElementTree as ET

# Master Palette Map - Overrides all possible elements into Digital Blue-Green/Teal Matrix Theme
COLOR_MAP = {
    # Whites and Light/Medium Greys -> Pure Deep Cyber Blue-Greens
    "FFFFFFFF": "FF000B14",  # Pure White -> Ultra-dark digital base
    "FFF0F0F0": "FF000810",  # Light Grey -> Secondary panel depth
    "FFE0E0E0": "FF001220",  # Mid-Light Grey -> Highlight container
    "FFCCCCCC": "FF001A2E",  # Border Grey -> Gridline accent
    "FFF1F1F1": "FF000B14",  # VS System interface grey -> Dark Base
    
    # System Greys & Shading -> Low-lit Digital Green & Blue accents
    "FF888888": "FF002D3D",  # Slate Grey -> Cyber Teal structural line
    "FF777777": "FF003F44",  # Muted Grey -> Deep low-lit matrix green
    "FF555555": "FF002633",  # Outline Grey -> Border gridline
    "FF999999": "FF005F66",  # Secondary text grey -> Clear teal-grey font
    "FF424242": "FF001A2E",  # Dark control border -> Cyber base containment
    
    # Hardcoded IDE Slate Blocks -> Override to Cyber Terminal Base
    "FF1E1E1E": "FF000B14",  # Default Dark theme slate -> Dark Matrix Base
    "FF2D2D30": "FF000810",  # Window Header slate -> Dark Panel Base
    "FF1B1B1C": "FF00050A",  # Dropdown pop-up layer -> Deep Shadow Grid
    
    # Standard Interface Interactive Accents -> Intense Glowing Neon Cyan & Green
    "FF007ACC": "FF00F5FF",  # Classic VS Blue -> Pure Neon Cyber Cyan
    "FF009BD8": "FF00E5EE",  # Soft highlight blue -> Glowing Cyan Frame
    "FF3399FF": "FF00F5FF",  # Interactive active focus -> Pure Neon Gridline
}

HEX_PATTERN = re.compile(r'[0-9A-Fa-f]{8}')

def convert_hex(hex_val):
    """Converts a specific hex color string to its Matrix digital ecosystem block."""
    upper_hex = hex_val.upper()
    if upper_hex in COLOR_MAP:
        return COLOR_MAP[upper_hex]
    
    # Clean up any missed white or light silver variations automatically
    if upper_hex.endswith("FFFFFF") or upper_hex.endswith("F0F0F0") or upper_hex.endswith("D6D6D6"):
        return "FF000B14"
    # Route completely dead blacks to match our custom deep blue-green grid lines
    if upper_hex.endswith("000000") and not upper_hex.startswith("00"):
        return "FF00050A"
        
    return hex_val

def apply_absolute_skin(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        modified_count = 0
        
        # Traverse every single tag down the XML configuration tree
        for node in root.iter():
            # Intercept all element blocks representing background, border, or text color definitions
            if node.tag in ('Background', 'Foreground', 'Color'):
                # Force Visual Studio to read our custom hex color instead of falling back to system themes
                if "Type" in node.attrib:
                    node.set("Type", "CT_RAW")
                
                source_val = node.get("Source")
                if source_val:
                    match = HEX_PATTERN.search(source_val)
                    if match:
                        old_hex = match.group(0)
                        new_hex = convert_hex(old_hex)
                        if new_hex != old_hex:
                            node.set("Source", source_val.replace(old_hex, new_hex))
                            modified_count += 1
            
            # Universal text and foreground filter: force high-contrast terminal matrix green text
            if node.tag == 'Foreground':
                source_val = node.get("Source")
                if source_val and any(g in source_val.upper() for g in ["FFFFFFFF", "FFF1F1F1", "FF999999"]):
                    node.set("Source", "FF00FF41")
                    modified_count += 1
                    
            # Inject glowing border attributes to ensure windows and IDE panels match theme parameters
            if "Name" in node.attrib and any(border in node.get("Name") for border in ["Border", "Gridline", "Separator"]):
                if node.tag == 'Background' or node.tag == 'Foreground':
                    node.set("Source", "FF00F5FF")  # Glowing Cyan border lines
                    modified_count += 1

        # Write data structure securely back to disk
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        
        # Line cleaning phase: Eliminate compilation-breaking trailing whitespaces
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        clean_lines = [line.rstrip() + '\n' for line in lines]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(clean_lines)
            
        print(f"Success: Fully converted {modified_count} properties to an absolute Matrix Theme in {os.path.basename(file_path)}.")
    except Exception as e:
        print(f"Critical Error skinning file {file_path}: {e}")

def main():
    current_directory = os.path.dirname(os.path.realpath(__file__)) or '.'
    for root_dir, _, files in os.walk(current_directory):
        for file in files:
            if file.endswith('.vstheme'):
                apply_absolute_skin(os.path.join(root_dir, file))

if __name__ == "__main__":
    main()
