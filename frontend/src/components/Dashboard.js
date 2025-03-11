import React, { useState, useEffect } from "react";
import axios from "axios";
import { Bar, Pie } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from "chart.js";
import "bootstrap/dist/css/bootstrap.min.css";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const Dashboard = () => {
  const [portfolioData, setPortfolioData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState("portfolio");

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/dashboard")
      .then((response) => {
        setPortfolioData(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center mt-5">Loading dashboard...</div>;

  // Data for Portfolio Summary Bar Chart
  const sortedPortfolio = Object.entries(portfolioData.portfolio.month_wise)
    .sort((a, b) => a[1].PortfolioValuationIn - b[1].PortfolioValuationIn);

  const portfolioMonths = sortedPortfolio.map(([month]) => month);
  const portfolioValues = sortedPortfolio.map(([, details]) => details.PortfolioValuationIn);

  const portfolioChartData = {
    labels: portfolioMonths,
    datasets: [
      {
        label: "Portfolio Valuation (₹)",
        data: portfolioValues,
        backgroundColor: "rgba(54, 162, 235, 0.6)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1,
      },
    ],
  };

  // Data for Asset Allocation Pie Chart
  const assetTypes = Object.keys(portfolioData.asset_allocation);
  const assetValues = assetTypes.map((type) => portfolioData.asset_allocation[type].Value);

  const assetAllocationChartData = {
    labels: assetTypes,
    datasets: [
      {
        data: assetValues,
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"],
      },
    ],
  };

  // Data for CDSL Holdings Pie Chart
  const cdslHoldings = Object.entries(portfolioData.CDSLHoldings);
  const cdslStockNames = cdslHoldings.map(([_, details]) => details.Security);
  const cdslStockValues = cdslHoldings.map(([_, details]) => details.Value);

  const cdslHoldingsChartData = {
    labels: cdslStockNames,
    datasets: [
      {
        data: cdslStockValues,
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"],
      },
    ],
  };

  // Data for Industry-Wise Stacked Bar Chart
 // Data for Industry-Wise Stacked Bar Chart (Now using count instead of total value)
// Generate unique colors for industries with multiple stocks
// Group stocks by industry
// Group stocks by industry
const industryStockData = {};
const stockColors = {};

cdslHoldings.forEach(([_, details]) => {
  const { Industry, Security, Value } = details;
  if (Industry && Industry !== "null") {
    if (!industryStockData[Industry]) {
      industryStockData[Industry] = {};
    }
    industryStockData[Industry][Security] = Value;

    if (!stockColors[Security]) {
      stockColors[Security] = `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.7)`;
    }
  }
});

const industryLabels = Object.keys(industryStockData);
const allStocks = [...new Set(cdslHoldings.map(([_, details]) => details.Security))];

const stackedDatasets = allStocks.map(stock => ({
  label: stock,
  data: industryLabels.map(industry => stock in industryStockData[industry] ? 1 : 0),
  backgroundColor: stockColors[stock],
}));

const industryStackedChartData = {
  labels: industryLabels,
  datasets: stackedDatasets,
};

  return (
    <div className="container mt-4">

  {/* Bordered Main Content Wrapper */}
  <div className="p-4 border rounded shadow bg-white"> 
    {/* Cards Section */}
    <div className="row d-flex justify-content-center mb-4">
      <div className="col-md-3 mx-2" onClick={() => setView("cdsl")}>
        <div className="card text-center bg-light">
          <div className="card-body">
            <h5 className="card-title">CDSL Demat</h5>
            <p className="card-text">
              <strong>Value: ₹{portfolioData.accounts["CDSL Demat Account"].Valuein}</strong>
            </p>
          </div>
        </div>
      </div>

      <div className="col-md-3 mx-2" onClick={() => setView("mf")}>
        <div className="card text-center bg-light">
          <div className="card-body">
            <h5 className="card-title">Mutual Funds</h5>
            <p className="card-text">
              <strong>Value: ₹{portfolioData.accounts["Mutual Fund Folios"].Valuein}</strong>
            </p>
          </div>
        </div>
      </div>

      <div className="col-md-3 mx-2" onClick={() => setView("portfolio")}>
        <div className="card text-center bg-light">
          <div className="card-body">
            <h5 className="card-title">Total Portfolio</h5>
            <p className="card-text">
              <strong>Value: ₹{portfolioData.accounts[""].Valuein}</strong>
            </p>
          </div>
        </div>
      </div>
    </div>

    {/* Portfolio View */}
    {view === "portfolio" && (
      <>
        <h4 className="mt-4 text-center">Portfolio Summary</h4>
        <div style={{ display: "flex", justifyContent: "center", width: "100%" }}>
          <div style={{ height: "400px", width: "70%" }}> {/* Increased size & centered */}
            <Bar 
              data={portfolioChartData} 
              options={{ 
                responsive: true, 
                maintainAspectRatio: false  // Allows chart to expand 
              }} 
            />
          </div>
        </div>

        {/* Asset Allocation */}
        <h4 className="mt-4 text-center">Asset Allocation</h4>
        <div className="row align-items-center g-0"> {/* Reduced gap using g-0 */}
          <div className="col-md-5 d-flex justify-content-center" style={{ height: "250px" }}>
            <Pie data={assetAllocationChartData} options={{ responsive: true, maintainAspectRatio: false }} />
          </div>
          <div className="col-md-7">
            <table className="table table-bordered mb-0"> {/* Reduced bottom margin */}
              <thead>
                <tr>
                  <th>Asset Type</th>
                  <th>Value (₹)</th>
                  <th>Percentage (%)</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(portfolioData.asset_allocation).map(([type, details]) => (
                  <tr key={type}>
                    <td>{type}</td>
                    <td>{details.Value}</td>
                    <td>{details.Percentage}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </>
    )}

    {/* MF Holdings View */}
    {view === "mf" && (
      <div className="d-flex justify-content-center align-items-center vh-100">
        <h2><strong>Mutual Fund Dashboard Under Development</strong></h2>
      </div>
    )}

    {/* CDSL Holdings View */}
    {view === "cdsl" && (
      <>
        <h4 className="mt-4">CDSL Holdings</h4>
        <button className="btn btn-secondary mb-2" onClick={() => setView("portfolio")}>Back</button>
        <div style={{ height: "300px", width: "100%" }}>
          <Pie data={cdslHoldingsChartData} options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { display: true, position: "right", align: "start"}, tooltip: { enabled: true } } }} />
        </div> 

        <h4 className="mt-4">Industry-Wise Stock Distribution</h4>                  
        <div style={{ display: "flex", justifyContent: "center", width: "100%" }}>
          <div style={{ height: "400px", width: "100%" }}>
          <Bar 
            data={industryStackedChartData} 
            options={{ 
              responsive: true, 
              maintainAspectRatio: false, 
              plugins: { 
                legend: { display: false },
                tooltip: {
                  callbacks: {
                    label: function (context) {
                      const industry = context.label;
                      const stock = context.dataset.label;
                      const value = industryStockData[industry][stock];
                      return `${stock}: ₹${value.toLocaleString()}`;
                    }
                  }
                }
              },
              scales: { 
                x: { stacked: true },
                y: {
                  stacked: true,
                  title: {
                    display: true,
                    text: 'Number of Stocks'
                  }
                }
              }
            }} 
          />
        </div>
        </div>
      </>
    )}
  </div> {/* End of bordered container */}
</div>

  );
};

export default Dashboard;
