import re

# File paths for your repository theme
INPUT_FILE = "CustomTheme.vstheme"
OUTPUT_FILE = "CustomTheme.vstheme" # Overwrites safely

# Matrix Palette Configuration Map (ABGR Format)
# Formats: Backgrounds -> Pure Black, Elements -> Cyber Charcoal, Text/Lines -> Matrix Greens
COLOR_REPLACEMENTS = {
    # 1. Canvas and Panels (Absolute Dark Spaces)
    r'Source="FF1E1E1E"': 'Source="FF000000"',  # Default editor background -> Absolute Black
    r'Source="FF2D2D30"': 'Source="FF17110D"',  # Default window panel background -> Deep Cyber Charcoal
    r'Source="FF252526"': 'Source="FF17110D"',  # Secondary dark theme backgrounds -> Deep Cyber Charcoal
    
    # 2. Text Typography (Phosphor Green Overlays)
    r'Source="FFD4D4D4"': 'Source="FF33FF00"',  # Plain Text / Base White labels -> Active Matrix Green
    r'Source="FF569CD6"': 'Source="FF66FF33"',  # Code Keywords -> Bright Phosphor Green
    r'Source="FFD69D85"': 'Source="FF33FF00"',  # Code Strings / Literals -> Active Matrix Green
    r'Source="FF4EC9B0"': 'Source="FF22CC00"',  # Code Classes/Types -> Medium Terminal Green
    r'Source="FF9CDCFE"': 'Source="FF22CC00"',  # Code Variables/Identifiers -> Medium Terminal Green
    r'Source="FF57A64A"': 'Source="FF006611"',  # Code Comments -> Deep Muted Green
    
    # 3. Framing & Static Pulsing Borders 
    r'Source="FF3F3F46"': 'Source="FF008822"',  # Inactive control frame borders -> Subdued Circuit Green
    r'Source="FF007ACC"': 'Source="FF33FF66"',  # Active Highlight / Blue Accents -> Glowing Neon Green Border
}

def apply_matrix_theme():
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Parsing {INPUT_FILE} structural node patterns...")
        modifications = 0
        
        # Sequentially scan and rewrite matching elements across all 11,000+ lines
        for pattern, replacement in COLOR_REPLACEMENTS.items():
            content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
            modifications += count
            
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Success! Adjusted {modifications} elements into a static Matrix layout.")
        print("You can safely double-click CustomTheme.vstheme to open the Visual Designer.")
        
    except FileNotFoundError:
        print(f"Error: Could not locate '{INPUT_FILE}' file. Put this script in your repo root.")

if __name__ == "__main__":
    apply_matrix_theme()
