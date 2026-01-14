"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:24
🚀 Status: ACTIVE / PRODUCTION
"""

import difflib
import hashlib
import json
import os
from collections import defaultdict


def get_hash(filename):
    hasher = hashlib.sha256()
    with open(filename, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def get_similarity(file1, file2):
    with open(file1, 'r', encoding='utf-8', errors='ignore') as f1, \
         open(file2, 'r', encoding='utf-8', errors='ignore') as f2:
        content1 = f1.read()
        content2 = f2.read()
        return difflib.SequenceMatcher(None, content1, content2).ratio()

def main():
    with open('nexus_files_info.json', 'r') as f:
        files_info = json.load(f)

    # Exact duplicates
    hashes = defaultdict(list)
    for info in files_info:
        path = info['FullName']
        if os.path.exists(path):
            h = get_hash(path)
            hashes[h].append(path)
    
    exact_duplicates = [paths for paths in hashes.values() if len(paths) > 1]

    # Similarity check
    # We only compare files that are not already identified as exact duplicates
    # and have similar sizes to optimize.
    similar_files = []
    processed_files = set()
    for paths in hashes.values():
        processed_files.update(paths)
    
    all_paths = [info['FullName'] for info in files_info if os.path.exists(info['FullName'])]
    
    # Sort by size to compare neighbors
    files_by_size = sorted(files_info, key=lambda x: x['Length'])
    
    for i in range(len(files_by_size)):
        if i % 30 == 0:
            print(f"Processing file {i}/{len(files_by_size)}...")
        for j in range(i + 1, min(i + 50, len(files_by_size))): # Increased window to 50
            f1 = files_by_size[i]['FullName']
            f2 = files_by_size[j]['FullName']
            
            # Skip if they are the same file or already found as exact duplicates
            if f1 == f2: continue
            
            # Check if they are already in the same exact duplicate group
            is_dup = False
            for dup_group in exact_duplicates:
                if f1 in dup_group and f2 in dup_group:
                    is_dup = True
                    break
            if is_dup: continue

            # Size difference should be small
            size1 = files_by_size[i]['Length']
            size2 = files_by_size[j]['Length']
            if size1 == 0 or size2 == 0: continue
            
            if abs(size1 - size2) / max(size1, size2) > 0.1:
                break # Too different in size
            
            sim = get_similarity(f1, f2)
            if sim > 0.85:
                similar_files.append((f1, f2, sim))

    results = {
        "exact_duplicates": exact_duplicates,
        "similar_files": similar_files
    }
    
    with open('duplicate_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    main()
