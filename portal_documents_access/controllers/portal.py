from odoo.http import request

from odoo.addons.documents.controllers.portal import DocumentCustomerPortal


class PortalDocumentsAccess(DocumentCustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "document_count" in counters and request.env.user.has_group(
            "base.group_portal"
        ):
            Document = request.env["documents.document"]
            # Count documents: own (created or related partner) OR shared with me
            # (not owner but have permission)
            domain = [
                "|",
                "|",
                ("create_uid", "=", request.env.user.id),
                ("partner_id", "=", request.env.user.partner_id.id),
                "&",
                ("owner_id", "!=", request.env.user.id),
                ("user_permission", "!=", "none"),
            ]
            values["document_count"] = Document.search_count(domain)
        return values
