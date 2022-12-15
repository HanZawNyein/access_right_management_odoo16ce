from odoo import fields, models, api, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    access_rights_management_ids = fields.Many2many('access.rights.management', 'access_management_users_rel', 'user_id', 'access_rights_management_id', 'Access Pack')
