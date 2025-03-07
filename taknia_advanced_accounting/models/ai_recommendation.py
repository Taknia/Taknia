from odoo import models, fields, api, _
import requests
import json

class AIRecommendation(models.Model):
    _name = 'taknia.financial.advice.ai'
    _description = 'AI Financial Recommendations'

    financial_report_id = fields.Many2one('taknia.financial.report', string="Related Financial Report")
    recommendation = fields.Text(string='AI Recommendation')
    action_type = fields.Selection([
        ('reminder', 'Set Reminder'),
        ('email', 'Send Email to Manager'),
        ('budget_revision', 'Request Budget Revision')
    ], string='Suggested Action')

    @api.model
    def get_advice(self, report):
        """ استدعاء OpenAI API لتحليل التقرير واقتراح توصيات مالية """
        ai_prompt = self._prepare_prompt(report)
        ai_response = self._call_openai_api(ai_prompt)

        recommendation_text = ai_response.get('recommendation', "No recommendation available.")
        suggested_action = ai_response.get('action', 'reminder')

        # حفظ التوصية في السجل
        advice_record = self.create({
            'financial_report_id': report.id,
            'recommendation': recommendation_text,
            'action_type': suggested_action,
        })

        # تنفيذ الإجراء المقترح
        advice_record._execute_suggested_action(report)

        return recommendation_text

    def _prepare_prompt(self, report):
        """ تجهيز الـ Prompt اللي هنرسله لـ OpenAI بناءً على بيانات التقرير """
        prompt = f"""
        You are an expert financial advisor for companies. 
        Here is the financial summary of the company:

        - Report Date: {report.report_date}
        - Branch: {report.branch_id.name if report.branch_id else 'All Branches'}
        - Total Assets: {report.total_assets}
        - Total Liabilities: {report.total_liabilities}
        - Total Equity: {report.total_equity}
        - Net Profit: {report.net_profit}
        - Total Revenue: {report.revenue}
        - Total Expenses: {report.expenses}

        Based on this data, please provide a brief financial recommendation (2-3 lines) for management.

        Also, suggest a suitable action from the following:
        - Set Reminder
        - Send Email to Manager
        - Request Budget Revision

        Please return a JSON object with:
        - recommendation: your financial advice
        - action: one of (reminder, email, budget_revision)
        """
        return prompt

    def _call_openai_api(self, prompt):
        """ اتصال مباشر مع OpenAI API """
        api_key = self.env['ir.config_parameter'].sudo().get_param('openai.api_key')
        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4",  # يمكن تغييره حسب الحاجة
            "messages": [{"role": "system", "content": "You are a financial advisor."},
                         {"role": "user", "content": prompt}],
            "temperature": 0.3,
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response_data = response.json()

            advice_text = response_data['choices'][0]['message']['content']

            # تحليل النص لوضعه في recommendation + action
            recommendation, action = self._parse_ai_response(advice_text)

            return {
                'recommendation': recommendation,
                'action': action
            }
        except Exception as e:
            return {
                'recommendation': "Failed to fetch AI recommendation.",
                'action': 'reminder'
            }

    def _parse_ai_response(self, text):
        """ تحليل الرد النصي من الذكاء الصناعي (لنفترض إنه بيبعته كسطرين: التوصية - الإجراء) """
        lines = text.strip().split('\n')
        recommendation = lines[0] if lines else "No recommendation provided."
        action = lines[1].strip().lower() if len(lines) > 1 else 'reminder'

        # تأكد أن الإجراء متوافق
        valid_actions = ['reminder', 'email', 'budget_revision']
        if action not in valid_actions:
            action = 'reminder'

        return recommendation, action

    def _execute_suggested_action(self, report):
        """ تنفيذ الإجراء المقترح مباشرة بعد استلام التوصية """
        if self.action_type == 'reminder':
            self._set_reminder(report)
        elif self.action_type == 'email':
            self._send_manager_email(report)
        elif self.action_type == 'budget_revision':
            self._request_budget_revision(report)

    def _set_reminder(self, report):
        """ إنشاء تذكير في Odoo """
        self.env['calendar.event'].create({
            'name': _("Review Financial Recommendation"),
            'start': fields.Datetime.now(),
            'stop': fields.Datetime.now(),
            'description': self.recommendation,
            'user_id': self.env.user.id,
        })

    def _send_manager_email(self, report):
        """ إرسال إيميل تنبيهي للمدير المالي """
        template = self.env.ref('taknia_advanced_accounting.email_template_financial_advice')
        if template:
            template.send_mail(report.id, force_send=True)

    def _request_budget_revision(self, report):
        """ فتح طلب مراجعة ميزانية جديد """
        self.env['budget.revision.request'].create({
            'report_id': report.id,
            'reason': _("AI Suggested Budget Revision"),
            'requested_by': self.env.user.id,
        })
