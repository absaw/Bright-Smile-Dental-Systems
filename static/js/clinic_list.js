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
                ],
                pageLength: 25,
                lengthMenu: [25, 50, 100],
                order: [[0, 'asc']],
                language: {
                    search: "",
                    searchPlaceholder: "Search..."
                },
                layout: {
                    top: {
                        searchPane: {
                            className: 'row',
                            rows: [
                                {
                                    className: 'col-sm-12 col-md-6',
                                    cells: [{ data: 'f' }]
                                },
                                {
                                    className: 'col-sm-12 col-md-6',
                                    cells: [{ data: 'l' }]
                                }
                            ]
                        }
                    },
                    bottom: 'rtip'
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load clinics data. Please try again.');
        });
});