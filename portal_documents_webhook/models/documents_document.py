from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DocumentsDocument(models.Model):
    _inherit = "documents.document"

    webhook_url = fields.Char(
        string="Webhook URL",
        help=(
            "URL to notify when a document is created or deleted in this folder. "
            "Only allowed on folders."
        ),
    )

    @api.constrains("webhook_url", "type", "folder_id")
    def _check_webhook_url_on_folder(self):
        for rec in self.filtered("webhook_url"):
            if rec.type != "folder":
                raise ValidationError(_("Webhook URL can only be set on folders."))
            if rec.folder_id:
                raise ValidationError(
                    _("A folder with a Webhook URL cannot have a parent folder.")
                )

    def _get_ancestor_webhook_url(self):
        folder = self.folder_id
        while folder:
            if folder.webhook_url:
                return folder.webhook_url
            folder = folder.folder_id
        return False

    def _prepare_webhook_queue_vals(self, action):
        webhook_url = self._get_ancestor_webhook_url()
        if webhook_url:
            return {
                "document_id": self.id,
                "action": action,
                "webhook_url": webhook_url,
                "user_id": self.env.user.id,
            }
        return None

    def _call_cron(self):
        cron = self.env.ref(
            "portal_documents_webhook.ir_cron_documents_webhook_queue",
        )
        if cron:
            cron._trigger()

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        queue_vals = [rec._prepare_webhook_queue_vals("create") for rec in records]
        queue_vals = [vals for vals in queue_vals if vals]
        if queue_vals:
            self.env["documents.webhook.queue"].sudo().create(queue_vals)
        self._call_cron()
        return records

    def unlink(self):
        if self.env.context.get("bypass_webhook_queue"):
            return super().unlink()

        docs_to_queue = self.filtered(
            lambda d: d.type != "folder" and d._get_ancestor_webhook_url()
        )
        queue_vals = [
            rec._prepare_webhook_queue_vals("unlink") for rec in docs_to_queue
        ]
        if queue_vals:
            self.env["documents.webhook.queue"].sudo().create(queue_vals)
        docs_to_queue._write({"active": False})
        res = super(DocumentsDocument, self - docs_to_queue).unlink()
        self._call_cron()
        return res

    def action_set_webhook_url(self):
        view = self.env.ref("portal_documents_webhook.view_set_webhook_url_wizard_form")
        return {
            "type": "ir.actions.act_window",
            "res_model": "set.webhook.url.wizard",
            "view_mode": "form",
            "view_id": view.id,
            "views": [(view.id, "form")],
            "target": "new",
            "context": {"active_ids": self.ids},
        }
