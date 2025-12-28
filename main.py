import os
from collections import defaultdict
from konlpy.tag import Mecab
from datasets import load_from_disk, load_dataset
import json

mecab = Mecab()


def load_iterable_data():
    if not os.path.exists('data_cache'):
        ds = load_dataset("lcw99/wikipedia-korean-20240501", split="train")
        ds.save_to_disk('data_cache')
    return load_from_disk('data_cache').to_iterable_dataset(num_shards=1024)


def analyze_lexicalization(dataset, limit_docs=100000):
    # root -> {next_morph: count}
    root_stats = defaultdict(lambda: defaultdict(int))
    # root -> count of occurrences in the MWP pattern (e.g., '에 ... 한')
    mwp_pattern_count = defaultdict(int)

    print(f"Analyzing {limit_docs} documents for fossilization patterns...")

    for i, entry in enumerate(dataset):
        if i >= limit_docs: break
        pos = mecab.pos(entry['text'])



        for j in range(len(pos) - 2):
            if j == 0:
                continue
            root, tag = pos[j]
            josa = ""
            next_tag = ""

            # VV ETM/EC
            if tag == "VV" and len(root) >= 1:
                prev_morph, prev_tag = pos[j - 1]
                next_morph, next_tag = pos[j + 1]
                eomi = next_morph
                if prev_tag[0] == "J" and next_tag in ["ETM", "EC"]:
                    josa = prev_morph

            # VV+ETM / VV+EC
            elif tag in ["VV+ETM", "VV+EC"] and len(root) >= 1:
                prev_morph, prev_tag = pos[j - 1]
                eomi = root[-1]
                root = root[:-1]

                if prev_tag[0] == "J":
                    josa = prev_morph

            # NNG/XR XSV/XSA ETM/EC
            elif tag in ["NNG", "XR"] and len(root) >= 1:
                prev_morph, prev_tag = pos[j - 1]
                next_morph, next_tag = pos[j + 1]
                subsequent_morph, subsequent_tag = pos[j + 2]
                # check for josa
                if prev_tag[0] == "J":
                    josa = prev_morph

                # XSV ETM/EC
                if next_tag in ["XSV", "XSA"] and subsequent_tag in ["ETM", "EC"]:
                    eomi = next_morph + subsequent_morph
                # XSA+ETM/EC
                else:
                    eomi = next_morph

            # continue if not VV or NNG
            else:
                continue

            if len(root) <= 2:
                root_stats[root][eomi] += 1
                if josa in ['에', '을', '를', '로'] and eomi in ["한", "하여", "해", "하", "하는"]:
                    mwp_pattern_count[root] += 1

    return root_stats, mwp_pattern_count


def main():
    ds = load_iterable_data()
    root_stats, mwp_pattern_count = analyze_lexicalization(ds)

    print(f"\n{'Root':<10} | {'Total':<6} | {'Variety':<8} | {'Fossil-Ratio'} | {'Status'}")
    print("-" * 65)

    # Filter for roots that appeared at least 10 times in our target pattern
    important_roots = [r for r, count in mwp_pattern_count.items() if count > 10]

    results = []
    for root in important_roots:
        total_occurrences = sum(root_stats[root].values())
        variety_count = len(root_stats[root])  # How many different things follow this root
        fossil_ratio = mwp_pattern_count[root] / total_occurrences

        # Heuristic:
        # MWPs usually have high fossilized ratio and high frequency
        status = "MWP Candidate" if fossil_ratio > 0.3 and total_occurrences > 1000 else "Regular Verb/Noun"
        results.append((root, total_occurrences, variety_count, fossil_ratio, status))

    # Sort by Fossilization Ratio
    for res in sorted(results, key=lambda x: x[1], reverse=True):
        roots_of_interest = ["취", "속", "근거", "기반", "위시", "한", "처", "임", "반", "의거"]
        root, total_occurrences, variety_count, fossil_ratio, status = res
        if total_occurrences > 30000 or total_occurrences > 10000 and fossil_ratio > 0.1 or root in roots_of_interest:
            print(f"{root:<10} | {total_occurrences:<6} | {variety_count:<8} | {fossil_ratio:.2f}         | {status}")


if __name__ == "__main__":
    main()