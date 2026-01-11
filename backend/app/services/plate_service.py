import re
try:
    from cities import TURKISH_CITIES
except ImportError:
    # Fallback if running tests or isolated
    TURKISH_CITIES = {}

def clean_and_validate_plate(text: str) -> str:
    """
    Cleans and standardizes the plate text using logic similar to the inference pipeline.
    Returns the formatted plate string.
    """
    raw_text = text.upper().strip()
    # Remove common garbage
    clean_text = re.sub(r'[^A-Z0-9\s]', '', raw_text)
    
    # 1. TR Prefix Check & Cleanup
    if clean_text.startswith("TR"):
        clean_text = clean_text[2:].strip() # Remove TR
        
    matcher_text = clean_text
    
    # Basic correction 0/O I/1
    if len(matcher_text) >= 2:
        first_two = list(matcher_text[:2])
        if first_two[0] == 'O': first_two[0] = '0'
        if first_two[0] == 'I': first_two[0] = '1'
        if first_two[1] == 'O': first_two[1] = '0'
        if first_two[1] == 'I': first_two[1] = '1'
        matcher_text = "".join(first_two) + matcher_text[2:]
        
    compact = matcher_text.replace(" ", "")
    
    # Validate structure roughly (2 digits + letters + numbers)
    # If it matches standard TR, format it nicely
    tr_match = re.match(r'^(\d{2})([A-Z]{1,3})(\d{3,4}).*$', compact)
    if tr_match:
        city_code, lets, nums = tr_match.groups()
        if 1 <= int(city_code) <= 81:
            return f"{city_code} {lets} {nums}"
            
    # Police
    police_match = re.match(r'^(\d{2})(A{1,3})(\d{3,4}).*$', compact)
    if police_match:
         city_code, lets, nums = police_match.groups()
         if 1 <= int(city_code) <= 81:
            return f"{city_code} {lets} {nums}"

    # If simple format fails but looks like plate, return cleaned compact version
    return compact
