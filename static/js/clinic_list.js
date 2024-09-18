document.addEventListener('DOMContentLoaded', function() {
    fetch('/clinics/api/clinics/')
        .then(response => response.json())
        .then(data => {
            $('#clinicsTable').DataTable({
                data: data,
                columns: [
                    { data: 'name' },
                    { data: 'phone_number' },
                    { data: 'city' },
                    { data: 'state' },
                    { data: 'doctor_count' },
                    { data: 'patient_count' },
                    {
                        data: null,
                        render: function(data, type, row) {
                            return `<a href="/clinics/${row.id}/" class="btn btn-primary btn-sm">View Details</a>`;
                        }
                    }
                ]
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load clinics data. Please try again.');
        });
});