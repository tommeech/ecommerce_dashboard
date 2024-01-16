// Initiate a fetch request to the '/api/low_stock_levels' endpoint
fetch('/api/low_stock_levels')
    // Parse the fetched response as JSON
    .then(response => response.json())
    // Use the parsed data to render the chart
    .then(data => {
        // Get the 2D rendering context of the HTML5 Canvas element with the id 'stockChart'
        const ctx = document.getElementById('stockChart').getContext('2d');
        
        // Create a new Chart.js instance to render a bar chart
        new Chart(ctx, {
            type: 'bar',  // Specify the type of chart as 'bar'
            data: {
                labels: data.products,  // Set the x-axis labels to the product names
                datasets: [{
                    label: 'Stock Quantity',  // Set the label for the dataset
                    data: data.quantities,  // Set the data for the bars as the stock quantities
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',  // Set the background color of the bars
                    borderColor: 'rgba(255, 99, 132, 1)',  // Set the border color of the bars
                    borderWidth: 1  // Set the border width of the bars to 1 pixel
                }]
            },
            options: {
                responsive: true,  // Ensure the chart is responsive to window resizing
                scales: {
                    yAxes: [{
                        beginAtZero: true  // Start the y-axis scale at zero
                    }],
                    xAxes: [{
                        display: true
                    }]
                }
            }
        });
    });
