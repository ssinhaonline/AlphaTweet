# AlphaTweet
@author: ssinhaonline

Tweet popularity predictor

Here's the project running instructions, for reference:

Part I: For a fresh new user:
=============================

User should have a significant activity and a follower's list for the project to be working with enough data.
1. From the project's home directory, execute:
$> python myScraper.py
2. On prompt, type:
@: <username>
3. Shall take a while to parse data depending on the user's activity and number of users.
4. Will create a file and a directory:
i) <username>.info : File that has metadata to find this specific user later on.
ii) <username>/ : Contains the user's tweets and follower's retweet history for the last 28 days. User's file named as u_<username>.csv and followerk's files shall be saved as f_<followerk>.csv
5. Once myScraper stops running, the classification can be done using:
$> python myDriver.py <username>
6. On prompt, enter the input tweet:
Enter the tweet for analysis: <input_tweet>
7. Shall produce desired output as:
i) Possible number of retweets: <n>
ii) Correlation: (<Pearson coefficient>, <p-value>)

Part 2: For reproducing the results in the proect report:
=========================================================

1. No need to use myScraper.py as data is already collected for 4 users with usernames:
i) mulaney
ii) azizansari
iii) amyschumer
iv) therealrusselp
They all have their data stored in <username>/ subdirectory and metadata in <username>.info file.
2. For each user, do steps 5 to 7 in Part I.
