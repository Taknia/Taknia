odoo.define('taknia_advanced_accounting.kpi_charts', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.KpiDashboard = publicWidget.Widget.extend({
        selector: '.kpi-dashboard-container',
        start: function () {
            this._loadCharts();
        },

        _loadCharts: function () {
            var self = this;
            var chartDataUrl = '/taknia_advanced_accounting/get_kpi_data';

            $.getJSON(chartDataUrl, function (data) {
                self._renderChart('kpi-revenue-chart', 'Revenue Growth', data.revenue);
                self._renderChart('kpi-profit-chart', 'Profit Margin', data.profit_margin);
                self._renderChart('kpi-customer-growth-chart', 'Customer Growth', data.customer_growth);
            });
        },

        _renderChart: function (containerId, title, data) {
            var ctx = document.getElementById(containerId).getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: title,
                        data: data.values,
                        borderColor: '#007bff',
                        backgroundColor: 'rgba(0, 123, 255, 0.2)',
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        },
    });

    return publicWidget.registry.KpiDashboard;
});
