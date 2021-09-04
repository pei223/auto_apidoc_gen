def singleton_class(class_):
    instance = [
        None,
    ]

    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = class_(*args, **kwargs)
        return instance[0]

    return wrapper
