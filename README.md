# AlphaTweet
Tweet popularity predictor

Here's the plan, for reference:

1. Input user ID and tweet
2. Collect the user's tweet using a parser, and collect user's followers into a list.
3. Spawn threads for collecting the follower's tweets.
4. For the user and the followers, filter the tweet containing tweets from the last 4 weeks. Divide this into 3 + 1 last week's tweets.
5. For the user, use 3 week's tweets for training, and last week's tweets as testing. For the follower's, only the 3 week's data is relevant, last week's tweet doesn't really fit into the plan for now.
6. Generate the model using Naive Bayesian Classifier. Refer to the report for more info.
