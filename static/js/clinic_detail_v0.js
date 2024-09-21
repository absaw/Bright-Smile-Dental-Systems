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
                document.getElementById('clinic-info').innerHTML = `
                    <p><strong>Name:</strong> <span id="clinic-name">${data.name}</span></p>
                    <p><strong>Address:</strong> <span id="clinic-address">${data.address}</span></p>
                    <p><strong>Phone:</strong> <span id="clinic-phone">${data.phone_number}</span></p>
                    <p><strong>Email:</strong> <span id="clinic-email">${data.email}</span></p>
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
                console.error("An error occurred: ", error);
                alert("Failed to load clinic details. Please try again.");
            });
    }

    loadClinicData();

    document.getElementById('edit-clinic-btn').addEventListener('click', function() {
        const clinicInfo = document.getElementById('clinic-info');
        const name = document.getElementById('clinic-name').textContent;
        const address = document.getElementById('clinic-address').textContent;
        const phone = document.getElementById('clinic-phone').textContent;
        const email = document.getElementById('clinic-email').textContent;

        clinicInfo.innerHTML = `
            <form id="edit-clinic-form">
                <p><strong>Name:</strong> <input type="text" name="name" value="${name}"></p>
                <p><strong>Address:</strong> <input type="text" name="address" value="${address}"></p>
                <p><strong>Phone:</strong> <input type="text" name="phone_number" value="${phone}"></p>
                <p><strong>Email:</strong> <input type="email" name="email" value="${email}"></p>
                <button type="submit" class="btn btn-primary">Save</button>
                <button type="button" id="cancel-edit" class="btn btn-secondary">Cancel</button>
            </form>
        `;

        document.getElementById('cancel-edit').addEventListener('click', loadClinicData);
    });

    document.addEventListener('submit', function(e) {
        if (e.target && e.target.id === 'edit-clinic-form') {
            e.preventDefault();
            const formData = new FormData(e.target);
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
                    loadClinicData();
                } else {
                    alert('Failed to update clinic information. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while updating clinic information.');
            });
        }
    });

    $('#doctorsTable').on('click', '.edit-doctor', function() {
        const doctorId = $(this).data('id');
        const row = $(this).closest('tr');
        const office_address = row.find('td:eq(1)').text();
        const working_schedule = row.find('td:eq(2)').text();

        $('#editDoctorId').val(doctorId);
        $('#editDoctorOfficeAddress').val(office_address);
        $('#editDoctorSchedule').val(working_schedule);

        $('#editDoctorModal').modal('show');
    });

    $('#saveEditDoctorBtn').click(function() {
        const formData = new FormData($('#editDoctorForm')[0]);
        formData.append('clinic_id', clinicId);

        fetch(`/clinics/api/doctors/${$('#editDoctorId').val()}/update-affiliation/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                $('#editDoctorModal').modal('hide');
                loadClinicData();
            } else {
                alert('Failed to update doctor information. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating doctor information.');
        });
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

    $('#saveAddDoctorBtn').click(function() {
        const formData = new FormData($('#addDoctorForm')[0]);
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