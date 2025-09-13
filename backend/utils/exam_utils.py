def calculate_score(answers, correct_answers):
    if len(answers) != len(correct_answers):
        return 0
    
    correct_count = sum(1 for i, answer in enumerate(answers) if answer == correct_answers[i])
    return (correct_count / len(correct_answers)) * 100