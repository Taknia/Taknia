odoo.define('taknia_branch_management.kpi_charts', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var fieldRegistry = require('web.field_registry');

    var KPIChartField = AbstractField.extend({
        template: 'KPIChartField',
        jsLibs: [
            '/taknia_branch_management/static/lib/chart.js/Chart.min.js',
        ],
        cssLibs: [
            '/taknia_branch_management/static/lib/chart.js/Chart.min.css',
        ],
        _render: function () {
            this._super.apply(this, arguments);
            this.$el.html('<canvas id="kpi_chart"></canvas>');
            var ctx = this.$el.find('#kpi_chart')[0].getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['KPI 1', 'KPI 2', 'KPI 3'],
                    datasets: [{
                        label: 'KPI Values',
                        data: [10, 20, 30],
                        backgroundColor: ['#2196F3', '#4CAF50', '#FF9800'],
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
        },
    });

    fieldRegistry.add('kpi_chart', KPIChartField);

    return KPIChartField;
});