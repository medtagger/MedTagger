def ask_user_question(prompt_message: str) -> bool:
    """Ask user a question and ask him/her for True/False answer (default answer is False)

    :param prompt_message: message that will be prompted to user
    :return: boolean information if user agrees or not
    """
    answer = input(prompt_message + ' [y/N] ')
    return answer.lower() in ['y', 'yes', 't', 'true']
