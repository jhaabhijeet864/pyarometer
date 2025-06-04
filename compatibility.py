def calculate_compatibility(name1, name2):
    """
    Calculate love compatibility between two names.
    
    Special cases:
    - "Suruchi" and "Abhijeet" (any order) = 1000% (perfect match)
    
    The algorithm:
    1. Normalizes names (lowercase, no spaces)
    2. Calculates a letter score (a=1, b=2, ..., z=26)
    3. Uses exponential decay on absolute difference in scores
    4. Computes common letter ratio
    5. Returns the average of these factors, clamped to 0-100
    """
    # Normalize names - strip whitespace and convert to lowercase
    n1 = name1.strip().lower().replace(" ", "")
    n2 = name2.strip().lower().replace(" ", "")
    
    # Special case detection
    if (n1 == "suruchi" and n2 == "abhijeet") or (n1 == "abhijeet" and n2 == "suruchi"):
        print(f"✨ SPECIAL MATCH DETECTED: {name1} and {name2}! ✨")
        return 100000000 # Perfect match
    
    # You can add more special cases here
    if (n1 == "sonali" and n2 == "harsh") or (n1 == "harsh" and n2 == "sonali"):
        return 100
    
    if (n1 == "siya" and n2 == "abhijeet") or (n1 == "abhijeet" and n2 == "siya"):
        return 85
        
    if (n1 == "suruchi" and n2 == "rohan") or (n1 == "rohan" and n2 == "suruchi"):
        return 0
    
    if (n1 == "tarun" and n2 == "eeshal") or (n1 == "eeshal" and n2 == "tarun"):
        return 150
    
    # Helper function to calculate a score for each letter
    def get_score(s):
        return sum(ord(c) - 96 for c in s if 'a' <= c <= 'z')
    
    # Calculate scores
    score1 = get_score(n1)
    score2 = get_score(n2)
    
    # Calculate difference factor
    diff = abs(score1 - score2)
    import math
    diff_factor = math.floor(math.exp(-diff / 50) * 100)
    
    # Calculate common letter factor
    set1 = set(n1)
    set2 = set(n2)
    common_letters = len(set1.intersection(set2))
    total_unique_letters = len(set1.union(set2))
    
    common_factor = math.floor((common_letters / total_unique_letters) * 100) if total_unique_letters > 0 else 0
    
    # Final compatibility
    compatibility = math.floor((diff_factor + common_factor) / 2)
    
    # Clamp final value between 0-100
    compatibility = min(100, max(0, compatibility))
    
    return compatibility

