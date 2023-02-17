from hashlib import sha256
from aiohttp_apispec import request_schema, response_schema, querystring_schema
from aiohttp.web_exceptions import HTTPNotFound, HTTPUnauthorized, HTTPForbidden
from app.admin.models import Admin
from app.admin.schemes import AdminSchema
from app.web.app import View
from app.store.admin.accessor import AdminAccessor
from app.web.utils import check_basic_auth, json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):

        data = await self.request.json()
        email = data['email']
        password = data['password']
        hashed_password = sha256(password.encode()).hexdigest()
        admin = await self.request.app.store.admins.get_by_email(email=email)
        if email == admin.email and hashed_password == admin.password:
            raw_admin = AdminSchema().dump(admin)
            return json_response(data={"admin":raw_admin})
        else:
            raw_admin = AdminSchema().dump(admin)
            return json_response(data={"invalid":raw_admin, "initial":str(hashed_password)})
            


class AdminCurrentView(View):
    @querystring_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def get(self):
        admin_email = self.request.app.database.admins[0].email
        admin = await self.request.app.store.admins.get_by_email(admin_email)
        if admin:
            return json_response(data={'admin': AdminSchema().dump(admin)})
        else:
            raise HTTPNotFound


class IndexView(View):
    async def get(self):
        return json_response(data='Bye, hello')
