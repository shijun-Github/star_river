import pynetease

# 创建pynetease客户端
client = pynetease.pynetease()

# 获取热门歌单，这里以获取华语流行榜为例
hot_playlists = client.top_playlists('华语流行榜')

# 打印每个热门歌单的名称和ID
for playlist in hot_playlists['playlists']:
    print(f"歌单名称: {playlist['name']}, 歌单ID: {playlist['id']}")