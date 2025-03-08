odoo.define('taknia_branch_management.Charts', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;

    var BranchCharts = AbstractAction.extend({
        template: 'taknia_branch_management.Charts',

        init: function(parent, context) {
            this._super(parent, context);
            this.charts = {};
        },

        start: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function() {
                self._initializeCharts();
            });
        },

        _initializeCharts: function() {
            this._createRevenueChart();
            this._createCustomerChart();
            this._createESGChart();
            this._createPerformanceChart();
        },

        _createRevenueChart: function() {
            var ctx = this.$el.find('#revenueChart')[0].getContext('2d');
            this.charts.revenue = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Actual Revenue',
                        backgroundColor: '#28a745',
                        data: []
                    }, {
                        label: 'Target Revenue',
                        backgroundColor: '#dc3545',
                        data: []
                    }]
                },
                options: this._getChartOptions('Revenue Analysis')
            });
        },

        _createCustomerChart: function() {
            var ctx = this.$el.find('#customerChart')[0].getContext('2d');
            this.charts.customers = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Customer Growth',
                        borderColor: '#7C7BAD',
                        data: []
                    }]
                },
                options: this._getChartOptions('Customer Trends')
            });
        },

        _createESGChart: function() {
            var ctx = this.$el.find('#esgChart')[0].getContext('2d');
            this.charts.esg = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: ['Environmental', 'Social', 'Governance'],
                    datasets: [{
                        label: 'ESG Score',
                        backgroundColor: 'rgba(124, 123, 173, 0.2)',
                        borderColor: '#7C7BAD',
                        data: []
                    }]
                },
                options: this._getChartOptions('ESG Performance')
            });
        },

        _createPerformanceChart: function() {
            var ctx = this.$el.find('#performanceChart')[0].getContext('2d');
            this.charts.performance = new Chart(ctx, {
                type: 'bubble',
                data: {
                    datasets: [{
                        label: 'Branch Performance',
                        backgroundColor: 'rgba(124, 123, 173, 0.5)',
                        data: []
                    }]
                },
                options: this._getChartOptions('Branch Performance Matrix')
            });
        },

        _getChartOptions: function(title) {
            return {
                responsive: true,
                maintainAspectRatio: false,
                title: {
                    display: true,
                    text: title
                },
                legend: {
                    position: 'bottom'
                },
                tooltips: {
                    mode: 'index',
                    intersect: false
                },
                scales: {
                    xAxes: [{
                        gridLines: {
                            color: 'rgba(0,0,0,0.05)'
                        }
                    }],
                    yAxes: [{
                        gridLines: {
                            color: 'rgba(0,0,0,0.05)'
                        },
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            };
        },

        updateChartData: function(chartId, newData) {
            var chart = this.charts[chartId];
            if (chart) {
                chart.data = newData;
                chart.update();
            }
        },

        destroy: function() {
            Object.values(this.charts).forEach(function(chart) {
                chart.destroy();
            });
            this._super.apply(this, arguments);
        }
    });

    return BranchCharts;
});
