$(document).ready(function () {
  
    console.log(chartData)
    let MonthYear = chartData.LineChartData["MonthYear"];
    let PortfolioValuation = chartData.LineChartData["PortfolioValuation"];

    new Chart($("#lineChart"), {
        type: "line",
        data: {
            labels: MonthYear,
            datasets: [{
                label: "Portfolio Valuation",
                data: PortfolioValuation,
                borderColor: "blue",
                fill: false
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: "Portfolio Valuation Over Time", // Chart Title
                    font: { size: 16 }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Month-Year" // X-Axis Title
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: "Portfolio Value (₹)" // Y-Axis Title
                    },
                    beginAtZero: true
                }
            }
        }
    });
});
