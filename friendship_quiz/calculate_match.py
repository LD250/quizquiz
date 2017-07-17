class CalculateMatch(object):

    def _get_answers_set(self, answers):
        return set([(answer.question_id, answer.choice_id) for answer in answers])

    def calculate_match(self, your_answers, friend_answers):
        total = len(your_answers)
        match = self._get_answers_set(your_answers) & self._get_answers_set(friend_answers)
        return len(match) / total
