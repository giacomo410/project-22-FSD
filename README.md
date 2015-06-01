# project-22-FSD
README
=================================
REQUIREMENTS:

-Ubuntu 14.04 recommended. Not tested on other OS.
-Java (tested with version 1.7.0_79)
-Python 2.7.x
-Tweepy 3.3.0 (>>pip install tweepy)
-TweeboParser (can be found at: http://sourceforge.net/projects/tweeboparser/)
-Python pakages:-> numpy
		-> python-Levenshtein
		-> urllib3.contrib.pyopenssl (follow the guide at: https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning)

DOWNLOAD AND INSTALLATION:

-Download TweeboParser and install it following the readme contained in its folder

-After TweeboParser has been installed download the folder src and move all the files present in this folder to the folder TweeeboParser created at the previous point

-Open the file gatherer_tagger.py and in the first 5 lines you have to insert the consumer_key, consumer_secret, access_token, access_token_secret for authentication which can be found in the Twitter account (many guides are available online) and the number of tweets to compare each iteration (increasing this number will increase both the processing time and accuracy)

-Download the file final.sh and place it in the TweeboParser folder

-To run the algorithm from the terminal navigate to the TweeboParser folder and execute final.sh  (>> ./final.sh) which will open two new terminals (one for gathering and tagging tweets, one for processing them)

-The results will be printed on the file result.txt
