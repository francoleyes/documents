import requests

from odoo import fields, models


class DocumentsWebhookQueue(models.Model):
    _name = "documents.webhook.queue"
    _description = "Documents Webhook Queue"

    document_id = fields.Many2one("documents.document", required=True)
    user_id = fields.Many2one(
        "res.users", string="User", help="User who triggered the webhook event"
    )
    action = fields.Selection(
        [("create", "Create"), ("unlink", "Unlink")], required=True
    )
    webhook_url = fields.Char(required=True)
    state = fields.Selection(
        [("pending", "Pending"), ("done", "Done"), ("error", "Error")],
        default="pending",
        index=True,
    )
    last_error = fields.Text()
    try_count = fields.Integer(default=0)
    last_try_date = fields.Datetime()

    def process_queue(self, batch_size=20):
        access_token = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "portal_documents_webhook.documents_webhook_access_token", default=None
            )
        )
        to_process = self.search([("state", "=", "pending")], limit=batch_size)
        for rec in to_process:
            headers = {}
            if access_token:
                headers["access_token"] = f"{access_token}"
            try:
                resp = requests.post(
                    rec.webhook_url,
                    json={"id": rec.document_id.id, "action": rec.action},
                    headers=headers,
                    timeout=15,
                )
                if resp.status_code == 200:
                    rec.state = "done"
                else:
                    rec.state = "error"
                    rec.last_error = f"HTTP {resp.status_code}: {resp.text}"
            except Exception as e:
                rec.state = "error"
                rec.last_error = str(e)
            rec.try_count += 1
            rec.last_try_date = fields.Datetime.now()

    def clean_document_webhook_queue_done(self):
        self.search([("state", "=", "done")]).unlink()

    def action_set_pending(self):
        self.write({"state": "pending"})
