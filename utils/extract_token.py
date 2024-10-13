def extract_token(cookies, token_name) -> str:
    for cookie in cookies.split(';'):
        if token_name in cookies:
            return cookie.split('=')[1]
