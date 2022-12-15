from odoo import api, fields, models
from lxml import etree
import ast


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def get_views(self, views, options=None):
        res = super().get_views(views, options)
        if 'views' in res.keys():
            actions_and_prints = []
            for access in self.env['remove.action'].search(
                    [('access_rights_management_id', 'in', self.env.user.access_rights_management_ids.ids),
                     ('model_id.model', '=', self._name)]):
                actions_and_prints += access.mapped('report_action_ids.action_id').ids
                actions_and_prints += access.mapped('server_action_ids.action_id').ids
            for view in ['list', 'form']:
                if view in res['views'].keys():
                    if 'toolbar' in res['views'][view].keys():
                        if 'print' in res['views'][view]['toolbar'].keys():
                            prints = res['views'][view]['toolbar']['print'][:]
                            for pri in prints:
                                if pri['id'] in actions_and_prints:
                                    res['views'][view]['toolbar']['print'].remove(pri)
                        if 'action' in res['views'][view]['toolbar'].keys():
                            action = res['views'][view]['toolbar']['action'][:]
                            for act in action:
                                if act['id'] in actions_and_prints:
                                    res['views'][view]['toolbar']['action'].remove(act)
        return res

    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        res = super().get_view(view_id, view_type, **options)
        access_management_obj = self.env['access.rights.management']
        doc = etree.XML(res['arch'])
        if view_type == 'form':
            # remove external link
            access_fields_recs = self.env['hide.field'].search([
                ('access_rights_management_id.user_ids', 'in', self.env.user.id),
                ('access_rights_management_id.active', '=', True),
                ('model_id.model', '=', res['model']), ('external_link', '=', True)])
            if access_fields_recs:
                for field in access_fields_recs.mapped('field_id'):
                    if field.ttype in ['many2many', 'many2one']:
                        for field_ele in doc.xpath("//field[@name='" + field.name + "']"):
                            options = 'options' in field_ele.attrib.keys() and field_ele.attrib['options'] or "{}"
                            options = ast.literal_eval(options)
                            options.update({'no_create': True, 'no_create_edit': True, 'no_open': True})
                            field_ele.attrib.update({'options': str(options)})
                res['arch'] = etree.tostring(doc, encoding='unicode')
            if access_management_obj.search(
                    [('active', '=', True), ('user_ids', 'in', self.env.user.id), ('hide_chatter', '=', True)],
                    limit=1).id:
                for div in doc.xpath("//div[@class='oe_chatter']"):
                    div.getparent().remove(div)
                res['arch'] = etree.tostring(doc, encoding='unicode')

        # the hole readonly
        readonly_access_id = access_management_obj.search(
            [('active', '=', True), ('user_ids', 'in', self.env.user.id),
             ('readonly', '=', True)])
        if readonly_access_id:
            doc.attrib.update({'create': 'false', 'delete': 'false', 'edit': 'false'})
            res['arch'] = etree.tostring(doc, encoding='unicode').replace('&amp;quot;', '&quot;')
        else:
            # TODO : Model access
            access_remove_action_model_ids = self.env['remove.action'].search([
                ('access_rights_management_id.user_ids', 'in', self.env.user.id),
                ('access_rights_management_id.active', '=', True),
                ('model_id.model', '=', res['model'])])
            if access_remove_action_model_ids:
                delete = 'true'
                edit = 'true'
                create = 'true'
                for remove_action_ids in access_remove_action_model_ids:
                    if remove_action_ids.restrict_create:
                        create = 'false'
                    if remove_action_ids.restrict_edit:
                        edit = 'false'
                    if remove_action_ids.restrict_delete:
                        delete = 'false'
                    if remove_action_ids.readonly:
                        create, delete, edit = 'false', 'false', 'false'
                doc.attrib.update({'create': create, 'delete': delete, 'edit': edit})
                res['arch'] = etree.tostring(doc, encoding='unicode')
        return res
