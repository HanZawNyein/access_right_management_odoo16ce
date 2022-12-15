from odoo import api, fields, models, _


class AccessRightsManagement(models.Model):
    _name = 'access.rights.management'
    _description = 'Access Rights Management'

    name = fields.Char(required=True)
    readonly = fields.Boolean('Read-Only')
    active = fields.Boolean('Active', default=True)
    user_ids = fields.Many2many('res.users', 'access_management_users_rel', 'access_rights_management_id', 'user_id',
                                'Users')
    hide_menu_ids = fields.Many2many('ir.ui.menu', 'access_management_menu_rel', 'access_rights_management_id',
                                     'menu_id', 'Hide Menu')
    hide_field_ids = fields.One2many('hide.field', 'access_rights_management_id', 'Hide Field')
    remove_action_ids = fields.One2many('remove.action', 'access_rights_management_id', 'Remove Action')
    hide_view_nodes_ids = fields.One2many('hide.view.nodes', 'access_rights_management_id', 'Button/Tab Access')
    hide_chatter = fields.Boolean('Hide Chatter')
    disable_debug_mode = fields.Boolean('Disable Developer Mode')

    def write(self, vals):
        res = super(AccessRightsManagement, self).write(vals)
        self.clear_caches()
        return res

    def unlink(self):
        res = super(AccessRightsManagement, self).unlink()
        self.clear_caches()
        return res
