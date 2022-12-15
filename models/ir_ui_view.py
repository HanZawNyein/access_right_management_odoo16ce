from odoo import models, SUPERUSER_ID, _


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    def _postprocess_tag_field(self, node, name_manager, node_info):
        # TODO : Hide Field
        res = super(IrUiView, self)._postprocess_tag_field(node, name_manager, node_info)
        hide_field_obj = self.env['hide.field'].sudo()
        if node.tag == 'field' or node.tag == 'label':
            for hide_field in hide_field_obj.search(
                    [('model_id.model', '=', name_manager.model._name),
                     ('access_rights_management_id.active', '=', True),
                     ('access_rights_management_id.user_ids', 'in', self._uid)
                     ]):
                for field_id in hide_field.field_id:
                    if (node.tag == 'field' and node.get('name') == field_id.name) or (
                            node.tag == 'label' and 'for' in node.attrib.keys() and node.attrib[
                        'for'] == field_id.name):

                        if hide_field.invisible:
                            node_info['modifiers']['invisible'] = True
                            node.set('invisible', '1')
                        if hide_field.readonly:
                            node_info['modifiers']['readonly'] = True
                            node.set('readonly', '1')
                            node.set('force_save', '1')
                        if hide_field.required:
                            node_info['modifiers']['required'] = True
                            node.set('required', '1')
        return res

    def _postprocess_tag_button(self, node, name_manager, node_info):
        # Hide Any Button
        postprocessor = getattr(super(IrUiView, self), '_postprocess_tag_button', False)
        if postprocessor:
            super(IrUiView, self)._postprocess_tag_button(node, name_manager, node_info)

        hide = None
        hide_button_obj = self.env['hide.view.nodes']
        hide_button_ids = hide_button_obj.sudo().search([
            ('model_id.model', '=', name_manager.model._name), ('access_rights_management_id.active', '=', True),
            ('access_rights_management_id.user_ids', 'in', self._uid)])

        # Filtered with same env user and current model
        btn_store_model_nodes_ids = hide_button_ids.mapped('btn_store_model_nodes_ids')
        if btn_store_model_nodes_ids:
            for btn in btn_store_model_nodes_ids:
                if btn.attribute_name == node.get('name'):
                    if node.get('string'):
                        if _(btn.attribute_string) == node.get('string'):
                            hide = [btn]
                            break
                    else:
                        hide = [btn]
                        break
        if hide:
            node.set('invisible', '1')
            if 'attrs' in node.attrib.keys() and node.attrib['attrs']:
                del node.attrib['attrs']
            node_info['modifiers']['invisible'] = True

        return None

    def _postprocess_tag_page(self, node, name_manager, node_info):
        postprocessor = getattr(super(IrUiView, self), '_postprocess_tag_page', False)
        if postprocessor:
            super(IrUiView, self)._postprocess_tag_page(node, name_manager, node_info)

        hide = None
        hide_tab_obj = self.env['hide.view.nodes']
        hide_tab_ids = hide_tab_obj.sudo().search([('model_id.model', '=', name_manager.model._name),
                                                   ('access_rights_management_id.active', '=', True),
                                                   ('access_rights_management_id.user_ids', 'in', self._uid)])

        page_store_model_nodes_ids = hide_tab_ids.mapped('page_store_model_nodes_ids')
        if page_store_model_nodes_ids:
            for tab in page_store_model_nodes_ids:
                if _(tab.attribute_string) == node.get('string'):
                    if node.get('name'):
                        if tab.attribute_name == node.get('name'):
                            hide = [tab]
                            break
                    else:
                        hide = [tab]
                        break
        if hide:
            node.set('invisible', '1')
            if 'attrs' in node.attrib.keys() and node.attrib['attrs']:
                del node.attrib['attrs']

            node_info['modifiers']['invisible'] = True

        return None
