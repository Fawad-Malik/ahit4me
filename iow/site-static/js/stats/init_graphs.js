window.onload = function () {
    // number_practices
    var number_practices_ctx = document.getElementById('number_practices').getContext('2d');
    window.number_practices = new Chart(number_practices_ctx, number_practices_config);

    // total_hours
    var total_hours_ctx = document.getElementById('total_hours').getContext('2d');
    window.total_hours = new Chart(total_hours_ctx, total_hours_config);

    // total_hours
    var fulfilment_ctx = document.getElementById('fulfilment').getContext('2d');
    window.total_hours = new Chart(fulfilment_ctx, fulfilment_config);
};

