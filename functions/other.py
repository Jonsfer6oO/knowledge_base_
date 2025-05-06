def convert_dict_in_str(data: dict):
    attrs = ', '.join(f"{k}={v}" for k, v in data.items())
    return attrs
