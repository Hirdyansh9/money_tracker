var ctx = document.getElementById("transactionChart").getContext("2d");
var chartData = JSON.parse("{{chart_data | safe}}");

var chart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: chartData.map((item) => item.month),
    datasets: [
      {
        label: "Lent",
        data: chartData.map((item) => item.lent),
        backgroundColor: "rgba(75, 192, 192, 0.6)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
        hoverBackgroundColor: "rgba(75, 192, 192, 0.8)",
      },
      {
        label: "Borrowed",
        data: chartData.map((item) => item.borrowed),
        backgroundColor: "rgba(255, 99, 132, 0.6)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1,
        hoverBackgroundColor: "rgba(255, 99, 132, 0.8)",
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
      },
    },
    plugins: {
      tooltip: {
        callbacks: {
          label: function (tooltipItem) {
            return (
              tooltipItem.dataset.label + ": $" + tooltipItem.raw.toFixed(2)
            );
          },
        },
      },
    },
  },
});
