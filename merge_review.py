import json
import re
import glob
import sys

target_dir = sys.argv[1]

data = {}
for f in glob.glob(f'{target_dir}/review_*.json'):
    try:
        with open(f, 'r', encoding='utf-8') as file:
            txt = file.read()
        try:
            data.update(json.loads(txt))
        except json.decoder.JSONDecodeError as e:
            print(f"Fixing {f}")
            txt = re.sub(r'(?<!\\)\\(?![\\"/bfnrtu])', r'\\\\', txt)
            with open(f, 'w', encoding='utf-8') as file:
                file.write(txt)
            data.update(json.loads(txt))
    except Exception as e:
        print(f'{f} failed: {e}')

with open(f'{target_dir}/review.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"Merged {len(data)} items into {target_dir}/review.json")
