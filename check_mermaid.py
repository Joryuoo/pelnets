import os
import re

dir_path = r"C:\Users\Kyle\Downloads\pelnets\2023"
md_files = [f for f in os.listdir(dir_path) if f.endswith(".md")]

for file in md_files:
    with open(os.path.join(dir_path, file), "r", encoding="utf-8") as f:
        content = f.read()
        
    # Find all mermaid blocks
    mermaid_blocks = re.findall(r"```mermaid\n(.*?)\n```", content, re.DOTALL)
    
    for i, block in enumerate(mermaid_blocks):
        # Look for common errors:
        # 1. Unquoted parentheses in node labels e.g. A[Label (Extra)]
        # 2. Invalid arrow types like -> instead of -->
        
        errors = []
        for line_num, line in enumerate(block.split("\n")):
            line = line.strip()
            
            # check for -> instead of -->
            if re.search(r"[^-]->", line):
                errors.append(f"Line {line_num+1}: Suspicious arrow -> instead of -->")
                
            # check for unquoted parentheses in bracket labels
            # Matches roughly: A[Something (bad)]
            if re.search(r"\[[^\"\]]*\(", line):
                errors.append(f"Line {line_num+1}: Unquoted parenthesis in node label")
                
            # check for unquoted brackets inside brackets
            if re.search(r"\[[^\"\]]*\[", line):
                errors.append(f"Line {line_num+1}: Unquoted bracket in node label")
                
        if errors:
            print(f"--- Suspicious Mermaid in {file} ---")
            for e in errors:
                print(e)
            print("Block snippet:")
            print("\n".join(block.split("\n")[:5]))
            print("...")
            print()
