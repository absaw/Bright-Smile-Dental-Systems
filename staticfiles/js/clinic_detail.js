document.addEventListener('DOMContentLoaded', function() {
    const clinicId = window.location.pathname.split('/')[2];
    
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
    const csrftoken = getCookie('csrftoken');

    function loadClinicData() {
        fetch(`/clinics/api/clinics/${clinicId}/`)
            .then(response => response.json())
            .then(data => {
                const clinicInfoTable = document.querySelector('#clinic-info table tbody');
                clinicInfoTable.innerHTML = `
                    <tr><th>Name:</th><td>${data.name}</td></tr>
                    <tr><th>Address:</th><td>${data.address}</td></tr>
                    <tr><th>Phone Number:</th><td>${data.phone_number}</td></tr>
                    <tr><th>Email:</th><td>${data.email}</td></tr>
                `;

                if ($.fn.DataTable.isDataTable('#doctorsTable')) {
                    $('#doctorsTable').DataTable().destroy();
                }
                $('#doctorsTable').DataTable({
                    data: data.doctors,
                    columns: [
                        { data: 'name' },
                        { data: 'office_address' },
                        { data: 'working_schedule' },
                        {
                            data: null,
                            render: function(data, type, row) {
                                return `<button class="btn btn-primary btn-sm edit-doctor" data-id="${row.id}">Edit</button>`;
                            }
                        }
                    ],
                    pageLength: 10,
                    lengthMenu: [10, 25, 50],
                    order: [[0, 'asc']],
                    language: {
                        search: "",
                        searchPlaceholder: "Search..."
                    },
                    dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rtip'
                });
            })
            .catch(error => {
                console.error("An error occurred: ", error);
                alert("Failed to load clinic details. Please try again.");
            });
    }

    loadClinicData();

    document.getElementById('edit-clinic-btn').addEventListener('click', function() {
        fetch(`/clinics/api/clinics/${clinicId}/`)
            .then(response => response.json())
            .then(data => {
                const form = document.getElementById('edit-clinic-form');
                form.innerHTML = `
                    <div class="form-group">
                        <label for="name">Name</label>
                        <input type="text" class="form-control" id="name" name="name" value="${data.name}" required>
                    </div>
                    <div class="form-group">
                        <label for="address">Address</label>
                        <textarea class="form-control" id="address" name="address" required>${data.address}</textarea>
                    </div>
                    <div class="form-group">
                        <label for="phone_number">Phone Number</label>
                        <input type="tel" class="form-control" id="phone_number" name="phone_number" value="${data.phone_number}" required pattern="[0-9]{10}" title="Please enter a 10-digit phone number">
                    </div>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" class="form-control" id="email" name="email" value="${data.email}" required>
                    </div>
                `;
                $('#editClinicModal').modal('show');
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to load clinic data for editing. Please try again.');
            });
    });

    document.getElementById('save-clinic-btn').addEventListener('click', function() {
        const form = document.getElementById('edit-clinic-form');
        
        if (form.checkValidity() === false) {
            form.reportValidity();
            return;
        }

        const formData = new FormData(form);

        fetch(`/clinics/api/clinics/${clinicId}/update/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                $('#editClinicModal').modal('hide');
                loadClinicData();
            } else {
                alert('Failed to update clinic information. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating clinic information.');
        });
    });

    $('#doctorsTable').on('click', '.edit-doctor', function() {
        const doctorId = $(this).data('id');
        const row = $(this).closest('tr');
        const office_address = row.find('td:eq(1)').text();
        const working_schedule = row.find('td:eq(2)').text();

        // Implement edit doctor functionality here
        // You can create a new modal for editing doctor affiliation or use an inline edit
        console.log(`Edit doctor ${doctorId} affiliation`);
    });

    document.getElementById('add-doctor-btn').addEventListener('click', function() {
        fetch(`/clinics/api/doctors/available/?clinic_id=${clinicId}`)
            .then(response => response.json())
            .then(data => {
                const select = document.getElementById('doctorSelect');
                select.innerHTML = '<option value="">Select a doctor...</option>';
                data.forEach(doctor => {
                    const option = document.createElement('option');
                    option.value = doctor.id;
                    option.textContent = doctor.name;
                    select.appendChild(option);
                });
                $('#addDoctorModal').modal('show');
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to load available doctors. Please try again.');
            });
    });

    document.getElementById('save-add-doctor-btn').addEventListener('click', function() {
        const form = document.getElementById('add-doctor-form');
        
        if (form.checkValidity() === false) {
            form.reportValidity();
            return;
        }

        const formData = new FormData(form);
        formData.append('clinic_id', clinicId);

        fetch('/clinics/api/doctors/add-affiliation/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                $('#addDoctorModal').modal('hide');
                loadClinicData();
            } else {
                alert('Failed to add doctor affiliation. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while adding doctor affiliation.');
        });
    });
});