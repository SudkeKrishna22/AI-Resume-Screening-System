import json

def get_skill_recommendations(missing_skills):

    with open(
        "Data/skills_recommendation.json",
        "r",
        encoding="utf-8"
    ) as f:

        recommendations = json.load(f)

    result = {}

    for skill in missing_skills:

        skill = skill.lower()

        if skill in recommendations:
            result[skill] = recommendations[skill]

    return result