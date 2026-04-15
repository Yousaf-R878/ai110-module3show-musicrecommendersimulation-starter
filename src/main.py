"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


USERS = {
    "Hype Gym-Goer": {
        "favorite_genre": "pop",
        "favorite_mood":  "intense",
        "target_energy":  0.95,
        "target_valence": 0.75,
        "target_tempo":   135,
        "likes_acoustic": False,
    },
    "Late-Night Coder": {
        "favorite_genre": "lofi",
        "favorite_mood":  "chill",
        "target_energy":  0.40,
        "target_valence": 0.58,
        "target_tempo":   78,
        "likes_acoustic": True,
    },
    "Sunday Morning": {
        "favorite_genre": "jazz",
        "favorite_mood":  "relaxed",
        "target_energy":  0.38,
        "target_valence": 0.70,
        "target_tempo":   90,
        "likes_acoustic": True,
    },

    # ── Adversarial / Edge-Case Profiles ──────────────────────────────────────

    # 1. Ghost Genre: genre not in the catalog — no song ever gets +2.0
    "Ghost Genre": {
        "favorite_genre": "k-pop",
        "favorite_mood":  "happy",
        "target_energy":  0.80,
        "target_valence": 0.85,
        "target_tempo":   120,
        "likes_acoustic": False,
    },

    # 2. Acoustic Contradiction: wants acoustic (+0.5) but also wants
    #    max energy/tempo — acoustic songs are low-energy, so the gaussian
    #    penalty fights the acoustic bonus
    "Acoustic Contradiction": {
        "favorite_genre": "metal",
        "favorite_mood":  "angry",
        "target_energy":  0.97,
        "target_valence": 0.18,
        "target_tempo":   168,
        "likes_acoustic": True,
    },

    # 3. Perfect Clone: preferences copied exactly from "Gym Hero" (song #5)
    #    energy=0.93, valence=0.77, tempo=132 — should approach max score
    "Perfect Clone (Gym Hero)": {
        "favorite_genre": "pop",
        "favorite_mood":  "intense",
        "target_energy":  0.93,
        "target_valence": 0.77,
        "target_tempo":   132,
        "likes_acoustic": False,
    },

    # 4. Genre–Mood Mismatch: genre="metal" + mood="chill" never co-occur
    #    in the catalog, so the two biggest bonuses can never both fire on
    #    the same song
    "Genre-Mood Mismatch": {
        "favorite_genre": "metal",
        "favorite_mood":  "chill",
        "target_energy":  0.60,
        "target_valence": 0.50,
        "target_tempo":   100,
        "likes_acoustic": False,
    },

    # 5. All-Zeros Extremist: gaussian targets at absolute minimums —
    #    tests whether very-quiet classical/ambient songs dominate purely
    #    on proximity, or whether categorical bonuses still matter
    "All-Zeros Extremist": {
        "favorite_genre": "classical",
        "favorite_mood":  "peaceful",
        "target_energy":  0.0,
        "target_valence": 0.0,
        "target_tempo":   0,
        "likes_acoustic": True,
    },

    # 6. Boundary Tester: likes_acoustic=True, but the acoustic check is
    #    strict (> 0.5). Velvet Hour has acousticness=0.44 — just below the
    #    cut. Does it still surface, and does it unfairly miss the +0.5 bonus?
    "Boundary Tester": {
        "favorite_genre": "r&b",
        "favorite_mood":  "romantic",
        "target_energy":  0.55,
        "target_valence": 0.76,
        "target_tempo":   88,
        "likes_acoustic": True,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in USERS.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\n" + "=" * 40)
        print(f"  {name}")
        print("=" * 40)
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n#{i}  {song['title']} by {song['artist']}")
            print(f"    Score : {score:.2f} / 6.00")
            print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}")
            print(f"    Why   : {explanation}")
        print("\n" + "=" * 40)


if __name__ == "__main__":
    main()
