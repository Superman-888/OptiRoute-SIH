import lightgbm as lgb


def load_model(model_path: str):
    return lgb.Booster(model_file=model_path)