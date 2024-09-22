document.addEventListener('DOMContentLoaded', function() {
    const patientId = window.location.pathname.split('/')[2];
    
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

    function loadPatientData() {
        fetch(`/patients/api/patients/${patientId}/`)
            .then(response => response.json())
            .then(data => {
                // window.alert(JSON.stringify(data));
                const patientInfoTable = document.querySelector('#patient-info table tbody');
                patientInfoTable.innerHTML = `
                    <tr><th>Name:</th><td>${data.name}</td></tr>
                    <tr><th>Address:</th><td>${data.address}</td></tr>
                    <tr><th>Phone Number:</th><td>${data.phone_number}</td></tr>
                    <tr><th>Date of Birth:</th><td>${data.date_of_birth}</td></tr>
                    <tr><th>SSN (last 4 digits):</th><td>${data.ssn_last_4}</td></tr>
                    <tr><th>Gender:</th><td>${data.gender === 'M' ? 'Male' : data.gender === 'F' ? 'Female' : 'Other'}</td></tr>
                `;

                // Initialize visits table
                if ($.fn.DataTable.isDataTable('#visitsTable')) {
                    $('#visitsTable').DataTable().destroy();
                }
    
                $('#visitsTable').DataTable({
                    data: data.visits,
                    columns: [
                        { data: 'date_time' },
                        { data: 'doctor_name' },
                        { data: 'clinic_name' },
                        { data: 'procedures' },
                        { data: 'doctor_notes' }
                    ],
                    pageLength: 10,
                    lengthMenu: [10, 25, 50],
                    order: [[0, 'desc']],
                    language: {
                        search: "",
                        searchPlaceholder: "Search..."
                    },
                    dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rtip'
                });
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to load patient details. Please try again.');
            });
    }

    loadPatientData();

    document.getElementById('edit-patient-btn').addEventListener('click', function() {
        fetch(`/patients/api/patients/${patientId}/`)
            .then(response => response.json())
            .then(data => {
                const form = document.getElementById('edit-patient-form');
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
                        <label for="date_of_birth">Date of Birth</label>
                        <input type="date" class="form-control" id="date_of_birth" name="date_of_birth" value="${data.date_of_birth}" required max="${new Date().toISOString().split('T')[0]}">
                    </div>
                    <div class="form-group">
                        <label for="ssn_last_4">SSN (last 4 digits)</label>
                        <input type="text" class="form-control" id="ssn_last_4" name="ssn_last_4" value="${data.ssn_last_4}" required pattern="[0-9]{4}" maxlength="4" title="Please enter the last 4 digits of the SSN">
                    </div>
                    <div class="form-group">
                        <label for="gender">Gender</label>
                        <select class="form-control" id="gender" name="gender" required>
                            <option value="M" ${data.gender === 'M' ? 'selected' : ''}>Male</option>
                            <option value="F" ${data.gender === 'F' ? 'selected' : ''}>Female</option>
                            <option value="O" ${data.gender === 'O' ? 'selected' : ''}>Other</option>
                        </select>
                    </div>
                `;
                $('#editPatientModal').modal('show');
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to load patient data for editing. Please try again.');
            });
    });

    document.getElementById('save-patient-btn').addEventListener('click', function() {
        const form = document.getElementById('edit-patient-form');
        
        if (form.checkValidity() === false) {
            form.reportValidity();
            return;
        }

        const formData = new FormData(form);

        fetch(`/patients/api/patients/${patientId}/update/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                $('#editPatientModal').modal('hide');
                loadPatientData();
            } else {
                alert('Failed to update patient information. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating patient information.');
        });
    });
});