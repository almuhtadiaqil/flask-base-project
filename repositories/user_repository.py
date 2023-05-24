from schemas.pagination_schema import PaginationSchema
from schemas.user_schema import UserSchema
from schemas.error_schema import ErrorSchema
from models.user_model import User
from sqlalchemy.sql import text
from app import db


class UserRepository:
    @staticmethod
    def get_all_users(request: PaginationSchema):
        try:
            query = User.query
            search = request["search"]
            order_by = request["order_by"]
            page_index = int(request["page_index"])
            page_size = int(request["page_size"])
            if search is not None:
                search = "%{}%".format(search.lower())
                query.filter(User.full_name.ilike(search) | User.nik.ilike(search))
            if order_by is not None:
                order_by = order_by.split(",")
                query.order_by(text("{} {}".format(order_by[0], order_by[1])))
            count = len(query.all())
            result = query.paginate(page=page_index, per_page=page_size)
            return result, count
        except Exception as e:
            error = ErrorSchema()
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)

    @staticmethod
    def create_user(user_schema: UserSchema):
        try:
            user = User(
                full_name=user_schema["full_name"],
                nik=user_schema["nik"],
                password=user_schema["password"],
                last_login_at=None,
                created_at=None,
                updated_at=None,
                deleted_at=None,
                privkey=None,
                pubkey=None,
            )

            user.setPassword(password=user_schema["password"])
            db.session.add(user)
            db.session.commit()

            return user
        except Exception as e:
            error = ErrorSchema()
            error = ErrorSchema().load({"message": str(e), "code": 500})
            raise Exception(error)
