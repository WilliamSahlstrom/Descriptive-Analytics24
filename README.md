# Web Scraping and Sentiment Analysis Project

This project consists of two main Python scripts, `Retrieval.py` and `Analysis.py`, designed to scrape web archives for article headlines, analyze sentiment, and visualize word frequency through word clouds. The project aims to extract insights from headlines over specific periods, particularly focusing on March 2020 and March 2022.

## Table of Contents

- [Retrieval.py](#retrievalpy)
- [Analysis.py](#analysispy)
- [Dashboard.py](#dashboardpy)
- [Results](#results)
- [Data Sample](#data-sample)

## Retrieval.py

This script is responsible for fetching URLs from web archives and scraping headlines from those URLs. The main functions include:

- `get_archive_urls(base_url, from_date, to_date, limit)`: Fetches archive URLs within a specified date range and limit. The function includes error handling for HTTP requests and JSON parsing.
- `get_article_data(url)`: Scrapes the article headline from the given URL using BeautifulSoup for HTML parsing. It includes fallback mechanisms for different HTML structures.
- `save_to_csv(data, filename)`: Saves the collected headlines and their publication dates to a CSV file.
- `main()`: Orchestrates the retrieval process, including specifying base URLs and date ranges for scraping.

The script handles HTTP errors, JSON parsing issues, and duplicates to ensure a clean dataset for analysis.

## Analysis.py

This script analyzes the scraped headlines for sentiment and visualizes the most frequent words through word clouds. The main components include:

- `_clean(text)`: Cleans and preprocesses text by removing non-alphabetic characters, converting to lowercase, stemming, and removing stopwords.
- `do_wordclouds(df, period, results_path)`: Generates word clouds for headlines in a specified period and saves the images. It also identifies the most frequent word in the period.
- `calculate_sentiment_scores(df, period)`: Calculates the average Vader sentiment compound score for headlines in a specified period, excluding zero values to aim for a more accurate average.
- `add_vader_scores_to_csv(df, results_path)`: Adds Vader sentiment scores to each headline in the dataset and saves the updated data to a CSV file.
- `main()`: Executes the analysis, including loading the data, performing sentiment analysis, generating word clouds, and saving the results.

The script utilizes the Vader Sentiment Analysis tool for sentiment analysis and the WordCloud library for visualizing word frequency.

## Dashboard.py

This script uses the Dash library to create a simple web-based dashboard for visualizing sentiment scores over time and comparing the differences in sentiment scores between the two periods (March 2020 and March 2022). The dashboard includes:

- A bar chart displaying the average Vader compound score over time.
- A bar chart comparing the sentiment scores between the two specified periods.

### Results

The results can be viewed in the results folder.

### Data Sample

A small sample of web scraped headlines includes various topics, indicating the diversity of news coverage in the specified periods.

| MM/YYYY  | Headline                                                |
|----------|---------------------------------------------------------|
| 03/2020  | Why the US is so vulnerable to coronavirus outbreak     |
| 03/2020  | Chinese group in talks to aid struggling jet maker Bombardier |
| 03/2020  | Steelmaking operation rolls out in Wales               |
| ...      | ...                                                     |
