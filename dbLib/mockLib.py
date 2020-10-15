def create_user(userId, baseline, time):
    pass

def get_user_attr(userId, attrs):
    if int(userId) % 2 == 0:
        return None
    return {
            'user_id': '1',
            'coins': 0,
            'brushes': [],
            'paints': [],
            'baseline': {
                'flow': 10,
                'volume': 20
            },
            'history': [],
            'backgrounds': [],
            'drawings': [],
            'lastBreath': 0
        }