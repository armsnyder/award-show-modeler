import twitter

twitter_key = 'DYcq5c6vadVEe4l8Xnd5Dhu29'
twitter_secret = 'PB0mYw89QYCu9YC63s3bbAxfJr2h07DmJ9zwNlKX4sT1yVbBDR'
twitter_access_token = '80998836-wYMg9lHff0WgBys71LV1SVFwyaaL0XVU17M7Gfx2x'
twitter_access_secret = 'd8MV8XAPJoNs40Z4164uUgMjUwmaqOYRygKm82U9zgD0o'
twitter_api = twitter.Twitter(
    auth=twitter.oauth.OAuth(twitter_access_token, twitter_access_secret, twitter_key, twitter_secret))