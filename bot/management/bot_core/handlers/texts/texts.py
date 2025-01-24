from urllib.parse import urlparse, parse_qs


def get_hello_text(username: str) -> str:
    return f"Главное меню."


def extract_page_number(url):
    print('extract_page_number: ')
    print(url)
    if url is None or url == 'None':
        print('parser_url is None')
        return None
    parsed_url = urlparse(url)
    print("PARSER URL:", parsed_url)
    query_params = parse_qs(parsed_url.query)
    print('QUERY PARAMS',query_params)
    page_number = query_params.get('page', [1])[0]
    return page_number