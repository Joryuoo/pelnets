import os
import re
import shutil

def main():
    root_dir = r"C:\Users\Kyle\Downloads\pelnets"
    files_dir = os.path.join(root_dir, "Files")
    dummy_dir = os.path.join(root_dir, "unused_images_dummy")
    
    if not os.path.exists(files_dir):
        print(f"Directory not found: {files_dir}")
        return

    # Create the dummy directory if it doesn't exist
    if not os.path.exists(dummy_dir):
        os.makedirs(dummy_dir)

    # 1. Collect all image files in Files/ and map them to their full paths
    image_files_map = {}
    for root, _, files in os.walk(files_dir):
        # Skip the dummy directory if it happens to be inside Files
        if "unused_images_dummy" in root:
            continue
            
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_files_map[f] = os.path.join(root, f)
                
    print(f"Found {len(image_files_map)} image files in 'Files/' directory.")

    # 2. Collect all referenced images in .md files
    referenced_images = set()
    md_count = 0
    # regex for Obsidian image links: ![[image.png]]
    obsidian_regex = re.compile(r'!\[\[(.*?)\]\]')
    # regex for standard markdown links: ![alt](image.png)
    standard_regex = re.compile(r'!\[.*?\]\((.*?)\)')
    
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.lower().endswith('.md'):
                md_count += 1
                with open(os.path.join(root, f), 'r', encoding='utf-8', errors='ignore') as md_file:
                    content = md_file.read()
                    
                    # Find Obsidian embeds
                    for match in obsidian_regex.findall(content):
                        # Some links might have aliases like ![[image.png|100]]
                        img_name = match.split('|')[0].strip()
                        referenced_images.add(img_name)
                        
                    # Find standard embeds
                    for match in standard_regex.findall(content):
                        filename = os.path.basename(match.strip())
                        referenced_images.add(filename)
                        
    print(f"Scanned {md_count} markdown files and found {len(referenced_images)} unique image references.")
    
    # 3. Find unused images and move them
    unused_images = set(image_files_map.keys()) - referenced_images
    
    print(f"\n--- Moving Unused Images ({len(unused_images)}) ---")
    if unused_images:
        for img in sorted(unused_images):
            src_path = image_files_map[img]
            dest_path = os.path.join(dummy_dir, img)
            
            try:
                shutil.move(src_path, dest_path)
                print(f"Moved: {img}")
            except Exception as e:
                print(f"Failed to move {img}: {e}")
                
        print(f"\nSuccessfully moved {len(unused_images)} unused images to: {dummy_dir}")
    else:
        print("All images in the 'Files/' folder are currently being used!")

if __name__ == "__main__":
    main()
