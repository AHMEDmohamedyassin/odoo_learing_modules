/** @odoo-module **/

import { Component, useState, onWillUnmount } from '@odoo/owl';
import { registry } from '@web/core/registry';
import { useService } from '@web/core/utils/hooks'

export class ListViewAction extends Component{
    static template = "my_module.ListView";
    
    setup() {
        super.setup();
        this.state = useState({
            'records': [],
            'name': ''  ,
            'id' : null
        });
        this.orm = useService('orm');
        this.rpc = useService('rpc');
        this.loadRecords();
        this.update_intervals = setInterval(() => {
            console.log('updated')
            this.loadRecords()
        }, 10000);
        onWillUnmount(() => clearInterval(this.update_intervals));   // clear interval not to fire error on navigate
    }

    // async loadRecords(){
    //     let result = await this.orm.searchRead("my_module.property" , [] , [])
    //     this.state.records = result
    // }

    async loadRecords () {
        let results = await this.rpc("/web/dataset/call_kw" , {
            model:"my_module.property" , 
            method:"search_read" , 
            args:[[]],
            kwargs:{fields : ['name' , 'description' , 'post_code' , 'selling_price']}
        })

        this.state.records = results
    }

    // select the update record
    async update_record(id){
        let results = await this.rpc("/web/dataset/call_kw" , {
            model:"my_module.property" , 
            method:"search_read" , 
            args: [[['id', '=', id]]],  // only the domain
            kwargs: { fields: ['name', 'description', 'post_code', 'selling_price'] },
        })

        this.state.name = results[0].name
        this.state.id = results[0].id
    }

    // handle update 
    async ChangeName(){
        if(!this.state.name || !this.state.id)
            return 
        
        let results = await this.rpc("/web/dataset/call_kw" , {
            model:"my_module.property" , 
            method:"write" , 
            args: [[this.state.id]],
            kwargs: {
                vals: {
                    name: this.state.name
                }
            }
        })

        this.state.id = null 
        this.state.name = null

        this.loadRecords()

        console.log(results)
    }
}

registry.category("actions").add("my_module.list_view_action" , ListViewAction);