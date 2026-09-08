import os
import glob

dir_path = r"C:\Users\Kyle\Downloads\pelnets\2022"

for i in range(1, 9):
    md_path = os.path.join(dir_path, f"2022S_FE-B_{i}.md")
    if not os.path.exists(md_path):
        continue
        
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace internal headers # 2022S_FE-B_Q1 to # 2022S_FE-B_1
    new_content = content.replace(f"# 2022S_FE-B_Q{i}\n", f"# 2022S_FE-B_{i}\n")
    new_content = new_content.replace(f"# 2022S_FE-B_Q{i}\r\n", f"# 2022S_FE-B_{i}\n")
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print(f"Fixed {md_path}")
