import getData
import loadData
import classifyByCourseId
import selectCourse
import requests
import drawRank

# 下载数据到rankData.json
url = 'Hided'
getData.get_data(url) 

# 加载数据
data = loadData.load_data('rankData.json')

# 获取玩家数据的字典列表
player_data = data['data']['time']

# 按 courseId 分类并按时间大小排序
# classfied_player_data 是一个字典，键为courseId(str)，值为一个字典列表
classfied_player_data = classifyByCourseId.classifyByCourseId(player_data)

# 让用户选择比赛
course_list = data['data']['course']
choice = selectCourse.select_course(course_list)

# 根据选择获取成绩数据
chosen_courseId = selectCourse.get_course_id_by_name(course_list, choice)
player_scores = selectCourse.get_player_scores_by_course_id(classfied_player_data, chosen_courseId)

# 创建玩家名称与对应时间的字典列表
# 获取玩家 UUID 和时间
uuid_time_list = [{"playerId": item["playerId"], "time": item["time"]} for item in player_scores]

# 通过 API 将 UUID 转换为玩家名称
"""
这个函数不能封装，否则最后Player ID会变为None
我也不知道为什么，可能也只是我饿晕犯病了，或者偶发的网络问题
"""
def get_player_name(uuid):
    url = f'https://skin.mualliance.ltd/api/union/profile/mapped/byuuid/{uuid}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('name', uuid)  # 返回玩家名称，如果没有则返回 UUID
    else:
        print(f"Failed to retrieve data for UUID {uuid}")
        return uuid

for item in uuid_time_list:
    item["playerId"] = get_player_name(item["playerId"])

# 打印最终的排行榜
for item in uuid_time_list:
    print(f"Player ID: {item['playerId']}, Time: {item['time']}")

# 绘制排行榜
drawRank.create_ranking_image(uuid_time_list)
