/** @odoo-module */

import {DocumentsControlPanel as BaseDocumentsControlPanel} from "@documents/views/search/documents_control_panel";
import {patch} from "@web/core/utils/patch";

patch(BaseDocumentsControlPanel.prototype, {
    async onSetWebhookUrl() {
        const docIds = this.targetRecords.map((r) => r.data.id);
        if (!docIds.length) return;
        const action = await this.orm.call(
            "documents.document",
            "action_set_webhook_url",
            [docIds]
        );
        await this.action.doAction(action);
    },
});
