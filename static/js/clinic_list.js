document.addEventListener('DOMContentLoaded', function() {
    let clinicsTable;

    function loadClinicsData() {
        fetch('/clinics/api/clinics/')
            .then(response => response.json())
            .then(data => {
                if (clinicsTable) {
                    clinicsTable.destroy();
                }
                clinicsTable = $('#clinicsTable').DataTable({
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
                                return `<a href="/clinics/${row.id}/" class="btn btn-primary btn-sm">View/Edit</a>`;
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
                alert('Failed to load clinics data. Please try again.');
            });
    }

    loadClinicsData();

    document.getElementById('add-clinic-btn').addEventListener('click', function() {
        $('#addClinicModal').modal('show');
    });

    document.getElementById('save-add-clinic-btn').addEventListener('click', function() {
        const form = document.getElementById('add-clinic-form');
        
        if (form.checkValidity() === false) {
            form.reportValidity();
            return;
        }

        const formData = new FormData(form);

        fetch('/clinics/api/clinics/add/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                $('#addClinicModal').modal('hide');
                loadClinicsData();
                form.reset();
            } else {
                alert('Failed to add clinic. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while adding the clinic.');
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
});

// document.addEventListener('DOMContentLoaded', function() {
//     fetch('/clinics/api/clinics/')
//         .then(response => response.json())
//         .then(data => {
//             $('#clinicsTable').DataTable({
//                 data: data,
//                 columns: [
//                     { data: 'name' },
//                     { data: 'phone_number' },
//                     { data: 'city' },
//                     { data: 'state' },
//                     { data: 'doctor_count' },
//                     { data: 'patient_count' },
//                     {
//                         data: null,
//                         render: function(data, type, row) {
//                             return `<a href="/clinics/${row.id}/" class="btn btn-primary btn-sm">View/Edit</a>`;
//                         }
//                     }
//                 ],
//                 pageLength: 25,
//                 lengthMenu: [25, 50, 100],
//                 order: [[0, 'asc']],
//                 language: {
//                     search: "",
//                     searchPlaceholder: "Search..."
//                 },
//                 layout: {
//                     top: {
//                         searchPane: {
//                             className: 'row',
//                             rows: [
//                                 {
//                                     className: 'col-sm-12 col-md-6',
//                                     cells: [{ data: 'f' }]
//                                 },
//                                 {
//                                     className: 'col-sm-12 col-md-6',
//                                     cells: [{ data: 'l' }]
//                                 }
//                             ]
//                         }
//                     },
//                     bottom: 'rtip'
//                 }
//             });
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             alert('Failed to load clinics data. Please try again.');
//         });
// });