import json
from models import db, Anime, Episode
from app import app

def slugify(name: str) -> str:
    return name.lower().strip().replace(' ', '-')

with app.app_context():
    # Ensure tables exist
    db.create_all()

    # Migration: add `image` column if missing (for simple dev DBs)
    try:
        from sqlalchemy import text
        result = db.session.execute(text("PRAGMA table_info('anime');"))
        cols = [row[1] for row in result.fetchall()]
        if 'image' not in cols:
            db.session.execute(text("ALTER TABLE anime ADD COLUMN image VARCHAR(200)"))
            db.session.commit()
            print('Added anime.image column to DB')
        if 'episodes' not in cols:
            db.session.execute(text("ALTER TABLE anime ADD COLUMN episodes INTEGER"))
            db.session.commit()
            print('Added anime.episodes column to DB')
        if 'genres' not in cols:
            db.session.execute(text("ALTER TABLE anime ADD COLUMN genres VARCHAR(300)"))
            db.session.commit()
            print('Added anime.genres column to DB')
    except Exception as e:
        print('Migration check failed or not necessary:', e)

    with open("data/anime_seed.json", "r") as f:
        data = json.load(f)
        for anime_data in data.get("anime", []):
            slug = anime_data.get("slug") or slugify(anime_data.get("name", ""))
            existing = Anime.query.filter_by(slug=slug).first()
            if existing:
                # Update missing fields (e.g., image or description) on existing records
                updated = False
                if anime_data.get('image') and not existing.image:
                    existing.image = anime_data.get('image')
                    updated = True
                if not existing.description and anime_data.get('description'):
                    existing.description = anime_data.get('description')
                    updated = True
                if anime_data.get('episodes_count') and not existing.episodes:
                    existing.episodes = anime_data.get('episodes_count')
                    updated = True
                if anime_data.get('genres') and not existing.genres:
                    existing.genres = ','.join(anime_data.get('genres', []))
                    updated = True
                if updated:
                    db.session.add(existing)
                    db.session.commit()
                    print(f"Updated existing anime with new data: {existing.name} ({slug})")
                else:
                    print(f"Skipping existing anime: {existing.name} ({slug})")
                continue

            anime = Anime(
                name=anime_data.get("name"),
                slug=slug,
                description=anime_data.get("description"),
                image=anime_data.get("image"),
                episodes=anime_data.get('episodes_count'),
                genres=','.join(anime_data.get('genres', [])) if anime_data.get('genres') else None
            )
            db.session.add(anime)
            db.session.commit()  # commit to get anime.id

            for ep in anime_data.get("episodes", []):
                episode = Episode(
                    anime_id=anime.id,
                    episode_no=ep["episode_no"],
                    title=ep["title"],
                    type=ep.get("type", "canon")
                )
                db.session.add(episode)

        db.session.commit()
    print("Database seeded successfully!")
