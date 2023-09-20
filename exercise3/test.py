import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt

# 读取文本文件
with open('Moby Dick.txt', 'r', encoding='utf-8') as file:
    text = file.read()
    
# 标记化
tokens = word_tokenize(text)

# 停止词过滤
stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

# 词性标记
pos_tags = nltk.pos_tag(filtered_tokens)
    
# 统计词性频率
pos_freq_dist = FreqDist(tag for (word, tag) in pos_tags)
top_five_pos = pos_freq_dist.most_common(5)

# 引理化
lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens[:20]]

# 绘制频率分布图
pos_freq_dist.plot()

# 显示结果
print("Top 5 POS and their frequencies:")
for pos, freq in top_five_pos:
    print(pos, freq)

print("\nLemmatized tokens:")
print(lemmatized_tokens)