import os
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from wordcloud import WordCloud
import re
from collections import Counter

# For some reason my code did not analyze all article headlines, so I added some extra cleanup (see below) to at least slightly improve the Vader scores
def _clean(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    text_words = text.split()
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    new_list_words = []
    for ww in text_words:
        ww = ww.strip()
        new_word = ps.stem(ww)
        if new_word not in stop_words:
            new_list_words.append(new_word)
    text = ""
    for ww in new_list_words:
        text = f"{text} {ww}"
    return text

# I used the wordcloud way of presenting most frequent words
def do_wordclouds(df, period, results_path):
    headlines = df[df['MM/YYYY'] == period]['Headline']
    headlines_cleaned = ' '.join([_clean(headline) for headline in headlines])

    wc = WordCloud().generate(headlines_cleaned)
    wc.to_file(os.path.join(results_path, f"{period.replace('/', '_')}_wordcloud.jpg"))

    # Function for counting the frequency itself
    words = headlines_cleaned.split()
    word_counts = Counter(words)
    most_common_word, frequency = word_counts.most_common(1)[0]

    print(f"The most frequent word in {period} headlines is: {most_common_word} (Frequency: {frequency})")  # This prints the most frequent word for 03/2020 and 03/2022

# What might be noticeable from the new csv file is that a fair few of the headlines are missing a "real" Vader score and are just '0.0'
# To handle this I decided to calculate the averages using only non-zero values since this gives in my opinion a more true average. The extra cleanup I added at the start of the code also added some articles their Vader scores back which also increased the Vader scores
def calculate_sentiment_scores(df, period):
    headlines = df[df['MM/YYYY'] == period]['Headline']

    analyser = SentimentIntensityAnalyzer()
    compound_scores = []

    for headline in headlines:
        cleaned_headline = _clean(headline)
        compound_score = analyser.polarity_scores(cleaned_headline)['compound']
        if compound_score != 0.0:
            compound_scores.append(compound_score)

    if compound_scores:
        average_score = sum(compound_scores) / len(compound_scores)
        print(f"Average Vader compound score for {period}: {average_score}")
        return compound_scores
    else:
        print(f"No non-zero Vader compound scores found for {period}")
        return []

def add_vader_scores_to_csv(df, results_path):
    analyser = SentimentIntensityAnalyzer()
    vader_scores = []

    for headline in df['Headline']:
        cleaned_headline = _clean(headline)
        vader_score = analyser.polarity_scores(cleaned_headline)['compound']
        vader_scores.append(vader_score)

    df['Vader score'] = vader_scores
    df.to_csv(os.path.join(results_path, "article_texts_with_vader_scores.csv"), index=False)

def main():
    # Since the path definition is not really needed earlier than this, it is a bit later on in my code than "usually" when it has been right at the beginning
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, "data", "article_texts.csv")
    results_path = os.path.join(script_dir, "results")
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    df = pd.read_csv(data_path)

    period_1 = "03/2020"
    period_2 = "03/2022"

    # Calculations happening in the below functions. Also, the Vader score for each article is also added to a new csv file that is then saved in the 'results' folder
    avg_score_1 = calculate_sentiment_scores(df, period_1)
    avg_score_2 = calculate_sentiment_scores(df, period_2)

    do_wordclouds(df, period_1, results_path)
    do_wordclouds(df, period_2, results_path)

    add_vader_scores_to_csv(df, results_path)

if __name__ == "__main__":
    main()

# The average Vader compound scores are printed into the terminal and are (excluding 0 values):
# Average Vader compound score for 03/2020: 0.03833720930232557
# Average Vader compound score for 03/2022: 0.08239183673469389

# Also, the single most used word in each period is displayed separately; please see the word cloud .jpg files for a full visualization of the frequency
# The most frequent word in 03/2020 headlines is: coronavirus (Frequency: 9)
# The most frequent word in 03/2022 headlines is: us (Frequency: 7)
