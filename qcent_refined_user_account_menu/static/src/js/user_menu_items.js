/** @odoo-module **/

import { registry } from "@web/core/registry";

// Access the user menu registry and remove specific items
const userMenuRegistry = registry.category("user_menuitems");
userMenuRegistry.remove("documentation");  // Remove documentation item
userMenuRegistry.remove("support");        // Remove support item
userMenuRegistry.remove("shortcuts");      // Remove shortcuts item
userMenuRegistry.remove("odoo_account");   // Remove My Odoo.com account item

console.log("Custom user menu items modified: documentation, support, and shortcuts removed.");
