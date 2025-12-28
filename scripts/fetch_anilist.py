"""Fetch popular anime from AniList and prepare a data file and images for seeding.

Usage: python scripts/fetch_anilist.py --count 150
"""
import os
import json
import argparse
import requests
from bs4 import BeautifulSoup

ANILIST_URL = "https://graphql.anilist.co"

QUERY = """
query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    media(sort: POPULARITY_DESC, type: ANIME) {
      id
      title { romaji english native }
      description
      episodes
      coverImage { large medium }
      genres
      status
      popularity
      siteUrl
    }
  }
}
"""


def slugify(name: str) -> str:
    slug = name.lower().strip().replace(" ", "-")
    slug = ''.join(c for c in slug if (c.isalnum() or c == '-'))
    return slug


def strip_html(html: str) -> str:
    if not html:
        return ''
    return BeautifulSoup(html, 'html.parser').get_text()


def download_image(url: str, dest_path: str) -> bool:
    try:
        r = requests.get(url, stream=True, timeout=15)
        r.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Failed to download image {url}: {e}")
        return False


def fetch_anime(count: int = 150) -> list:
    per_page = 50
    page = 1
    results = []
    seen_slugs = set()

    while len(results) < count:
        variables = {"page": page, "perPage": per_page}
        r = requests.post(ANILIST_URL, json={"query": QUERY, "variables": variables}, timeout=30)
        r.raise_for_status()
        data = r.json()
        media = data.get('data', {}).get('Page', {}).get('media', [])
        if not media:
            break

        for m in media:
            title = m['title'].get('romaji') or m['title'].get('english') or m['title'].get('native')
            if not title:
                continue
            base_slug = slugify(title)
            slug = base_slug
            if slug in seen_slugs:
                slug = f"{base_slug}-{m['id']}"
            seen_slugs.add(slug)

            desc = strip_html(m.get('description') or '')
            desc = (desc[:400] + '...') if len(desc) > 400 else desc

            anime = {
                'name': title,
                'slug': slug,
                'description': desc,
                'episodes_count': m.get('episodes'),
                'genres': m.get('genres', []),
                'cover': m.get('coverImage', {}).get('large') or m.get('coverImage', {}).get('medium'),
                'site_url': m.get('siteUrl'),
            }
            results.append(anime)
            if len(results) >= count:
                break

        page += 1
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=150, help='Number of anime to fetch')
    parser.add_argument('--out', default='data/anime_seed.json', help='Output JSON file')
    args = parser.parse_args()

    os.makedirs('data', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)

    print(f"Fetching top {args.count} anime from AniList...")
    anime_list = fetch_anime(args.count)
    print(f"Fetched {len(anime_list)} anime entries")

    # Download cover images
    for a in anime_list:
        if a.get('cover'):
            ext = os.path.splitext(a['cover'])[1].split('?')[0] or '.jpg'
            img_path = f"static/images/{a['slug']}{ext}"
            if not os.path.exists(img_path):
                ok = download_image(a['cover'], img_path)
                if ok:
                    # store relative path without leading 'static/'
                    a['local_image'] = img_path.replace('static/', '')
            else:
                a['local_image'] = img_path.replace('static/', '')

    # Save JSON in a format compatible with seed.py
    out = {'anime': []}
    for a in anime_list:
        out['anime'].append({
            'name': a['name'],
            'slug': a['slug'],
            'description': a['description'],
            'image': a.get('local_image'),
            'genres': a.get('genres', []),
            'episodes_count': a.get('episodes_count')
        })

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Wrote {args.out}")


if __name__ == '__main__':
    main()
