from odoo import api, fields, models


class HideField(models.Model):
    _name = 'hide.field'
    _description = 'HideField'

    access_rights_management_id = fields.Many2one('access.rights.management')

    model_id = fields.Many2one('ir.model', 'Model')
    model_name = fields.Char(string='Model Name', related='model_id.model', readonly=True, store=True)

    field_id = fields.Many2many('ir.model.fields', 'hide_field_ir_model_fields_rel', 'hide_field_id', 'ir_field_id',
                                'Field')

    invisible = fields.Boolean('Invisible')
    readonly = fields.Boolean('Read-Only')
    required = fields.Boolean('Required')
    external_link = fields.Boolean('Remove External Link')
