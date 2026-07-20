try:
    from textblob import TextBlob
except ImportError:
    class DummyBlob:
        def __init__(self, text):
            self.text = text.lower()
            self.sentiment = self._analyze()
            
        def _analyze(self):
            pos_words = ['good', 'great', 'awesome', 'excellent', 'happy', 'love']
            neg_words = ['bad', 'terrible', 'awful', 'sad', 'hate', 'worst']
            score = 0
            for w in self.text.split():
                if w in pos_words: score += 1
                if w in neg_words: score -= 1
                
            class Polarity:
                def __init__(self, s): self.polarity = s
            return Polarity(score * 0.5)
            
    TextBlob = DummyBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0.1:
        return "Positive", polarity
    elif polarity < -0.1:
        return "Negative", polarity
    else:
        return "Neutral", polarity

if __name__ == '__main__':
    reviews = [
        "I absolutely love this movie! It was fantastic.",
        "The plot was terrible and the acting was awful.",
        "It was an okay movie, nothing special but not bad."
    ]
    
    for r in reviews:
        sentiment, score = analyze_sentiment(r)
        print(f"Review: '{r}'\n-> Sentiment: {sentiment} (Score: {score:.2f})\n")
        
    user_text = input("Enter a movie review or tweet: ")
    sentiment, score = analyze_sentiment(user_text)
    print(f"-> Sentiment: {sentiment} (Score: {score:.2f})")
