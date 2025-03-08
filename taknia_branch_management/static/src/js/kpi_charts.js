odoo.define('taknia_branch_management.kpi_charts', function (require) {
    'use strict';

    var rpc = require('web.rpc');

    function renderKPIChart(data) {
        // Render the KPI chart using the given data
        // Example: using Chart.js
        var ctx = document.getElementById('kpiChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    rpc.query({
        model: 'branch.kpi.dashboard',
        method: 'get_kpi_data',
    }).then(function (data) {
        renderKPIChart(data);
    });
});