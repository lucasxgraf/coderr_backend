def get_auth_response(user, token):
    """Return a standardized auth response dict used by both registration and login."""
    return {
        'token': token.key,
        'username': user.username,
        'email': user.email,
        'user_id': user.id,
    }
