def format_user_response(user_dict):
    return {
        "id": str(user_dict["_id"]),
        "name": user_dict["name"],
        "email": user_dict["email"],
        "classification": user_dict["classification"],
        "exam_score": user_dict.get("exam_score"),
        "completed_courses": user_dict.get("completed_courses", []),
        "current_course": user_dict.get("current_course")
    }