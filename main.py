import re
from datasets import load_dataset

korean_postposition_regex = r'[에을를] [^ \t\n]+[한] '

ds = load_dataset("lcw99/wikipedia-korean-20240501", split="train", streaming=True)


def search_wikipedia(dataset, regex_pattern, limit=100):
    compiled_re = re.compile(regex_pattern)
    results = []

    print(f"Searching for matches...")
    for i, entry in enumerate(dataset):
        text = entry['text']
        matches = list(set(compiled_re.findall(text)))

        if matches:
            results.append({
                "title": entry['title'],
                "matches": matches,
                "context": text[:200] + "..."  # Snippet for verification
            })

        if len(results) >= limit:
            break

    return results


# 3. Execute search
found_items = search_wikipedia(ds, korean_postposition_regex)

# 4. Display results
candidates = set()
for item in found_items:
    print(f"Title: {item['title']}")
    print(f"Matches: {item['matches']}\n")
    candidates.update(item['matches'])

print(f"Candidates: {candidates}")