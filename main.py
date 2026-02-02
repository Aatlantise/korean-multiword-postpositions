import os
from collections import defaultdict
from konlpy.tag import Mecab
from datasets import load_from_disk, load_dataset
import csv
import json

mecab = Mecab()


def load_iterable_data():
    if not os.path.exists('data_cache'):
        ds = load_dataset("lcw99/wikipedia-korean-20240501", split="train")
        ds.save_to_disk('data_cache')
    return load_from_disk('data_cache').to_iterable_dataset(num_shards=1024)


def extract_adpositional_mwe(pos_data):
    candidates = []
    n = len(pos_data)

    # Forms of 'Hata' to look for (add more as needed!)
    # We use this for both checking the end of a fused root AND matching a standalone token.
    hata_forms = ['한', '하', '할', '했', '해', '함']

    for i in range(n - 1):
        # --- Step 0: Anchor on the Josa ---
        josa_m, josa_t = pos_data[i]

        # Must be a particle (J*)
        if not josa_t.startswith('J'):
            continue

        # Stop if we are at the end of the sentence
        if i + 1 >= n: break

        root_m, root_t = pos_data[i + 1]

        # --- Case 1: The Fused Root (Hata is inside) ---
        # Logic: The root word itself ends with one of our hata forms.
        # Example: ('에', 'JKB'), ('관한', 'VV+ETM') -> '관한' ends with '한'

        # We assume the root must be some kind of content word (VV, NNG, XR)
        # We also allow compound tags like 'VV+ETM' here.
        if any(root_t.startswith(t) for t in ["VV", "NNG", "XR", "NNP"]):

            # Check if the surface form ends with a known hata form
            # e.g. "관한" ends with "한"
            if any(root_m.endswith(h) for h in hata_forms):
                candidates.append({
                    "mwe": f"{josa_m} {root_m}",
                    "pattern": "fused_root",
                    "josa": josa_m,
                    "root": root_m[0],
                    "eomi": root_m[1:],
                    "tokens": [pos_data[i], pos_data[i + 1]]
                })
                continue  # If we found a fused match, we don't need to check split

        # --- Case 2: The Split Root (Hata is the next word) ---
        # Logic: The root is just a noun/root, and the NEXT token is the hata form.
        # Example: ('에', 'JKB'), ('근거', 'NNG'), ('한', 'XSV+ETM')

        if i + 3 < n:
            next_m, next_t = pos_data[i + 2]
            subsequent_m, subsequent_t = pos_data[i + 3]

            # Does the NEXT token match our list? (e.g. is it '한', '해', '해서'?)
            if next_m[0] in hata_forms:
                candidates.append({
                    "mwe": f"{josa_m} {root_m}{next_m}{subsequent_m}",
                    "josa": josa_m,
                    "root": root_m,
                    "eomi": next_m + subsequent_m,
                    "pattern": "split_next",
                    "tokens": [pos_data[i], pos_data[i + 1], pos_data[i + 2]]
                })

    return candidates


def filter_stats(stats_dict, threshold=10):
    """
    Filters a nested dictionary, keeping only inner entries with values >= threshold.
    Also removes the root key if no inner entries remain.
    """
    filtered_result = {}

    for root, sub_dict in stats_dict.items():
        # Create a new sub-dictionary with only the frequent items
        new_sub_dict = {k: v for k, v in sub_dict.items() if v >= threshold}

        # Only add the root to the result if it still has data
        if new_sub_dict:
            filtered_result[root] = new_sub_dict

    return filtered_result


def analyze_lexicalization(dataset, limit_docs=None):
    # root -> {mwe: count}
    mwe_stats = defaultdict(lambda: defaultdict(int))
    josa_stats = defaultdict(lambda: defaultdict(int))
    eomi_stats = defaultdict(lambda: defaultdict(int))

    if limit_docs is not None:
        print(f"Analyzing {limit_docs} documents for MWE candidates...")
    else:
        print("Analyzing all documents for MWE candidates...")

    for i, entry in enumerate(dataset):
        if limit_docs and i >= limit_docs: break
        pos = mecab.pos(entry['text'])


        candidates = extract_adpositional_mwe(pos)

        for candidate in candidates:
            root = candidate['root']

            if root in ['한', '하', '할', '했', '해', '함']:
                continue

            josa = candidate['josa']
            eomi = candidate['eomi']
            mwe = candidate['mwe'].strip(".")
            mwe_stats[root][mwe] += 1
            josa_stats[root][josa] += 1
            eomi_stats[root][eomi] += 1

    return filter_stats(mwe_stats), filter_stats(josa_stats), filter_stats(eomi_stats)


def main():
    ds = load_iterable_data()
    mwe_stats, josa_stats, eomi_stats = analyze_lexicalization(ds)

    print(f"\n{'Root':<10} | {'Total':<6} | {'# Josa':<8} | {'# Eomi':<8} | {'# MWEs':<8}")
    print("-" * 65)

    results = []
    for root in mwe_stats:
        total_occurrences = sum(mwe_stats[root].values())
        josa_count = len(josa_stats[root])  # How many josa precede this root
        eomi_count = len(eomi_stats[root])
        mwe_count = len(mwe_stats[root])
        mwe_ex = [k for k, v in mwe_stats[root].items()]
        results.append(
            [
                root, total_occurrences, josa_count, eomi_count, mwe_count, mwe_ex
            ]
        )

    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

    # Sort by Fossilization Ratio
    for res in sorted_results:
        root, total_occurrences, josa_count, eomi_count, mwe_count, mwe_ex = res
        # if total_occurrences > 300 and eomi_count < 20:
        print(f"{root:<10} | {total_occurrences:<6} | {josa_count:<8} | {eomi_count:<8} | {mwe_count:<8} | {', '.join(mwe_ex)}")

    output_filename = "mwe_analysis_results.csv"

    with open(output_filename, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)

        # Write the Header
        writer.writerow(['Root', 'Total Occurrences', 'Josa Count', 'Eomi Count', 'MWE Count', 'MWE Examples'])

        # Write the Data
        for row in sorted_results:
            root, total, josa_c, eomi_c, mwe_c, mwe_ex_list = row

            # Join the list of examples into a single string separated by commas
            mwe_ex_str = ", ".join(mwe_ex_list)

            writer.writerow([root, total, josa_c, eomi_c, mwe_c, mwe_ex_str])

    print(f"\nSuccessfully saved results to {output_filename}")


if __name__ == "__main__":
    main()