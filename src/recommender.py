from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Parse a songs CSV and return a list of dicts with typed numeric fields."""
    import csv
    import os
    if not os.path.isabs(csv_path) and not os.path.exists(csv_path):
        csv_path = os.path.join(os.path.dirname(__file__), '..', csv_path)
    songs = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Return a (score, reasons) tuple rating how well a song matches user preferences."""
    import math

    score = 0.0
    reasons = []

    # 1. Genre match: +2.0
    if song.get('genre') == user_prefs.get('favorite_genre'):
        score += 2.0
        reasons.append('genre match (+2.0)')

    # 2. Mood match: +1.0
    if song.get('mood') == user_prefs.get('favorite_mood'):
        score += 1.0
        reasons.append('mood match (+1.0)')

    # 3. Acoustic match: +0.5
    # likes_acoustic=True favors high acousticness (>0.5), False favors low
    if user_prefs.get('likes_acoustic') and song.get('acousticness', 0) > 0.5:
        score += 0.5
        reasons.append('acoustic match (+0.5)')
    elif not user_prefs.get('likes_acoustic') and song.get('acousticness', 0) <= 0.5:
        score += 0.5
        reasons.append('acoustic match (+0.5)')

    def gaussian(song_val: float, target: float, sigma: float) -> float:
        return math.exp(-((song_val - target) ** 2) / (2 * sigma ** 2))

    # 4. Energy proximity: up to +1.0 (sigma=0.2 on 0-1 scale)
    energy_pts = round(gaussian(song.get('energy', 0), user_prefs.get('target_energy', 0.5), 0.2), 2)
    score += energy_pts
    reasons.append(f'energy proximity (+{energy_pts})')

    # 5. Valence proximity: up to +0.5 (sigma=0.2 on 0-1 scale)
    valence_pts = round(gaussian(song.get('valence', 0), user_prefs.get('target_valence', 0.5), 0.2) * 0.5, 2)
    score += valence_pts
    reasons.append(f'valence proximity (+{valence_pts})')

    # 6. Tempo proximity: up to +0.5 (sigma=20 on BPM scale)
    tempo_pts = round(gaussian(song.get('tempo_bpm', 0), user_prefs.get('target_tempo', 120), 20) * 0.5, 2)
    score += tempo_pts
    reasons.append(f'tempo proximity (+{tempo_pts})')

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs against user preferences and return the top k as (song, score, explanation)."""
    scored = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [(song, score, ', '.join(reasons)) for song, score, reasons in scored[:k]]
