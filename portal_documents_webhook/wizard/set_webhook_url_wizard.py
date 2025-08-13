from odoo import _, fields, models
from odoo.exceptions import UserError


class SetWebhookUrlWizard(models.TransientModel):
    _name = "set.webhook.url.wizard"
    _description = "Set Webhook URL Wizard"

    webhook_url = fields.Char(string="Webhook URL")

    def action_set_webhook_url(self):
        active_ids = self.env.context.get("active_ids")
        if not active_ids:
            raise UserError(_("No documents selected."))
        self.env["documents.document"].browse(active_ids).write(
            {"webhook_url": self.webhook_url}
        )
        return {"type": "ir.actions.client", "tag": "soft_reload"}
