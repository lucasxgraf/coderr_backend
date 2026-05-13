def get_auth_response(user, token):
    return {
        'token': token.key,
        'username': user.username,
        'email': user.email,
        'user_id': user.id,
    }