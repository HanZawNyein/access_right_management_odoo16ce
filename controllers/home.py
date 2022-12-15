from odoo.addons.web.controllers.action import Action
from odoo.addons.web.controllers.home import Home
from odoo.addons.web.controllers.utils import ensure_db
from odoo.http import request
from odoo import http


class Home(Home):

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        ensure_db()
        user = request.env.user.browse(request.session.uid)
        if len(user.company_ids) > 1:
            request.env['ir.ui.menu'].clear_caches()
        if not kw.get('debug') or kw.get('debug') != "0":
            access_management = request.env['access.rights.management'].sudo().search(
                [('active', '=', True), ('disable_debug_mode', '=', True), ('user_ids', 'in', user.id)], limit=1)
            if access_management.id:
                return request.redirect('/web?debug=0')
                # request.session.debug = '0'

        return super(Home, self).web_client(s_action=s_action, **kw)
