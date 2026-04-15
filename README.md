# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real world systems use both collaborative filtering and content-based filtering in order to create recommendations for their users. For example, real world systems like Youtube may use collaboritate filtering by recognizing patterns within a users behavior. For example, if two users watch similar videos, Youtube may suggest videos watched by one user to the other. On the other hand Spotify uses lots of content-based filtering by extracting metadata from songs as well as performing audio analysis in order to match songs based on their sound and audio cues, rather than simply based off patterns. These two coupled together create very robust recommendation systems. My version will mostly be focusing on content based filtering, as we're closely looking at music metadata in order to create recommendations for a user.

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
  Each song in my system uses the features of: Genre,
  mood, energy, tempo_bpm, valence, danceability, and acousticness. 
- What information does your `UserProfile` store
  Each UserProfile stores the users favorite_genre, the users favorite_mood, their target_energy for how energetic they want their music to be, likes_acoustic for whether they like produced or acoustic sounds, target_tempo for tempo preferences and target_valence, for valence preferences.
- How does your `Recommender` compute a score for each song
  To start, each song will get a score from 0-5.5, which will be calculated as follows:
  1. +2.0 points for a genre match
  2. +1.0 point for a mood match
  3. +.5 point for an acoustic match. high accousticness >0.5,  
  4. up to +1.0 point for matching energy via Gaussian Proximity formula
  5. up to +.5 point for matching valence via Gaussian Proximity formula
  6. up to +.5 point for matching tempo via Gaussian Proximity formula
  
  The final score is then calculated via a sum across all features.

- How do you choose which songs to recommend
  my `recommend_songs` function runs the `score_song` function on every song in the catalog, then:

1. Sorts all songs by score, highest first
2. Returns the top `k` results (default: 5)
3. Attaches an explanation string for each pick, describing why it matched

Any biases may occur due to the high weight of genre matching, where it could ignore good suggestions simply because the genre isnt the same.


You can include a simple diagram or bullet list if helpful.

Taste profile:

user_prefs = {
    "favorite_genre": "pop",
    "favorite_mood":  "happy",
    "target_energy":  0.80,   
    "likes_acoustic": False 
}

Gave this to AI and it suggested this for my user_perfs as my prior design was somewhat narrow and this can help without expanding the user_perfs too much:

user_prefs = {
    "favorite_genre": "pop",
    "favorite_mood":  "happy",
    "target_energy":  0.80, 
    "target_tempo":   120,   
    "target_valence": 0.80,   
    "likes_acoustic": False  
}

Recipe:
+2.0 points for a genre match
+1.0 point for a mood match
+0-1.0 point for energy match
Similarity points on acousticness and valence
(not used.)

![Design Visualization](./images/User%20Preference%20Song-2026-04-15-051903.png)
---

![Working Code](./images/Working%20SS.png)
---
### Profile screenshots
![Sunday Morning](./images/Sunday.png)
![Late-Night Coder](./images/Coder.png)
![Hype Gym-Goer](./images/Hype.png)
![Ghost Genre](./images/Mismatch1.png)
![Acoustic Contradiction](./images/Mismatch2.png)
![Perfect Clone](./images/Mismatch3.png)
![Genre–Mood Mismatch](./images/Mismatch4.png)
![All Zeros Extremist](./images/Mismatch5.png)
![The Boundary Tester](./images/Mismatch6.png)



## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

