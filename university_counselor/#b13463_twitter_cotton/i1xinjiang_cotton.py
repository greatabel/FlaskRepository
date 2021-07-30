from csv_operation import csv_reader
from sentiment import anlaysis

from i2detection import detect

# import botometer



# rapidapi_key = ""
# twitter_app_auth = {
#     'consumer_key': '',
#     'consumer_secret': '',
#     'access_token': '',
#     'access_token_secret': '',
#   }
  
# blt_twitter = botometer.BotometerLite(rapidapi_key=rapidapi_key, **twitter_app_auth)

# # Prepare a list of screen_names you want to check.
# # The list should contain no more than 100 screen_names; please remove the @


# # Prepare a list of user_ids you want to check.
# # The list should contain no more than 100 user_ids.
# user_id_list = [ 77436536, 1548959833]
# blt_scores = blt_twitter.check_accounts_from_user_ids(user_id_list)

# print(blt_scores)
'''
第一部分就是识别机器人用户  在总用户的占比 发布的推文占比  
第二部分就是构建传播网络结构 分析下机器人账户的行为特征
第三部分就是做一下账户推文的文本特点和情感倾向

'''
class Percent(float):
    def __str__(self):
        return '{:.4%}'.format(self)



cotton = csv_reader("xinjiang324_327.csv", "data")
print(cotton[0], "#" * 10, cotton[1], "#" * 10, " \n", cotton[2])
name_dict = {}
for c in cotton[1:]:

	if len(c)> 7:
		if c[7] not in name_dict:
			name_dict[c[7] ] = 1
		else:
			name_dict[c[7] ] += 1

print(len(name_dict), name_dict)

def filterTheDict(dictObj, callback):
    newDict = dict()
    # Iterate over all the items in dictionary
    for (key, value) in dictObj.items():
        # Check if item satisfies the given condition then add to new dict
        if callback((key, value)):
            newDict[key] = value
    return newDict

# 找出值得分析的userid列表
# newDict = filterTheDict(name_dict, lambda elem: elem[1] > 1)
# print(newDict, len(newDict))


# Open a file: 打开所有用户主页被抓取数据
file = open('data/profiles.txt', mode='r') 
# read all lines at once
all_of_it = file.read()
# close the file
file.close()
records = all_of_it.split('##########')
print(len(records))

bot_list = []

for record in records:
	if '|' in record:
		items = record.split('|')
		# print(len(items),items, '*'*5)
		score = detect(items)
		if score <= 3.5:
			bot_list.append(items[2].strip().replace('@', '').lower())



print('#'*30,'\n')

print('bot数量:',len(bot_list),'\nbot列表:',bot_list)


x = Percent(len(bot_list)/ len(name_dict))

print("1. bot/总用户的占比:", x )

bot_cotton = 0

filter_tweets = []
for c in cotton[1:]:

	if len(c)> 7:
		if c[7]  in bot_list:
			# print(c[7])
			bot_cotton += 1
			filter_tweets.append(c)
			# 为网络分析 所使用
			# if c[10] is not None and len(c[10]) > 0 and '@' in c[10]:
			# 	t = c[10].split()
			# 	if '@' in t[0]:
			# 		# print('t[0]=', t[0][1:])
			# 		print("name="+c[7]+ ",name="+t[0][1:]+",'"+ c[3]+"'")

print('bot推文数:',bot_cotton)

print('#'*30,'\n 2. bot发布的推文占比:')
y = Percent(bot_cotton/ len(cotton))
print(y)

# print("-*-" * 10)
# data2019 = csv_reader("2020_04-06sankaku.csv", "data")
# print(data2019[0], "#" * 10, data2019[1], "#" * 10, " \n", data2019[2])


# print("-" * 10, "tweets:")
# print(data2020[1][10], "\n", "#" * 10, "\n", data2019[1][10])


js_txt = '''

var DATA = {
'''

print("\n1. Heat comparison")
# print(len(data2020), " VS ", len(data2019))

compare_txt = "'bot_cotton':" + str(bot_cotton) + ", 'total_cotton':" + str(len(cotton))
js_txt += compare_txt


# data2020full = csv_reader("2021-06senkaku.csv", "data")
# data2020full = data2020

print("\n2. sentiment anlaysis")
total_sentiment = 0

num_positive = 0
num_neural = 0
num_nagtive = 0

unwanted_chars = ".,-_ ()’'"
black_list = ["//t.co/daqs0qh2wb #", "# #", 
    "[ auto ]", "//t.co/tgzew5at0r https", "s territory"]
wordfreq = {}

usernamefreq = {}

split = 1
# pick_twlist = data2020full[0::split]
# pick_twlist = data2020full[0::split]
# for tw in pick_twlist:
for tw in filter_tweets:
    text = tw[10]
    username = tw[8]
    # print(text, "\n@@@username=", username, "\n")
    words, sentiment_tw = anlaysis(text)
    print(sentiment_tw)
    total_sentiment += sentiment_tw
    if sentiment_tw < 0:
        num_nagtive += 1
    if sentiment_tw == 0:
        num_neural += 1
    if sentiment_tw > 0:
        num_positive += 1
    # print('words=', words)
    for raw_word in words:
        word = raw_word.strip(unwanted_chars)
        if word not in wordfreq:
            if word not in black_list:
                wordfreq[word] = 0
        if word not in black_list:
            wordfreq[word] += 1
    if username == 'Indo-Pacific News - Watching the CCP-China Threat':
        username = 'Indo-Pacific News'
    username = username.replace("'", "")
    if username not in usernamefreq:
        usernamefreq[username] = 0
    usernamefreq[username] += 1

print('@'*30, usernamefreq)

print("tatal sentiment polarity:", total_sentiment)
print("average sentiment polarity:", total_sentiment / len(filter_tweets))
print(
    "number of (positive VS neural VS nagtive):",
    num_positive * split,
    num_neural * split,
    num_nagtive * split,
)
sentiment_txt = ",'total_sentiment_polarity':" + str( round(total_sentiment, 2)) \
    + ", 'average_sentiment_polarity':" + str(round( total_sentiment / len(filter_tweets),2))  \
    + ",'num_positive':" + str(num_positive * split) + ", 'num_neural':" + str(num_neural * split) \
     + ",'num_nagtive':" + str(num_nagtive * split) + ", 'filter_tweets':" + str(len(filter_tweets))
js_txt += sentiment_txt

js_txt += " };\n"


print("\n 3. related words related to this topic")

js_txt += 'var RELATED_WORDS = {'
# print(wordfreq)
index = 0
a1_sorted_keys = sorted(wordfreq, key=wordfreq.get, reverse=True)
for r in a1_sorted_keys:
    if wordfreq[r] > 1:
        print(r, wordfreq[r])
        if index < 10:
            js_txt += "'" + r + "':" + str(wordfreq[r]) + ','
            index += 1


js_txt += " };\n"


index = 0
print("\n 4. username often posts related topics")
js_txt += 'var WHO_TWEETS = {'
a2_sorted_keys = sorted(usernamefreq, key=usernamefreq.get, reverse=True)
# print('#'*20, usernamefreq)

for r in a2_sorted_keys:
    if usernamefreq[r] >= 1 and r not in ('name'):
        print(r, usernamefreq[r])
        if index < 10:
            js_txt += "'" + r + "':" + str(usernamefreq[r]) + ','
            index += 1


js_txt += " };"

# write to a local js file , let d3 do data-visual
with open("data_visualization/xinjiang.js", 'w') as file:
    file.write(js_txt.strip())


