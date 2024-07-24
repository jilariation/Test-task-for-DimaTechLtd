from sanic import Sanic
from app.controllers.admin_controller import bp as bp_admin
from app.controllers.auth_controller import bp as bp_auth
from app.controllers.payment_controller import bp as bp_payment
from app.controllers.user_controller import bp as bp_user

app = Sanic("my_async_app")
app.blueprint(bp_admin)
app.blueprint(bp_auth)
app.blueprint(bp_user)
app.blueprint(bp_payment)
