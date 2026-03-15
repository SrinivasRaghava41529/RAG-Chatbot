def validate_answer(answer):

    if answer is None:
        return "⚠ No response generated."

    if len(answer.strip()) == 0:
        return "⚠ The model returned an empty answer."

    if len(answer) < 10:
        return "⚠ The generated answer is too short to be reliable."

    return answer