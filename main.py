import os
import re
from konlpy.tag import Mecab
from datasets import load_dataset, load_from_disk
from collections import defaultdict

# Initialize MeCab
mecab = Mecab()


def load_iterable_data():
    if not os.path.exists('data_cache'):
        ds = load_dataset("lcw99/wikipedia-korean-20240501", split="train")
        ds.save_to_disk('data_cache')
    return load_from_disk('data_cache').to_iterable_dataset(num_shards=1024)


def analyze_mwp_candidates(dataset, limit_docs=1000):
    """
    Returns two dictionaries:
    - candidates: frequency of { (particle, root): count }
    - negatives: frequency of { root_with_shikida: count }
    """
    candidates = defaultdict(int)
    shikida_usage = defaultdict(int)
    examples = defaultdict(list)

    print(f"Processing {limit_docs} documents...")

    for i, entry in enumerate(dataset):
        if i >= limit_docs: break

        text = entry['text']
        pos = mecab.pos(text)

        for j in range(len(pos) - 2):
            # 1. Search for: [Particle] + [Root] + [한/ㄴ/은]
            # Particles: 에(JKB), 을/를(JKO), 로(JKB)
            if pos[j][1] in ['JKB', 'JKO'] and pos[j][0] in ['에', '을', '를', '로']:
                # Look at the next morph (The root) and the one after (The ending)
                root = pos[j + 1][0]
                ending = pos[j + 2][0]
                ending_tag = pos[j + 2][1]

                if ending == '한' or (ending_tag == 'ETM' and 'ㄴ' in ending):
                    phrase = f"{pos[j][0]} {root}{ending}"
                    candidates[(pos[j][0], root)] += 1
                    if len(examples[phrase]) < 2:
                        examples[phrase].append(entry['title'])

            # 2. Negative Constraint: Search for Root + 시키다 (XSV)
            # This helps identify if the root is a productive verb
            if pos[j + 1][1] == 'XSV' and pos[j + 1][0].startswith('시키'):
                root_potential = pos[j][0]
                shikida_usage[root_potential] += 1

    return candidates, shikida_usage, examples


def main():
    ds = load_iterable_data()
    candidates, shikida_usage, examples = analyze_mwp_candidates(ds, limit_docs=2000)

    print(f"\n{'Resulting MWP Candidate':<20} | {'Root':<10} | {'Shikida-Count'}")
    print("-" * 60)

    for (part, root), count in sorted(candidates.items(), key=lambda x: x[1], reverse=True):
        full_phrase = f"{part} {root}한"
        s_count = shikida_usage.get(root, 0)

        # Negative Constraint Filter:
        # If the root appears with '시키다' more than once, it's likely a normal verb.
        # MWPs like '대' (from 대한) almost never appear as '대시키다'.
        is_mwp = "True" if s_count == 0 else "False (Verb)"

        if count > 2:  # Show only significant patterns
            print(f"{full_phrase:<20} | {root:<10} | {s_count:<5} | {is_mwp}")


if __name__ == "__main__":
    main()