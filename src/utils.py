def map_from_dict_like(model, dict_like: dict):
    attributes = [attr for attr in vars(model) if not attr.startswith("_")]
    model_attributes = {key: dict_like[key] for key in attributes}
    return model(**model_attributes)
