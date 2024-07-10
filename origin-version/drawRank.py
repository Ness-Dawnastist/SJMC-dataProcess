from PIL import Image, ImageDraw, ImageFont

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
