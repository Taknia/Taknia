from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class BranchComparison(models.Model):
    _name = 'branch.comparison.report'
    _description = 'Branch Financial Comparison Report'

    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.company)
    branch_ids = fields.Many2many('res.branch', string="Branches")
    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)
    comparison_data = fields.Text(string="Comparison Data", compute='_compute_comparison_data', store=False)
    ai_recommendations = fields.Text(string="AI Recommendations")

    def action_generate_comparison(self):
        """توليد التقرير المقارن بين الفروع"""
        data = self._get_branch_financial_data()
        self.comparison_data = self._format_comparison_data(data)
        self.ai_recommendations = self._generate_ai_recommendations(data)

    def _get_branch_financial_data(self):
        """استخراج البيانات المالية لكل فرع"""
        data = {}
        for branch in self.branch_ids:
            invoices = self.env['account.move'].search([
                ('branch_id', '=', branch.id),
                ('company_id', '=', self.company_id.id),
                ('invoice_date', '>=', self.date_from),
                ('invoice_date', '<=', self.date_to),
                ('state', '=', 'posted')
            ])

            total_sales = sum(inv.amount_total_signed for inv in invoices if inv.move_type == 'out_invoice')
            total_refunds = sum(inv.amount_total_signed for inv in invoices if inv.move_type == 'out_refund')
            net_sales = total_sales - total_refunds

            expenses = self.env['account.move.line'].search([
                ('branch_id', '=', branch.id),
                ('company_id', '=', self.company_id.id),
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to),
                ('account_id.internal_group', '=', 'expense'),
            ])
            total_expenses = sum(expense.debit for expense in expenses)

            data[branch.name] = {
                'sales': net_sales,
                'expenses': total_expenses,
                'profit': net_sales - total_expenses,
            }

        return data

    def _format_comparison_data(self, data):
        """تهيئة البيانات بشكل جدول نصي"""
        table = "Branch Comparison Report\n\n"
        table += f"Period: {self.date_from} - {self.date_to}\n\n"
        table += "{:<20} {:<15} {:<15} {:<15}\n".format("Branch", "Net Sales", "Expenses", "Profit")
        table += "-" * 70 + "\n"

        for branch, values in data.items():
            table += "{:<20} {:<15,.2f} {:<15,.2f} {:<15,.2f}\n".format(
                branch,
                values['sales'],
                values['expenses'],
                values['profit']
            )

        return table

    def _generate_ai_recommendations(self, data):
        """توصيات ذكاء صناعي بناءً على أداء الفروع"""
        recommendations = []
        sorted_branches = sorted(data.items(), key=lambda x: x[1]['profit'], reverse=True)

        if len(sorted_branches) >= 2:
            best_branch, worst_branch = sorted_branches[0], sorted_branches[-1]
            recommendations.append(f"أفضل فرع أداءً: {best_branch[0]} بصافي ربح {best_branch[1]['profit']:.2f}")
            recommendations.append(f"أقل فرع أداءً: {worst_branch[0]} بصافي ربح {worst_branch[1]['profit']:.2f}")

            profit_gap = best_branch[1]['profit'] - worst_branch[1]['profit']
            recommendations.append(f"الفرق في الربحية بين أفضل وأسوأ فرع: {profit_gap:.2f}")

            if profit_gap > 0:
                recommendations.append(f"ننصح بدراسة ممارسات فرع {best_branch[0]} لتطبيقها في فرع {worst_branch[0]}.")
            else:
                recommendations.append("يبدو أن أداء الفروع متقارب.")

        if all(values['profit'] <= 0 for values in data.values()):
            recommendations.append("جميع الفروع تحقق خسائر خلال هذه الفترة. ينصح بمراجعة الاستراتيجية المالية.")

        return "\n".join(recommendations)

    @api.model
    def cron_automatic_branch_comparison(self):
        """كرون جوب لتوليد تقرير مقارنة الفروع بشكل تلقائي (مثال يمكن تشغيله شهريًا)"""
        companies = self.env['res.company'].search([])
        for company in companies:
            branches = self.env['res.branch'].search([('company_id', '=', company.id)])
            if not branches:
                continue

            report = self.create({
                'company_id': company.id,
                'branch_ids': [(6, 0, branches.ids)],
                'date_from': fields.Date.today().replace(day=1),
                'date_to': fields.Date.today(),
            })
            try:
                report.action_generate_comparison()
                _logger.info(f"Branch Comparison Report auto-generated for company {company.name}")
            except Exception as e:
                _logger.error(f"Failed to generate branch comparison report for {company.name}: {str(e)}")

