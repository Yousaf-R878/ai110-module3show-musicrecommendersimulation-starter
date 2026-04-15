# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **Musiscore 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate 
    It generates a list of song recommendations based on user preferences.
- What assumptions does it make about the user  
    It assumes that the energy/vibe of the song is the most important aspect of a song for the user
- Is this for real users or classroom exploration  
    Classroom exploration

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)
    Each song is described by six values: genre, mood, energy, valence, tempo, and acousticness. The catalog also stores danceability, but the scorer does not currently use it.

- What user preferences are considered
    Each user tells the system six things: their favorite genre, their favorite mood, a target energy level (0–1), a target valence level (0–1), a preferred tempo in BPM, and a yes/no on whether they like acoustic-sounding music.

- How does the model turn those into a score
    The model adds up points across six categories with a maximum total of 5.5 points. Genre match and mood match are each worth 1.0 point, you either get it or you don't. Acoustic preference is worth 0.5 points the same way. Energy proximity is worth up to 2.0 points, valence proximity up to 0.5, and tempo proximity up to 0.5. The three proximity scores use a bell curve so songs close to the user's target earn nearly full points and songs far away earn close to zero — it fades gradually rather than cutting off sharply. The song with the highest total is recommended first.

- What changes did you make from the starter logic
    I changed the weights/important of the energy and genre so that matching genres didnt have the most significance for recommendations


---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
    18
- What genres or moods are represented
    Genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, country, classical, hip-hop, r&b, metal, reggae, folk, edm
- Did you add or remove data  
    Yes
- Are there parts of musical taste missing in the dataset  
    Yes, there are so many more songs that exist in the world, and this dataset captures a very small amount of music and music variety that exists.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results
    The system works best for lofi fans and pop fans as their favorite genre exists more than once in the catalog. Additionally, the system works well for users with strong energy preferences at the high and low ends. 

- Any patterns you think your scoring captures correctly
    The bell-curve proximity scoring does a good job of rewarding "close but not exact" matches instead of treating them as failures. A song that is 0.1 away from the user's target energy still earns about 88% of the maximum energy points, which feels fair. The system also correctly separates users who want acoustic music from those who do not.

- Cases where the recommendations matched your intuition
    The Perfect Clone test confirmed that when a user's preferences match a song almost exactly, that song scores near the maximum (5.50 out of 5.5) and sits far ahead of everything else. The Late-Night Coder and Sunday Morning profiles also produced results that made immediate sense: quiet, slow, acoustic-leaning songs rose to the top for both, with genre being the signal that correctly separated lofi from jazz.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 
One weakness I discovered during my experiments was the fact that 13 out of the 15 genres in my csv have only 1 song. This made it so that the +1.0 genre bonus fired at most once and then the catalog got exhausted. Meaning, the rest of their recommendations are pulled from the wrong genre, but since the data set is so small, it gives the illusion of diversity.
Prompts:  


---

## 7. Evaluation

### Profiles Tested

Nine user profiles were run through my recommender — three "standard" profiles representing everyday listeners, and six adversarial profiles designed specifically to find weaknesses in the scoring logic.

Standard profiles:
- Hype Gym-Goer — high-energy pop fan who wants intense, fast music
- Late-Night Coder — prefers mellow lofi with a chill mood while working
- Sunday Morning — laid-back jazz listener who likes acoustic, relaxed songs

Adversarial profiles:
- Ghost Genre — requests "k-pop," a genre that does not exist in the catalog
- Acoustic Contradiction — says they like acoustic music but also wants the highest-possible energy and a metal/angry mood
- Perfect Clone — preferences copied exactly from the song "Gym Hero" to test whether a near-perfect match actually scores near the maximum
- Genre–Mood Mismatch — requests "metal" genre with a "chill" mood, a combination no song in the catalog has
- All-Zeros Extremist — sets every numeric target to zero to see what happens when the math collapses at extreme values
- Boundary Tester — an R&B fan who says they like acoustic music, designed to expose a known edge case where the acoustic check uses a strict cutoff

--

### What Was Surprising

Gym Hero keeps showing up for the wrong people. Even when a user's genre and mood preferences don't match pop or intense, Gym Hero still climbs into the top 5 for many profiles because its energy (0.93) is close to the catalog's most popular energy range. Since energy is now worth up to 2.0 points, a song with near-perfect energy can outscore songs that actually match the user's stated genre. This is the clearest sign that energy weight dominates the system after the rebalancing.


The acoustic bonus can be completely irrelevant to the winner. The Acoustic Contradiction profile asked for acoustic-sounding music but also wanted metal energy and an angry mood. Iron Hymn — the only metal/angry song — won with a score of 5.00 despite having an acousticness of 0.04, one of the lowest in the entire catalog. The acoustic bonus never fired on the #1 result because genre + mood + energy overpowered it.


 The All-Zeros Extremist profile set every numeric target to zero. The valence and tempo proximity scores both returned +0.00 for almost every song because the math curve drops off so steeply. The only thing that saved the results was that the user's genre (classical) and mood (peaceful) matched Raindrop Sonata exactly, which pushed it far ahead of the pack on categorical bonuses alone.



---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences
    Add danceability as a scored signal — it is already in the catalog but currently ignored.

- Better ways to explain recommendations
    Show which single signal contributed the most to each song's score, so the user knows if they got a result because of genre, energy, or something else.

- Improving diversity among the top results
    Cap the top 5 to at most two songs per genre so the list does not stack with near-identical tracks.

- Handling more complex user tastes
    Let users set an energy range instead of a single target, which would help listeners who want both calm and loud music depending on context.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
    
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
