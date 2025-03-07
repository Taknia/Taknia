// استخدام مكتبة Chart.js لعرض مؤشرات الأداء الرئيسية (KPI)

// التأكد من تحميل المكتبة
if (typeof Chart !== 'undefined') {
    // دالة لتهيئة وعرض الرسم البياني
    function renderKPIChart(ctx, labels, data, chartTitle, chartType) {
        new Chart(ctx, {
            type: chartType, // نوع الرسم البياني مثل "bar", "line", "pie"
            data: {
                labels: labels,
                datasets: [{
                    label: chartTitle,
                    data: data,
                    backgroundColor: '#4e73df', // اللون الأساسي للمؤشر
                    borderColor: '#2e59d9',
                    borderWidth: 1,
                    hoverBackgroundColor: '#2e59d9',
                    hoverBorderColor: '#1e3d8e',
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 10
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function (tooltipItem) {
                                return tooltipItem.raw + '%'; // إضافة رمز النسبة المئوية
                            }
                        }
                    }
                }
            }
        });
    }

    // دالة لإظهار الرسم البياني للـ KPI للإيرادات (Revenue)
    function showRevenueKPIChart() {
        const ctx = document.getElementById('kpi-revenue-chart').getContext('2d');
        const labels = ['Q1', 'Q2', 'Q3', 'Q4']; // تسميات الفترات الزمنية
        const data = [75, 80, 90, 95]; // بيانات الإيرادات في النسب المئوية
        renderKPIChart(ctx, labels, data, 'إيرادات الفروع', 'line');
    }

    // دالة لإظهار الرسم البياني للـ KPI لرضا العملاء (Customer Satisfaction)
    function showCustomerSatisfactionChart() {
        const ctx = document.getElementById('kpi-customer-satisfaction-chart').getContext('2d');
        const labels = ['الفرع 1', 'الفرع 2', 'الفرع 3']; // تسميات الفروع
        const data = [85, 90, 88]; // بيانات رضا العملاء
        renderKPIChart(ctx, labels, data, 'رضا العملاء', 'bar');
    }

    // دالة لإظهار الرسم البياني للـ KPI لأداء الموظفين (Employee Performance)
    function showEmployeePerformanceChart() {
        const ctx = document.getElementById('kpi-employee-performance-chart').getContext('2d');
        const labels = ['أبريل', 'مايو', 'يونيو', 'يوليو']; // تسميات الأشهر
        const data = [80, 75, 90, 95]; // بيانات الأداء
        renderKPIChart(ctx, labels, data, 'أداء الموظفين', 'line');
    }

    // دالة لتشغيل جميع الرسوم البيانية عند تحميل الصفحة
    document.addEventListener('DOMContentLoaded', function () {
        showRevenueKPIChart();
        showCustomerSatisfactionChart();
        showEmployeePerformanceChart();
    });
}
