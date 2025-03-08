# استيراد الملفات الرئيسية الأخرى
from . import accounting_report
from . import branch_comparison_report
from . import financial_kpi
from . import financial_health_score
from . import customer_profitability
from . import financial_advice_ai
from . import product_costing_analysis
from . import esg_analysis
from . import payment_integration
from . import bank_flow_analysis
from . import overdue_analysis
from . import res_config_settings

from . import branch
from . import branch_performance
from . import branch_budget

# استيراد kpi_dashboard داخل دالة متأخرة لتجنب التداخل
def load_kpi_dashboard():
    from . import kpi_dashboard  # التأكد من أن الاستيراد فقط عند الحاجة
