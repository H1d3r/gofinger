import json

def deduplicate_fingerprints(input_file, output_file):
    """
    Reads a fingerprint JSON file, removes duplicate fingerprints, and saves the result to a new file.

    A fingerprint is considered a duplicate if the "cms", "method", "location", and "keyword" fields are identical.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing the input file: {e}")
        return

    fingerprints = data.get('fingerprint', [])
    if not fingerprints:
        print("No fingerprints found in the file.")
        return

    unique_fingerprints = []
    seen_fingerprints = set()

    for fingerprint in fingerprints:
        # Create a unique, hashable key for each fingerprint based on its contents
        try:
            fingerprint_key = (
                fingerprint.get('cms'),
                fingerprint.get('method'),
                fingerprint.get('location'),
                # Keywords are sorted to ensure that the order doesn't matter
                tuple(sorted(fingerprint.get('keyword', [])))
            )
        except (AttributeError, TypeError):
            # Skip fingerprints that don't have the expected structure
            continue

        if fingerprint_key not in seen_fingerprints:
            unique_fingerprints.append(fingerprint)
            seen_fingerprints.add(fingerprint_key)

    # Create the new JSON structure with the unique fingerprints
    new_data = {'fingerprint': unique_fingerprints}

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"Error writing the output file: {e}")
        return

    num_removed = len(fingerprints) - len(unique_fingerprints)
    print(f"Successfully removed {num_removed} duplicate fingerprints.")
    print(f"The unique fingerprints have been saved to: {output_file}")

if __name__ == '__main__':
    # Absolute paths for the input and output files
    input_path = r"D:\BaiduSyncdisk\huaimeng\hack\tools\前期渗透\1信息收集\指纹\1Finger\go版本\1finger-go 0.4 优化模块化测试\library\finger.json"
    output_path = r"D:\BaiduSyncdisk\huaimeng\hack\tools\前期渗透\1信息收集\指纹\1Finger\go版本\1finger-go 0.4 优化模块化测试\library\finger_unique.json"
    
    deduplicate_fingerprints(input_path, output_path)