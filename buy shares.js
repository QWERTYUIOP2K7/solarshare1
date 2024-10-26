let totalSavings = 0;

function buyShare(project, price) {
    totalSavings += price; // Add the price of the share to total savings
    document.getElementById('totalSavings').innerText = totalSavings;
    alert('You have successfully bought a share in this solar farm for ₹100');
}