{
    "author": "Franco Leyes",
    "license": "AGPL-3",
    "name": "Portal Documents Webhook",
    "version": "18.0.1.0.0",
    "summary": "Webhook for portal shared documents",
    "website": "https://github.com/francoleyes/documents",
    "depends": ["portal_documents_access"],
    "data": [
        "data/ir_cron.xml",
        "data/ir_actions_server.xml",
        "data/param_access_token.xml",
        "security/ir.model.access.csv",
        "views/documents_webhook_queue_views.xml",
        "views/documents_document_views.xml",
        "wizard/set_webhook_url_wizard_view.xml",
    ],
    "installable": True,
    "assets": {
        "web.assets_backend": ["portal_documents_webhook/static/src/views/**/*"],
    },
}
