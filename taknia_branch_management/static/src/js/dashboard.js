odoo.define('taknia_branch_management.Dashboard', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;
    var rpc = require('web.rpc');
    var session = require('web.session');

    var BranchDashboard = AbstractAction.extend({
        template: 'taknia_branch_management.Dashboard',
        events: {
            'click .refresh-dashboard': '_onRefreshDashboard',
            'click .view-details': '_onViewDetails',
            'change .period-selector': '_onPeriodChange',
        },

        init: function(parent, context) {
            this._super(parent, context);
            this.dashboardData = {};
            this.selectedPeriod = 'monthly';
            this.charts = {};
        },

        willStart: function() {
            return $.when(
                this._super.apply(this, arguments),
                this._loadDashboardData()
            );
        },

        start: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function() {
                self._initializeCharts();
                self._setupRefreshInterval();
            });
        },

        _loadDashboardData: function() {
            var self = this;
            return rpc.query({
                model: 'taknia.branch',
                method: 'get_dashboard_data',
                args: [this.selectedPeriod],
            }).then(function(result) {
                self.dashboardData = result;
            });
        },

        _initializeCharts: function() {
            this._initializePerformanceChart();
            this._initializeRevenueChart();
            this._initializeESGChart();
            this._initializeCustomerChart();
        },

        _initializePerformanceChart: function() {
            // Implementation using Chart.js
            var ctx = this.$el.find('#performanceChart')[0].getContext('2d');
            this.charts.performance = new Chart(ctx, {
                type: 'line',
                data: this._getPerformanceChartData(),
                options: this._getChartOptions('Performance Trends')
            });
        },

        _getPerformanceChartData: function() {
            return {
                labels: this.dashboardData.periods || [],
                datasets: [{
                    label: 'Performance Score',
                    data: this.dashboardData.performance || [],
                    borderColor: '#7C7BAD',
                    fill: false
                }]
            };
        },

        _getChartOptions: function(title) {
            return {
                responsive: true,
                maintainAspectRatio: false,
                title: {
                    display: true,
                    text: title
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                },
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Period'
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Value'
                        }
                    }]
                }
            };
        },

        _setupRefreshInterval: function() {
            var self = this;
            this.refreshInterval = setInterval(function() {
                self._onRefreshDashboard();
            }, (session.branch_dashboard_refresh_interval || 5) * 60 * 1000);
        },

        _onRefreshDashboard: function(ev) {
            if (ev) { ev.preventDefault(); }
            var self = this;
            return this._loadDashboardData().then(function() {
                self._updateCharts();
                self._updateKPIs();
            });
        },

        _updateCharts: function() {
            Object.values(this.charts).forEach(function(chart) {
                chart.update();
            });
        },

        _updateKPIs: function() {
            this.$('.kpi-value').each(function() {
                var $kpi = $(this);
                var metric = $kpi.data('metric');
                var value = this.dashboardData[metric];
                $kpi.text(value);
            });
        },

        _onViewDetails: function(ev) {
            ev.preventDefault();
            var actionName = $(ev.currentTarget).data('action');
            this.do_action(actionName);
        },

        _onPeriodChange: function(ev) {
            this.selectedPeriod = $(ev.currentTarget).val();
            this._onRefreshDashboard();
        },

        destroy: function() {
            if (this.refreshInterval) {
                clearInterval(this.refreshInterval);
            }
            this._super.apply(this, arguments);
        }
    });

    core.action_registry.add('branch_dashboard', BranchDashboard);

    return BranchDashboard;
});
