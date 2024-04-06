import re


def dictify_questions(text: str):
    questions = re.findall(r"Вопрос \d+:\s(.*?)\sОтвет", text, re.DOTALL)
    answers = re.findall(r"Ответ:\s(.*?)\.\s\s", text)

    questionnaire = list(zip(questions, answers))
    return questionnaire
