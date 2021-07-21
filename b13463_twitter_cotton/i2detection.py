def detect(items):
	score = 5
	following = None
	followers = None
	for item in items:
		if 'Avatar:' in item:
			print(item)
			if 'default_profile_normal.png' in item:
				# 无自定义头像，降低真人权重
				score -= 1
		if 'Bio:' in item:
			# 无简介，降低真人权重
			item = item.replace('Bio:', '').strip()
			if len(item) < 5:
				score -= 1
		if 'Following:' in item:
			following = item.replace('Following:', '').strip()
			print('following=', following) 
			
		if 'Followers:' in item:
			followers = item.replace('Followers:', '').strip()
			print('Followers=', followers) 
			if int(followers) <= 3:
				score -= 0.5

		if 'Tweets:' in item:
			tweets = item.replace('Tweets:', '').strip()
			if int(tweets) <= 10:
				score -= 0.5
		if 'Likes:' in item:
			likes = item.replace('Likes:', '').strip()
			if int(likes) <= 10:
				score -= 0.5
				
	if int(following) != 0:
		rate = int(followers)/int(following) 
		if rate < 0.1:
			score -= 1

	return score