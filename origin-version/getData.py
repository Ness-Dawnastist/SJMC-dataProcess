def get_data(url):
    import requests

    # 获取数据
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 保存到本地
        with open('rankData.json', 'w', encoding='utf-8') as file:
            file.write(response.text)
        print("已成功更新到 'rankData.json'")
    else:
        print(f"请求失败，状态码: {response.status_code}")
        input("输入任意字符后按回车，按最后一次更新的数据继续：")
