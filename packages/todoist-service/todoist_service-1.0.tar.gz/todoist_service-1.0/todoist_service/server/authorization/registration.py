from todoist_service.todoist_wrapper.todoist_api_wrapper import TodoistAPIWrapper
from todoist_service.db import DB


def register_user(access_token: str):
    doist = TodoistAPIWrapper(access_token)
    user_id = str(doist.get_user_id())
    user_name = str(doist.get_user_name())

    db = DB.get_instance()
    db.add_user(user_id=user_id, token=access_token, full_name=user_name)
    return access_token, user_id
