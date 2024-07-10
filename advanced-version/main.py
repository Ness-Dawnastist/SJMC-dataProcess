import json
import requests
from PIL import Image, ImageDraw, ImageFont


def get_player_name(uuid):
    url = f'https://skin.mualliance.ltd/api/union/profile/mapped/byuuid/{uuid}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('name', uuid)  # 返回玩家名称，如果没有则返回 UUID
    else:
        print(f"Failed to retrieve data for UUID {uuid}")
        return uuid


def get_data():
    url = 'https://mc.sjtu.cn/smp2_parkour.php?pass=ynkdress'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"请求失败，状态码: {response.status_code}")
        input("输入任意字符后按回车，按最后一次更新的数据继续：")
        return None


def group_by_course_id(player_data):
    course_scores = {}

    # 遍历 time 列表，将每个字典按 courseId 分类
    for item in player_data:
        course_id = item['courseId']
        if course_id not in course_scores:
            course_scores[course_id] = []
        course_scores[course_id].append(item)

    # 对每个 courseId 列表中的字典按 time 进行排序
    for _, times in course_scores.items():
        # 将 time 从字符串转换为整数进行排序
        times.sort(key=lambda x: int(x['time']))

    return course_scores


# 创建排行榜图片
def create_ranking_image(rankings, filename='rankings.jpg'):
    width, height = 800, 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    try:
        # 使用本地字体文件
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        # 如果没有 arial.ttf 字体文件，使用默认字体
        font = ImageFont.load_default()

    # 绘制标题
    title = "Ranking List"
    # 使用 textbbox 计算文本大小
    bbox = draw.textbbox((0, 0), title, font=font)
    title_width = bbox[2] - bbox[0]
    title_height = bbox[3] - bbox[1]
    draw.text(((width - title_width) / 2, 20), title, font=font, fill='black')

    # 绘制表头
    draw.text((50, 60), 'Rank', font=font, fill='black')
    draw.text((150, 60), 'Player Name', font=font, fill='black')
    draw.text((400, 60), 'Time', font=font, fill='black')

    # 绘制玩家成绩
    y = 100  # 起始 Y 坐标
    for index, ranking in enumerate(rankings):
        rank_text = f"{index + 1}"
        name_text = ranking['playerId']
        time_text = f"{ranking['time']}"
        draw.text((50, y), rank_text, font=font, fill='black')
        draw.text((150, y), name_text, font=font, fill='black')
        draw.text((400, y), time_text, font=font, fill='black')
        y += 30  # 下一行的 Y 坐标

    # 保存图像
    image.save(filename)


def select_course(course_list):
    while True:
        print(f"Available courses:")
        for course in course_list:
            print(f"{course['name']}")

        choice = input("Enter the course you want to inquire:")
        for course in course_list:
            if course['name'] == choice:
                return course['courseId']
        else:
            print("Invalid course, please enter again:")
            continue


if __name__ == '__main__':
    # 下载数据
    data = get_data()

    if data:
        # 保存到 rankData.json
        with open('rankData.json', 'w', encoding='utf-8') as file:
            file.write(data)
            print("已成功更新到 'rankData.json'")
            data = json.loads(data)
    else:
        # 加载数据
        with open('rankData.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

    # 获取玩家数据的字典列表
    player_data = data['data']['time']

    # 按 courseId 分类并按时间大小排序
    # course_scores 是一个字典，键为courseId(str)，值为一个字典列表
    course_scores = group_by_course_id(player_data)

    # 让用户选择比赛
    course_list = data['data']['course']
    chosen_course_id = select_course(course_list)

    # 根据选择获取成绩数据
    if chosen_course_id in course_scores:
        player_scores = course_scores[chosen_course_id]
    else:
        print("此比赛还没有记录，程序即将关闭")
        exit()

    # 创建玩家名称与对应时间的字典列表
    # 获取玩家 UUID、名称和时间
    rankings = [{
        "playerId": get_player_name(item["playerId"]),
        "time": item["time"]
    } for item in player_scores]

    # 打印最终的排行榜
    for item in rankings:
        print(f"Player ID: {item['playerId']}, Time: {item['time']}")

    # 绘制排行榜
    create_ranking_image(rankings)