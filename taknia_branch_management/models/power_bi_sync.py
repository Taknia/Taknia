import requests
import json
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class BranchPowerBISync(models.Model):
    _name = "branch.power.bi.sync"
    _description = "Branch Power BI Synchronization"

    name = fields.Char(string="Sync Name", required=True, default=lambda self: _("New Power BI Sync"))
    branch_ids = fields.Many2many("res.branch", string="Branches")
    dataset_id = fields.Char(string="Power BI Dataset ID", required=True)
    last_sync_date = fields.Datetime(string="Last Sync Date", readonly=True)
    sync_status = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string="Sync Status", default="pending", readonly=True)
    access_token = fields.Char(string="Power BI Access Token", required=True)

    def action_sync_with_power_bi(self):
        """ Synchronize branch data with Power BI """
        for record in self:
            if not record.dataset_id or not record.access_token:
                raise UserError(_("Please provide Power BI Dataset ID and Access Token."))

            url = f"https://api.powerbi.com/v1.0/myorg/datasets/{record.dataset_id}/rows"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {record.access_token}'
            }

            branch_data = []
            for branch in record.branch_ids:
                branch_data.append({
                    "branch_id": branch.id,
                    "branch_name": branch.name,
                    "revenue": branch.total_revenue,
                    "expenses": branch.total_expenses,
                    "profit": branch.total_revenue - branch.total_expenses,
                    "employee_count": branch.employee_count,
                    "created_date": branch.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                })

            try:
                response = requests.post(url, headers=headers, data=json.dumps(branch_data))
                if response.status_code in [200, 201]:
                    record.write({
                        "last_sync_date": fields.Datetime.now(),
                        "sync_status": "success"
                    })
                else:
                    _logger.error(f"Power BI Sync Failed: {response.text}")
                    record.write({"sync_status": "failed"})
                    raise UserError(_("Failed to sync with Power BI. Check your credentials and dataset ID."))

            except Exception as e:
                _logger.error(f"Power BI Sync Exception: {e}")
                record.write({"sync_status": "failed"})
                raise UserError(_("An error occurred while syncing with Power BI."))

