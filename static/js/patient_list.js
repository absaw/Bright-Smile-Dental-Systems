document.addEventListener('DOMContentLoaded', function() {
    let table;

    function loadPatients() {
        fetch('/patients/api/patients/')
            .then(response => response.json())
            .then(data => {
                if ($.fn.DataTable.isDataTable('#patientsTable')) {
                    $('#patientsTable').DataTable().destroy();
                }
                table = $('#patientsTable').DataTable({
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
                    dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rtip'
                });
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to load patients data. Please try again.');
            });
    }

    document.getElementById('addPatientBtn').addEventListener('click', function() {
        $('#addPatientModal').modal('show');
        // document.getElementById("date_of_birth").setAttribute("max", "${new Date().toISOString().split('T')[0]}");
    });

    document.getElementById('submitAddPatient').addEventListener('click', function() {
        const form = document.getElementById('addPatientForm');
        
        if (form.checkValidity() === false) {
            form.reportValidity();
            return;
        }

        const formData = new FormData(form);

        fetch('/patients/api/add_patient/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                $('#addPatientModal').modal('hide');
                loadPatients(); // Reload the entire table
                alert('Patient added successfully!');
                form.reset();
            } else {
                alert('Failed to add patient. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while adding the patient.');
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    loadPatients();
});