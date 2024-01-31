// Function to fetch data from an API endpoint and render a Chart.js chart
async function fetchDataAndRenderChart(apiEndpoint, chartElementId, chartConfig) {
  try {
    // Fetch data from the specified API endpoint
    let response = await fetch(apiEndpoint);
    let data = await response.json();

    // Get the 2D rendering context of the chart canvas
    const ctx = document.getElementById(chartElementId).getContext("2d");

    // Create a new Chart instance with the specified configuration and data
    new Chart(ctx, chartConfig(data));
  } catch (error) {
    // Log and handle errors that occur during data fetching or chart rendering
    console.error("Error fetching or rendering chart:", error);
  }
}

// Example usage of fetchDataAndRenderChart to create a line chart for orders over time
fetchDataAndRenderChart("/api/orders_over_time", "ordersChart", (data) => ({
  type: "line",
  data: {
    labels: data.dates,
    datasets: [
      {
        label: "Number of Orders",
        data: data.counts,
      },
    ],
  },
}));

// Example usage for a bar chart showing products with low stock levels
fetchDataAndRenderChart("/api/low_stock_levels", "stockChart", (data) => ({
  type: "bar",
  data: {
    labels: data.products,
    datasets: [
      {
        label: "Low Stock",
        data: data.quantities,
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
      },
      x: {
        display: false, // This will hide the x-axis labels
      },
    },
  },
}));

// Example usage for a bar chart showing most popular products
fetchDataAndRenderChart("/api/most_popular_products", "popularProductsChart", (data) => ({
  type: "bar",
  data: {
    labels: data.map((item) => item.product_name),
    datasets: [
      {
        label: "Quantity Sold",
        data: data.map((item) => item.total_quantity),
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
      },
      x: {
        display: false, // This will hide the x-axis labels
      },
    },
  },
}));

// Revenue Generation Chart
fetchDataAndRenderChart("/api/revenue_generation", "revenueChart", (data) => ({
  type: "line",
  data: {
    labels: data.dates,
    datasets: [
      {
        label: "Total Revenue",
        data: data.revenues,
      },
    ],
  },
}));

// Product Category Popularity Chart
fetchDataAndRenderChart("/api/product_category_popularity", "categoryPopularityChart", (data) => ({
  type: "pie",
  data: {
    labels: data.categories,
    datasets: [
      {
        label: "Total Sales",
        data: data.sales,
      },
    ],
  },
}));

// Payment Method Popularity Chart
fetchDataAndRenderChart("/api/payment_method_popularity", "paymentMethodChart", (data) => ({
  type: "pie",
  data: {
    labels: data.methods,
    datasets: [
      {
        label: "Transaction Count",
        data: data.counts,
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      x: {
        display: false, // This will hide the x-axis labels
      },
    },
  },
}));

// Temperature Over Time Chart
fetchDataAndRenderChart("/api/temperature_over_time", "temperatureChart", (data) => ({
  type: "line",
  data: {
    labels: data.daily.time,
    datasets: [
      {
        label: "Temperature (°C)",
        data: data.daily.temperature_2m_max,
        borderColor: "rgba(255, 0, 0, 1)",
        backgroundColor: "rgba(200, 0, 192, 0.2)",
        fill: false,
      },
    ],
  },
}));
