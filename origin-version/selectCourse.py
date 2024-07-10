import sys

def select_course(course_list):
    print(f"Available courses:".rstrip())
    for current_course in course_list:
        print(f"{current_course['name']}")

    choice = input("Enter the course you want to inquire:") 
    course_names = [course['name'] for course in course_list]
    if choice in course_names:
        return choice
    else:
        print("Invalid course, please enter again:")
        return select_course(course_list)

def get_course_id_by_name(course_list, choice):
    
    for course in course_list:
        if course['name'] == choice:
            return course['courseId']
     
def get_player_scores_by_course_id(classfied_player_data, chosen_courseId):
    
    try:
        player_scores = classfied_player_data[chosen_courseId]
        return player_scores
    except KeyError:
        print("此比赛还没有记录，程序即将关闭")
        sys.exit()
    except Exception:
        print("Fatal error, please contact the developer.")