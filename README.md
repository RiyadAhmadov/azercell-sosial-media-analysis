# Azercell Sosial Media Analysis

!['Azercell'](https://fed.az/upload/news/995493.png)

## Project Overview

This project involves performing sentiment analysis on comments scraped from the Instagram account of The State Social Protection Fund (SSPF) of the Azerbaijan Republic. The analysis aims to categorize public sentiment and provide insights into how the fund's activities and posts are perceived by the public.

## Data

The dataset used for this project includes the following columns:

- **Rəy**: The comment or feedback text from the post.
- **Bəyənmə_Sayı**: The number of likes the post received.
- **Paylaşımın_Məzmunu**: The content or description of the post.
- **Hesab_Adı**: The username of the account that posted the comment.
- **Paylaşımın_Tarix**: The date the post was published.
- **Paylaşımın_Zamanı**: The time the post was published.

## Methodology

1. **Data Collection**: Comments were scraped from the official Instagram account of SSPF using web scraping techniques.
2. **Data Preprocessing**: The scraped data was cleaned and organized into a structured DataFrame for analysis.
3. **Sentiment Analysis**: A sentiment analysis model was applied to the `Rəy` column to classify the comments as positive, negative, or neutral.
4. **Visualization**: The results of the sentiment analysis were visualized using Power BI to provide a clear understanding of the public's sentiment towards SSPF's activities.

## Tools and Technologies

- **Python**: Used for data scraping, cleaning, and sentiment analysis.
- **Power BI**: Used for data visualization and presenting the results.
- **Pandas**: For handling and preprocessing data.
- **Natural Language Processing (NLP)**: Techniques used for sentiment analysis.

## Results

The analysis provides insights into the general sentiment of the public regarding the SSPF's activities. The visualizations in Power BI highlight the distribution of sentiments across different posts and over time.

## How to Run the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/RiyadAhmadov/azercell-sosial-media-analysis.git
   ```
   
## Conclusion

This project demonstrates the application of sentiment analysis to social media comments, providing valuable insights into public opinion regarding a government fund's activities. The results can help inform the fund's communication strategies and improve its engagement with the public.
