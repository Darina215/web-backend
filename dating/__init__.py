from flask import Blueprint

dating = Blueprint(
    'dating',
    __name__,
    template_folder='templates',
    url_prefix='/dating'
)

from . import routes
