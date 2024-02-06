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
    // X-axis labels representing dates
    labels: data.dates,
    datasets: [
      {
        // Legend label
        label: "Number of Orders",
        // Y-axis data representing the count of orders
        data: data.counts,
      },
    ],
  },
}));

//  usage for a bar chart showing products with low stock levels
fetchDataAndRenderChart("/api/low_stock_levels", "stockChart", (data) => ({
  type: "bar",
  data: {
    // X-axis labels representing product names
    labels: data.products,
    datasets: [
      {
        // Legend label
        label: "Low Stock",
        // Y-axis data representing the quantity of low stock
        data: data.quantities,
      },
    ],
  },
  options: {
    // Chart responsiveness and scales configuration
    responsive: true,
    scales: {
      y: {
        beginAtZero: true, // Start Y-axis from zero
      },
      x: {
        display: false, // Hide X-axis labels
      },
    },
  },
}));

// Example usage for a bar chart showing most popular products
fetchDataAndRenderChart("/api/most_popular_products", "popularProductsChart", (data) => ({
  type: "bar",
  data: {
    // X-axis labels representing product names from the data
    labels: data.map((item) => item.product_name),
    datasets: [
      {
        // Legend label
        label: "Quantity Sold",
        // Y-axis data representing the total quantity sold for each product
        data: data.map((item) => item.total_quantity),
      },
    ],
  },
  options: {
    // Chart responsiveness and scales configuration
    responsive: true,
    scales: {
      y: {
        beginAtZero: true, // Start Y-axis from zero
      },
      x: {
        display: false, // Hide X-axis labels
      },
    },
  },
}));

// Revenue Generation Chart
fetchDataAndRenderChart("/api/revenue_generation", "revenueChart", (data) => ({
  type: "line",
  data: {
    // X-axis labels representing dates
    labels: data.dates,
    datasets: [
      {
        // Legend label
        label: "Total Revenue",
        // Y-axis data representing total revenue
        data: data.revenues,
      },
    ],
  },
}));

// Product Category Popularity Chart
fetchDataAndRenderChart("/api/product_category_popularity", "categoryPopularityChart", (data) => ({
  type: "pie",
  data: {
    // Labels for different product categories
    labels: data.categories,
    datasets: [
      {
        // Legend label
        label: "Total Sales",
        // Data representing total sales for each product category
        data: data.sales,
      },
    ],
  },
}));

// Payment Method Popularity Chart
fetchDataAndRenderChart("/api/payment_method_popularity", "paymentMethodChart", (data) => ({
  type: "pie",
  data: {
    // Labels for different payment methods
    labels: data.methods,
    datasets: [
      {
        // Legend label
        label: "Transaction Count",
        // Data representing the transaction count for each payment method
        data: data.counts,
      },
    ],
  },
  options: {
    // Chart responsiveness and scales configuration
    responsive: true,
    scales: {
      x: {
        display: false, // Hide X-axis labels
      },
    },
  },
}));

// Temperature Over Time Chart
fetchDataAndRenderChart("/api/temperature_over_time", "temperatureChart", (data) => ({
  type: "line",
  data: {
    // X-axis labels representing daily time points
    labels: data.daily.time,
    datasets: [
      {
        // Legend label
        label: "Temperature (°C)",
        // Y-axis data representing maximum daily temperatures
        data: data.daily.temperature_2m_max,
        borderColor: "rgba(255, 0, 0, 1)", // Red border color
        backgroundColor: "rgba(200, 0, 192, 0.2)", // Purple fill color with opacity
        fill: false, // Do not fill the area under the line
      },
    ],
  },
}));
