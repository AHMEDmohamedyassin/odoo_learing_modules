/** @odoo-module **/

import { Component } from '@odoo/owl';
import { registry } from '@web/core/registry';

export class ListViewAction extends Component{
    static template = "my_module.ListView";
    
    setup() {
        super.setup();
    }
}

registry.category("actions").add("my_module.list_view_action" , ListViewAction);