def get_weather(**kwargs):
    city = kwargs.get('city', '').lower()
    if city == 'vizag':
        return '38 c'
    return '40 c'


def add_numbers(**kwargs):
    return sum(kwargs.values())


AVAILABLE_TOOLS = {
    'get_weather': get_weather,
    'add_numbers': add_numbers,
}


def run_tool(function_name: str, function_input: dict):
    tool = AVAILABLE_TOOLS[function_name]
    return str(tool(**function_input))
