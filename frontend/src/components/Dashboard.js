import React, { useState, useEffect } from "react";
import axios from "axios";
import { Bar, Pie, Scatter } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement, ScatterController, LineElement, PointElement} from "chart.js";
import "bootstrap/dist/css/bootstrap.min.css";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement, ScatterController, LineElement, PointElement);

const Dashboard = () => {
  const [portfolioData, setPortfolioData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState("portfolio");

  useEffect(() => {
    const userId = localStorage.getItem("session_id");
    if (!userId) {
      console.error("User ID not found!");
      return;
    }
  
    axios.get(`http://127.0.0.1:5000/api/dashboard/${userId}`)
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
  if (!portfolioData) return <div className="text-center mt-5">No data available</div>;

// Portfolio Summary Bar Chart
const portfolioChartData = {
  labels: portfolioData?.portfolio?.length > 0 
    ? portfolioData.portfolio.map(entry => `${entry.month} ${entry.year}`)
    : [],
  datasets: [
    {
      label: "Portfolio Valuation (₹)",
      data: portfolioData?.portfolio?.length > 0 
        ? portfolioData.portfolio.map(entry => entry.value)
        : [],
      backgroundColor: "rgba(54, 162, 235, 0.6)",
      borderColor: "rgba(54, 162, 235, 1)",
      borderWidth: 1,
    },
  ],
};

// Asset Allocation Pie Chart
const assetAllocationChartData = {
  labels: portfolioData?.asset_allocation?.length > 0
    ? portfolioData.asset_allocation.map(item => item.name)
    : [],
  datasets: [
    {
      data: portfolioData?.asset_allocation?.length > 0
        ? portfolioData.asset_allocation.map(item => item.value)
        : [],
      backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"],
    },
  ],
};

// CDSL Holdings Pie Chart
const cdslHoldingsChartData = {
  labels: portfolioData?.CDSLHoldings?.length > 0
    ? portfolioData.CDSLHoldings.map(holding => holding.security)
    : [],
  datasets: [
    {
      data: portfolioData?.CDSLHoldings?.length > 0
        ? portfolioData.CDSLHoldings.map(holding => holding.value)
        : [],
      backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"],
    },
  ],
};

// Industry-Wise Stock Distribution
const industryStockData = {};
const stockColors = {};

if (portfolioData?.CDSLHoldings?.length > 0) {
  portfolioData.CDSLHoldings.forEach((details) => {
    const { security, value } = details;
    industryStockData[security] = { [security]: value };
    stockColors[security] = `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.7)`;
  });
}

const industryLabels = Object.keys(industryStockData);
const allStocks = portfolioData?.CDSLHoldings?.length > 0
  ? portfolioData.CDSLHoldings.map(details => details.security)
  : [];

const stackedDatasets = allStocks.length > 0
  ? allStocks.map(stock => ({
      label: stock,
      data: industryLabels.map(industry => industry === stock ? industryStockData[industry][stock] : 0),
      backgroundColor: stockColors[stock],
    }))
  : [];

const industryStackedChartData = {
  labels: industryLabels.length > 0 ? industryLabels : [],
  datasets: stackedDatasets,
};

 // Mutual Fund Data
 const mfHoldings = portfolioData?.MFHoldings || [];

 // Investment vs Valuation (Bar Chart)
 const investmentVsValuationData = {
   labels: mfHoldings.map(fund => fund.schemename),
   datasets: [
     {
       label: "Amount Invested (₹)",
       data: mfHoldings.map(fund => fund.cumulativeamountinvested),
       backgroundColor: "rgba(54, 162, 235, 0.6)",
     },
     {
       label: "Current Valuation (₹)",
       data: mfHoldings.map(fund => fund.valuation),
       backgroundColor: "rgba(255, 99, 132, 0.6)",
     }
   ]
 };

 // NAV Distribution (Bar Chart)
 const navDistributionData = {
   labels: mfHoldings.map(fund => fund.schemename),
   datasets: [
     {
       label: "NAV",
       data: mfHoldings.map(fund => fund.nav),
       backgroundColor: "rgba(75, 192, 192, 0.6)",
     }
   ]
 };

 // Expense Ratio vs Valuation (Scatter Plot)
 const expenseVsValuationData = {
   datasets: [
     {
       label: "Expense Ratio vs Valuation",
       data: mfHoldings.map(fund => ({
         x: fund.averagetotalexpenseratio,
         y: fund.valuation
       })),
       backgroundColor: "rgba(255, 206, 86, 0.6)",
       pointRadius: 5
     }
   ]
 };

 // Gross Commission Paid (Pie Chart)
 const commissionData = {
   labels: mfHoldings.map(fund => fund.schemename),
   datasets: [
     {
       data: mfHoldings.map(fund => fund.grosscommissionpaidtodistributors),
       backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"],
     }
   ]
 };



// Calculate total portfolio value
const totalPortfolioValue = portfolioData?.accounts?.length > 0
  ? portfolioData.accounts.reduce((sum, account) => sum + account.value, 0)
  : 0;
  return (
    <div className="container mt-4">
      <div className="p-4 border rounded shadow bg-white">
        {/* Cards Section */}
        <div className="row d-flex justify-content-center mb-4">
          <div className="col-md-3 mx-2" onClick={() => setView("cdsl")}>
            <div className="card text-center bg-light">
              <div className="card-body">
                <h5 className="card-title">CDSL Demat</h5>
                <p className="card-text">
                  <strong>Value: ₹{portfolioData.accounts[0].value.toLocaleString()}</strong>
                </p>
              </div>
            </div>
          </div>

          <div className="col-md-3 mx-2" onClick={() => setView("mf")}>
            <div className="card text-center bg-light">
              <div className="card-body">
                <h5 className="card-title">Mutual Funds</h5>
                <p className="card-text">
                  <strong>Value: ₹{portfolioData.accounts[1].value.toLocaleString()}</strong>
                </p>
              </div>
            </div>
          </div>

          <div className="col-md-3 mx-2" onClick={() => setView("portfolio")}>
            <div className="card text-center bg-light">
              <div className="card-body">
                <h5 className="card-title">Total Portfolio</h5>
                <p className="card-text">
                  <strong>Value: ₹{totalPortfolioValue.toLocaleString()}</strong>
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
              <div style={{ height: "400px", width: "70%" }}>
                <Bar 
                  data={portfolioChartData} 
                  options={{ 
                    responsive: true, 
                    maintainAspectRatio: false 
                  }} 
                />
              </div>
            </div>

            <h4 className="mt-4 text-center">Asset Allocation</h4>
            <div className="row align-items-center g-0">
              <div className="col-md-5 d-flex justify-content-center" style={{ height: "250px" }}>
                <Pie data={assetAllocationChartData} options={{ responsive: true, maintainAspectRatio: false }} />
              </div>
              <div className="col-md-7">
                <table className="table table-bordered mb-0">
                  <thead>
                    <tr>
                      <th>Asset Type</th>
                      <th>Value (₹)</th>
                      <th>Percentage (%)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {portfolioData.asset_allocation.map((item) => (
                      <tr key={item.name}>
                        <td>{item.name}</td>
                        <td>{item.value.toLocaleString()}</td>
                        <td>{item.percentage}</td>
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
          <>
          <h4 className="mt-4 text-center">Mutual Fund Insights</h4>

          {/* Investment vs Valuation */}
          <h5 className="mt-4">Investment vs. Valuation</h5>
          <div style={{ height: "400px", width: "100%" }}>
            <Bar data={investmentVsValuationData} options={{ responsive: true, maintainAspectRatio: false }} />
          </div>

          {/* NAV Distribution */}
          <h5 className="mt-4">NAV Distribution</h5>
          <div style={{ height: "300px", width: "100%" }}>
            <Bar data={navDistributionData} options={{ responsive: true, maintainAspectRatio: false }} />
          </div>

          {/* Expense Ratio vs Valuation */}
          <h5 className="mt-4">Expense Ratio vs. Valuation</h5>
          <div style={{ height: "300px", width: "100%" }}>
            <Scatter data={expenseVsValuationData} options={{ responsive: true, maintainAspectRatio: false }} />
          </div>

          {/* Gross Commission Paid */}
          <h5 className="mt-4">Gross Commission Paid</h5>
          <div style={{ height: "300px", width: "100%" }}>
            <Pie data={commissionData} options={{ responsive: true, maintainAspectRatio: false }} />
          </div>
        </>
        )}

        {/* CDSL Holdings View */}
        {view === "cdsl" && (
          <>
            <h4 className="mt-4">CDSL Holdings</h4>
            {portfolioData.CDSLHoldings?.length > 0 ? (
              <>
                <button className="btn btn-secondary mb-2" onClick={() => setView("portfolio")}>
                  Back
                </button>
                <div style={{ height: "300px", width: "100%" }}>
                  <Pie 
                    data={cdslHoldingsChartData}
                    options={{ 
                      responsive: true, 
                      maintainAspectRatio: false,
                      plugins: {
                        legend: { display: true, position: "right", align: "start" },
                        tooltip: { enabled: true }
                      }
                    }} 
                  />
                </div>
                <h4 className="mt-4">Stock Distribution</h4>
                <div style={{ display: "flex", justifyContent: "center", width: "100%" }}>
                  <div style={{ height: "400px", width: "100%" }}>
                    <Bar 
                      data={industryStackedChartData} 
                      options={{ 
                        responsive: true, 
                        maintainAspectRatio: false, 
                        plugins: { 
                          legend: { display: true },
                          tooltip: {
                            callbacks: {
                              label: function (context) {
                                const stock = context.dataset.label;
                                const value = context.raw;
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
                              text: 'Value (₹)'
                            }
                          }
                        }
                      }} 
                    />
                  </div>
                </div>
              </>
            ) : (
              <div className="text-center">No CDSL Holdings data available</div>
            )}
          </>
        )}
      </div>
    </div>
  );
};
export default Dashboard;