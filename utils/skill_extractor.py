def extract_skills(text, skill_list):
    text = text.lower()
    found_list = []

    for skill in skill_list:
        if skill.lower() in text:
            found_list.append(skill)

    return list(set(found_list))

