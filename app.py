import os
from flask import Flask, render_template
from models import db, Anime, Episode

# Load config
from config import Config

app = Flask(__name__)
# Load base config and allow env overrides
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)

# Optional: Flask-Migrate if available (for db migrations)
try:
    from flask_migrate import Migrate
    migrate = Migrate(app, db)
except Exception:
    migrate = None

@app.route("/")
def home():
    anime_list = Anime.query.all()
    return render_template("home.html", anime_list=anime_list)

@app.route("/watch-order/<slug>")
def watch_order(slug):
    anime = Anime.query.filter_by(slug=slug).first_or_404()
    episodes = Episode.query.filter_by(anime_id=anime.id).order_by(Episode.episode_no).all()
    return render_template("watch_order.html", anime=anime, episodes=episodes)

@app.cli.command('remove-fillers')
def remove_fillers_cmd():
    """Delete filler episodes from the DB and clean related data files."""
    deleted = Episode.query.filter_by(type='filler').delete(synchronize_session=False)
    db.session.commit()
    print(f"Deleted {deleted} filler episodes from database.")

    import json, os

    # Clean MAL filler file by removing episodes marked as filler
    mf = 'data/mal_filler.json'
    if os.path.exists(mf):
        try:
            with open(mf, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for k, v in data.items():
                if isinstance(v, dict) and 'episodes' in v:
                    v['episodes'] = [ep for ep in v['episodes'] if not ep.get('filler')]
            with open(mf, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Cleaned {mf}")
        except Exception as e:
            print("Failed to clean mal_filler.json:", e)

    # Clear filler ranges (no longer used)
    fr = 'data/filler_ranges.json'
    if os.path.exists(fr):
        try:
            with open(fr, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            print(f"Cleared {fr}")
        except Exception as e:
            print("Failed to clear filler_ranges.json:", e)

    # Update import report counts
    report = 'data/filler_import_report.json'
    if os.path.exists(report):
        try:
            with open(report, 'r', encoding='utf-8') as f:
                r = json.load(f)
            r['marked_filler'] = 0
            with open(report, 'w', encoding='utf-8') as f:
                json.dump(r, f, ensure_ascii=False, indent=2)
            print("Updated filler_import_report.json")
        except Exception as e:
            print("Failed to update filler_import_report.json:", e)


if __name__ == "__main__":
    # For local development we ensure DB tables exist
    with app.app_context():
        db.create_all()
    debug = os.environ.get('FLASK_ENV') != 'production'
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port, debug=debug)
