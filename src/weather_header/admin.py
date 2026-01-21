from fastapi import FastAPI
from sqladmin import Admin, ModelView

from weather_header.db.session import engine
from weather_header.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.is_free_tier,
        User.is_frame_custom,
        User.frame_name,
        User.is_texture_custom,
        User.texture_name,
    ]


def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
