import sys
import numpy as np

# 用户特征：性别（0=女, 1=男）、年龄（18-60）、历史行为（物品ID）
user_features = np.array([
    [1, 25, 101],  # 用户1
    [0, 30, 102],  # 用户2
])

# 物品特征：类别（0=电影, 1=书籍）、热度（0-1）
item_features = np.array([
    [0, 0.8],  # 物品1
    [1, 0.5],  # 物品2
])

# 标签：用户是否喜欢该物品
labels = np.array([1, 0])  # 用户1喜欢物品1, 用户2不喜欢物品2
print(user_features)
print(item_features)
print(labels)


###################################################################


import numpy as np
import pandas as pd
print(np.__version__)  # 应输出1.19.5
print('++++++++++++++++++++++++++++++')
import tensorflow as tf
print(tf.__version__)  # 确保无报错

print('------------------------------')


import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Dense, Flatten, Concatenate
from tensorflow.keras.models import Model

# 参数设置
embedding_dim = 8  # 嵌入维度
print('22222222222222222222222222222222222222', embedding_dim)

# 用户塔
user_input = Input(shape=(3,), name="user_input")  # 用户特征：性别、年龄、历史行为
user_embedding = Dense(embedding_dim, activation="relu")(user_input)  # 用户特征转向量

# 物品塔
item_input = Input(shape=(2,), name="item_input")  # 物品特征：类别、热度
item_embedding = Dense(embedding_dim, activation="relu")(item_input)  # 物品特征转向量


print(user_embedding)
print(item_embedding)

# 匹配层：余弦相似度
similarity = tf.keras.layers.Dot(axes=-1, normalize=True, name="cosine_similarity")(
    [user_embedding, item_embedding]
)

# 构建模型
model = Model(inputs=[user_input, item_input], outputs=similarity)
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# 打印模型结构
model.summary()

sys.exit()

######################################################################
# 模型训练
model.fit(
    [user_features, item_features],  # 输入
    labels,                          # 标签
    epochs=10,
    batch_size=2
)


#####################################################################
# 测试用户特征
test_user = np.array([[1, 28, 101]])  # 性别=男, 年龄=28, 历史行为=物品101

# 测试物品特征
test_items = np.array([
    [0, 0.9],  # 物品1
    [1, 0.7],  # 物品2
])

# 计算相似度
scores = model.predict([test_user, test_items])
print("测试用户与物品的匹配分数：", scores)
