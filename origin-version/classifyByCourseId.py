def classifyByCourseId(player_data):

    classifyByCourseId = {}

    # 遍历 time 列表，将每个字典按 courseId 分类
    for item in player_data:
        current_course_id = item['courseId']
        if current_course_id not in classifyByCourseId:
            classifyByCourseId[current_course_id] = []
        classifyByCourseId[current_course_id].append(item)

    # 对每个 courseId 列表中的字典按 time 进行排序
    for current_course_id, times in classifyByCourseId.items():
        # 将 time 从字符串转换为整数进行排序
        times.sort(key=lambda x: int(x['time']))

    return classifyByCourseId


