
 - Had meeting with Irina on Friday
 - I told her about what I had been doing so far
 - She suggested using the number of favorites/retweets as some sort of measure for sentiment which is not something I had considered
 -  She has also suggested focusing on logistics (3PL) companies like DHL

- Also had the datastream training
- Can get all sorts of finical information, most of which is over my head
- Going to focus on public companies and use stocks for now
- For private companies, could use finical news but going to focus on public now as that will be easier
- Have used datastream to pull a number of stock prices over a 2 year period for various top public logistics companies that have active Twitter accounts

- Hit my first roadblock so far
- I don't think my pipeline is going to work
- When someone replies to a tweet, they are unlikely to mention the concept/entity/keyword analyzed from the previous tweet due to the shortform nature of Twitter
- Say Tesco tweet "We have a new credit card", a reply could be "This is a really bad idea", the pipeline I came up would not pick up this Tweet despite it being relevant
-
- Have decided to go for a broader idea of analyzing the sentiment of all the replies to a particular Tweet and linking this to the most relevant concept/entities/keywords from the original Tweet
- Could then graph the sentiment over time for each concept/entity/keyword as a series as originally planned - maybe this graph could be correlated to finical news for example, if replies sent about Tesco credit card are negative and there is a negative article that mentions Tesco's credit card - may be linked

- Alternatively, could graph the average sentiment for each Tweet over time as one series, allowing you to see how each individual tweet has been received. This could then be linked to stock prices to see if there is a correlation
- Would like to work in number of favorites/retweets as part of the reception of a Tweet


18/06/17
- Having issues with getting replies
- Can't directly search for replies to a specific Tweet using the API
- Can pull Tweets more recent than other Tweet sent to a certain account - about as close as you can get
- My results when doing that only include a few replies
- Most of the tweets sent to the account are not replies to a specific Tweet

- New idea: Pull Tweets sent to the account that are not replies, do entity extraction and sentiment analysis on this Tweets
- Could graph the average sentiment of tweets over time sent to the account for example
- Build a coloured word cloud sort of thing from these replies of the most commonly talked about concepts and the sentiment about those concepts

- This may not work as people are probably more likely to be negative when tweeting to the account as they are likely looking to have an issue resolved
- in the same way that likely most of the tweets from a company accounts are going to have a positive sentiment
- Tweets might not necessarily be about new developments which might make event prediction hard