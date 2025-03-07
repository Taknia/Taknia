from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class PartnerProfitability(models.Model):
    _name = 'partner.profitability'
    _description = 'Partner Profitability Analysis'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.company)
    total_sales = fields.Float(string="Total Sales", compute='_compute_financial_data', store=True)
    total_cost = fields.Float(string="Total Cost", compute='_compute_financial_data', store=True)
    gross_profit = fields.Float(string="Gross Profit", compute='_compute_financial_data', store=True)
    profitability_ratio = fields.Float(string="Profitability Ratio (%)", compute='_compute_financial_data', store=True)
    analysis_date = fields.Datetime(string="Analysis Date", default=fields.Datetime.now)
    ai_recommendations = fields.Text(string="AI Recommendations")

    @api.depends('partner_id')
    def _compute_financial_data(self):
        for record in self:
            invoices = self.env['account.move'].search([
                ('partner_id', '=', record.partner_id.id),
                ('move_type', 'in', ['out_invoice', 'out_refund']),
                ('company_id', '=', record.company_id.id),
                ('state', '=', 'posted')
            ])

            total_sales = sum(inv.amount_total_signed for inv in invoices if inv.move_type == 'out_invoice')
            total_refunds = sum(inv.amount_total_signed for inv in invoices if inv.move_type == 'out_refund')
            record.total_sales = total_sales - total_refunds

            total_cost = sum(inv.amount_total_signed for inv in invoices if inv.invoice_line_ids)
            record.total_cost = total_cost * 0.65  # افتراضي: هامش الربح 35% - يمكن تطويره لاحقاً

            record.gross_profit = record.total_sales - record.total_cost
            record.profitability_ratio = (record.gross_profit / record.total_sales * 100) if record.total_sales else 0.0

    def action_analyze_partner_profitability(self):
        """ تشغيل التحليل اليدوي مع توصيات AI """
        for record in self:
            record.analysis_date = fields.Datetime.now()
            record.ai_recommendations = record._generate_ai_recommendations()
            _logger.info(f"Partner Profitability Analysis updated for partner: {record.partner_id.name}")

    def _generate_ai_recommendations(self):
        """ توصيات ذكاء صناعي مبدئية - يتم ربطها لاحقاً بـ ChatGPT API """
        recommendations = []
        if self.profitability_ratio > 30:
            recommendations.append(f"العميل {self.partner_id.name} يعد من العملاء ذوي الربحية العالية.")
            recommendations.append("ننصح بزيادة الاهتمام به وتقديم عروض خاصة.")
        elif self.profitability_ratio > 10:
            recommendations.append(f"العميل {self.partner_id.name} يحقق ربحية مقبولة.")
            recommendations.append("يمكن دراسة تقديم مزايا إضافية لتحسين العلاقة.")
        else:
            recommendations.append(f"العميل {self.partner_id.name} يحقق هامش ربح ضعيف.")
            recommendations.append("ننصح بمراجعة شروط التعامل والأسعار.")

        return "\n".join(recommendations)

    @api.model
    def cron_automatic_partner_profitability_analysis(self):
        """ كرون جوب لتحليل ربحية العملاء لكل الشركات """
        companies = self.env['res.company'].search([])
        for company in companies:
            partners = self.env['res.partner'].search([('company_id', '=', company.id), ('customer_rank', '>', 0)])
            for partner in partners:
                record = self.search([('partner_id', '=', partner.id), ('company_id', '=', company.id)], limit=1)
                if not record:
                    record = self.create({
                        'partner_id': partner.id,
                        'company_id': company.id
                    })
                try:
                    record.action_analyze_partner_profitability()
                except Exception as e:
                    _logger.error(f"Failed to analyze partner profitability for {partner.name}: {str(e)}")
