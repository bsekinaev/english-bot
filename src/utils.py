from datetime import datetime, timedelta

def get_next_review(level):
    intervals = [1,3,7,14,30] # Дни через которые повторить
    return datetime.now() + timedelta(days=intervals[level])
