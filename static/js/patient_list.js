document.addEventListener('DOMContentLoaded', function() {
    fetch('/patients/api/patients/')
        .then(response => response.json())
        .then(data => {
            $('#patientsTable').DataTable({
                data: data,
                columns: [
                    { data: 'name' },
                    { data: 'date_of_birth' },
                    { data: 'last_visit_date' },
                    { data: 'last_visit_doctor' },
                    { data: 'last_visit_procedures' },
                    { data: 'next_appointment_date' },
                    { data: 'next_appointment_doctor' },
                    { data: 'next_appointment_procedure' },
                    {
                        data: null,
                        render: function(data, type, row) {
                            return `<a href="/patients/${row.id}/" class="btn btn-primary btn-sm">View/Edit</a>`;
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
            alert('Failed to load patients data. Please try again.');
        });
});