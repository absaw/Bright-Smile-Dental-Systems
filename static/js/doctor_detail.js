document.addEventListener('DOMContentLoaded', function() {
    const doctorId = window.location.pathname.split('/')[2];
    
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

    function loadDoctorData() {
        fetch(`/doctors/api/doctors/${doctorId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                const doctorInfoTable = document.querySelector('#doctor-info table tbody');
                doctorInfoTable.innerHTML = `
                    <tr><th>NPI:</th><td>${data.npi}</td></tr>
                    <tr><th>Name:</th><td>${data.name}</td></tr>
                    <tr><th>Email:</th><td>${data.email}</td></tr>
                    <tr><th>Phone:</th><td>${data.phone_number}</td></tr>
                    <tr><th>Specialties:</th><td>${data.specialties.join(', ')}</td></tr>
                `;

                // Initialize clinics table
                if ($.fn.DataTable.isDataTable('#clinicsTable')) {
                    $('#clinicsTable').DataTable().destroy();
                }
                $('#clinicsTable').DataTable({
                    data: data.affiliated_clinics,
                    columns: [
                        { data: 'name' },
                        { data: 'office_address' },
                        { data: 'working_schedule' }
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

                // Initialize patients table
                if ($.fn.DataTable.isDataTable('#patientsTable')) {
                    $('#patientsTable').DataTable().destroy();
                }
                $('#patientsTable').DataTable({
                    data: data.affiliated_patients,
                    columns: [
                        { data: 'name' },
                        { data: 'date_of_birth' },
                        { data: 'last_visit_date' }
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
                alert("Failed to load doctor details. Please try again.");
            });
    }

    loadDoctorData();

    document.getElementById('edit-doctor-btn').addEventListener('click', function() {
        fetch(`/doctors/api/doctors/${doctorId}/`)
            .then(response => response.json())
            .then(data => {
                const form = document.getElementById('edit-doctor-form');
                const specialtiesOptions = data.all_procedures.map(proc => 
                    `<option value="${proc.id}" ${data.specialties.includes(proc.name) ? 'selected' : ''}>${proc.name}</option>`
                ).join('');

                form.innerHTML = `
                    <div class="form-group">
                        <label for="npi">NPI</label>
                        <input type="text" class="form-control" id="npi" name="npi" value="${data.npi}" required pattern="[0-9]{10}" title="NPI must be a 10-digit number">
                    </div>
                    <div class="form-group">
                        <label for="name">Name</label>
                        <input type="text" class="form-control" id="name" name="name" value="${data.name}" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" class="form-control" id="email" name="email" value="${data.email}" required>
                    </div>
                    <div class="form-group">
                        <label for="phone_number">Phone Number</label>
                        <input type="tel" class="form-control" id="phone_number" name="phone_number" value="${data.phone_number}" required pattern="[0-9]{10}" title="Please enter a 10-digit phone number">
                    </div>
                    <div class="form-group">
                        <label for="specialties">Specialties</label>
                        <select class="form-control" id="specialties" name="specialties" multiple required size="5">
                            ${specialtiesOptions}
                        </select>
                        <small class="form-text text-muted">Hold Ctrl (Windows) or Command (Mac) to select multiple specialties.</small>
                    </div>
                `;

                $('#editDoctorModal').modal('show');
            })
            .catch(error => {
                console.error("Error fetching doctor data for edit:", error);
                alert("Failed to load doctor data for editing. Please try again.");
            });
    });

    document.getElementById('save-doctor-btn').addEventListener('click', function() {
        const form = document.getElementById('edit-doctor-form');
        
        if (form.checkValidity() === false) {
            form.reportValidity();
            return;
        }

        const formData = new FormData(form);
        
        // Handle multiple selected specialties
        const specialties = Array.from(form.specialties.selectedOptions).map(option => option.value);
        formData.delete('specialties');
        specialties.forEach(specialty => {
            formData.append('specialties', specialty);
        });

        fetch(`/doctors/api/doctors/${doctorId}/update/`, {
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
                loadDoctorData();
            } else {
                alert('Failed to update doctor information. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating doctor information.');
        });
    });
});