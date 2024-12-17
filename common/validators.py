def convert_str_hash_list_validator(cls, v):
    if isinstance(v, str):
        v = v.split('#')

    return ' '.join(v).split()
