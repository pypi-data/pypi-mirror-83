# -*- coding: utf-8 -*-

import ckan.plugins.toolkit as tk


def get_auth_functions():
    return {
        "fpx_order_ticket": fpx_order_ticket,
    }


@tk.auth_allow_anonymous_access
def fpx_order_ticket(context, data_dict):
    return {"success": True}
