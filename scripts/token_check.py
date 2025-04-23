#!/usr/bin/env python3
"""Token check script ensures utility code is within size budget."""
import json, os, sys
def main():
    contract_path = os.path.join(os.path.dirname(__file__), '..', 'utility_contract.json')
    try:
        with open(contract_path, 'r') as f:
            contract = json.load(f)
    except Exception as e:
        print(f"Failed to load utility_contract.json: {e}", file=sys.stderr)
        return 1
    size_budget = contract.get("size_budget", 0)
    total_size = 0
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as pf:
                    total_size += len(pf.read())
    print(f"Total code size: {total_size} bytes, budget: {size_budget} bytes")
    if total_size > size_budget:
        print("Size budget exceeded", file=sys.stderr)
        return 1
    return 0
if __name__ == '__main__':
    sys.exit(main())