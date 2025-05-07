import argparse
import requests
import csv
import sys
import re

api_key = "YOUR_API_KEY"

def v2_search(query: str, page: int, size: int, wildcard: bool, regex: bool, de_dupe: bool) -> dict:
    res = requests.post("https://api.dehashed.com/v2/search", json={
        "query": query,
        "page": page,
        "size": size,
        "wildcard": wildcard,
        "regex": regex,
        "de_dupe": de_dupe,
    }, headers={
        "Content-Type": "application/json",
        "DeHashed-Api-Key": api_key,
    })

    if res.status_code != 200:
        print(f"Error: {res.status_code} - {res.text}", file=sys.stderr)
        sys.exit(1)
    return res.json()

def sanitize_filename(domain: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', domain)

def write_to_csv(results, domain):
    fields_to_keep = {
        "id": "id",
        "name": "name",
        "email": "email",
        "database": "database_name",
        "username": "username",
        "hashed_password": "hashed_password",
        "password": "password"
    }

    filename = f"dehashed_{sanitize_filename(domain)}.csv"

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields_to_keep.keys())
        writer.writeheader()

        for entry in results:
            filtered = {}
            for col, key in fields_to_keep.items():
                val = entry.get(key, "")
                if isinstance(val, list):
                    val = ", ".join(val)
                filtered[col] = val
            writer.writerow(filtered)

    print(f"\n✅ Results saved to {filename}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Search DeHashed API for a domain")
    parser.add_argument('--domain', type=str, required=True, help='Domain to search (e.g. example.com)')
    parser.add_argument('--size', type=int, default=100, help='Results per page (max 100)')
    parser.add_argument('--wildcard', action='store_true', help='Enable wildcard matching')
    parser.add_argument('--regex', action='store_true', help='Enable regex matching')
    parser.add_argument('--dedupe', action='store_true', help='De-duplicate results')
    parser.add_argument('--max-pages', type=int, default=None, help='Maximum number of pages to fetch')  

    args = parser.parse_args()
    cleaned_domain = args.domain.lstrip('@')
    search_query = f"domain:{cleaned_domain}"

    page = 1
    all_results = []

    print(f"🔍 Searching DeHashed for {search_query}...")

    while True:
        if args.max_pages is not None and page > args.max_pages:
            print(f"⛔ Reached max page limit: {args.max_pages}")
            break
            
        response = v2_search(
            query=search_query,
            page=page,
            size=args.size,
            wildcard=args.wildcard,
            regex=args.regex,
            de_dupe=args.dedupe
        )

        entries = response.get("entries", [])
        if not entries:
            break

        all_results.extend(entries)
        print(f"Fetched page {page}, total so far: {len(all_results)}")
        page += 1

    print(f"\n📦 Total records fetched: {len(all_results)}")
    write_to_csv(all_results, cleaned_domain)
