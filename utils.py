def validate_score(score):
    try:
        score = score.split(':')
        score_1 = int(score[0])
        score_2 = int(score[1])

        return score_1, score_2

    except:
        return False, False
