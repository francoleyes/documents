{
    "name": "Portal Documents Access",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "summary": "Enable portal users to access documents module",
    "website": "https://github.com/francoleyes/documents",
    "author": "Franco Leyes",
    "depends": [
        "documents",
        "portal",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
    ],
    "installable": True,
}
