from flask import Blueprint

admin_bp = Blueprint('admin', __name__, template_folder='admin/templates')

from admin.admin_api import *
