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
// Display next appointment
                displayNextAppointment(data.next_appointment);
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
                // window.alert(JSON.stringify(data));
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

    //Updates:=========
    // Add New Visit
    document.getElementById('add-visit-btn').addEventListener('click', function() {
        const form = document.getElementById('add-visit-form');
        form.innerHTML = `
            <div class="form-group">
                <label for="visit-date">Date and Time</label>
                <input type="datetime-local" class="form-control" id="visit-date" name="visit-date" required>
            </div>
            <div class="form-group">
                <label for="visit-doctor">Doctor</label>
                <select class="form-control" id="visit-doctor" name="visit-doctor" required>
                    <!-- Options will be populated dynamically -->
                </select>
            </div>
            <div class="form-group">
                <label for="visit-clinic">Clinic</label>
                <select class="form-control" id="visit-clinic" name="visit-clinic" required>
                    <!-- Options will be populated dynamically -->
                </select>
            </div>
            <div class="form-group">
                <label for="visit-procedures">Procedures</label>
                <select multiple class="form-control" id="visit-procedures" name="visit-procedures" required>
                    <!-- Options will be populated dynamically -->
                </select>
            </div>
            <div class="form-group">
                <label for="visit-notes">Doctor's Notes</label>
                <textarea class="form-control" id="visit-notes" name="visit-notes" rows="3"></textarea>
            </div>
        `;
        
        // Populate doctors, clinics, and procedures
        fetchDoctors();
        fetchClinics();
        fetchProceduresForVisit();
        
        $('#addVisitModal').modal('show');
    });

    document.getElementById('save-visit-btn').addEventListener('click', function() {
        const form = document.getElementById('add-visit-form');
        
        if (form.checkValidity() === false) {
            form.reportValidity();
            return;
        }

        const formData = new FormData(form);
        formData.append('patient_id', patientId);

        fetch('/patients/api/visits/add/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                $('#addVisitModal').modal('hide');
                loadPatientData();
            } else {
                alert('Failed to add new visit. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while adding the new visit.');
        });
    });

// Modify the save-appointment-btn event listener
document.getElementById('save-appointment-btn').addEventListener('click', function() {
    const form = document.getElementById('book-appointment-form');
    
    if (form.checkValidity() === false) {
        form.reportValidity();
        return;
    }

    const formData = new FormData(form);
    formData.append('patient_id', patientId);

    // Adjust field names to match backend expectations
    formData.set('doctor_id', formData.get('appointment-doctor'));
    formData.set('clinic_id', formData.get('appointment-clinic'));
    formData.set('procedure_id', formData.get('appointment-procedure'));
    formData.set('date', formData.get('appointment-date'));
    formData.set('time', formData.get('appointment-time'));

    // Remove the original form fields
    formData.delete('appointment-doctor');
    formData.delete('appointment-clinic');
    formData.delete('appointment-procedure');
    formData.delete('appointment-date');
    formData.delete('appointment-time');

    fetch('/appointments/api/book/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            $('#bookAppointmentModal').modal('hide');
            loadPatientData();
        } else {
            alert('Failed to book appointment. ' + (data.message || 'Please try again.'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while booking the appointment.');
    });
});

    // Helper functions for fetching data and updating options
    function fetchDoctors() {
        fetch('/doctors/api/doctors/')
            .then(response => response.json())
            .then(data => {
                const select = document.getElementById('visit-doctor');
                select.innerHTML = data.map(doctor => `<option value="${doctor.id}">${doctor.name}</option>`).join('');
            });
    }

    function fetchClinics() {
        fetch('/clinics/api/clinics/')
            .then(response => response.json())
            .then(data => {
                const select = document.getElementById('visit-clinic');
                select.innerHTML = data.map(clinic => `<option value="${clinic.id}">${clinic.name}</option>`).join('');
            });
    }

   
    function fetchProceduresForVisit() {
        fetch('/procedures/api/procedures/')
            .then(response => response.json())
            .then(data => {
                const visitSelect = document.getElementById('visit-procedures');
                const options = data.map(procedure => `<option value="${procedure.id}">${procedure.name}</option>`).join('');
                visitSelect.innerHTML = options;
            })
            .catch(error => {
                console.error('Error fetching procedures for visit:', error);
            });
    }
    
    function fetchProceduresForAppointment() {
        fetch('/procedures/api/procedures/')
            .then(response => response.json())
            .then(data => {
                // window.alert(JSON.stringify(data));

                const appointmentSelect = document.getElementById('appointment-procedure');
                const options = data.map(procedure => `<option value="${procedure.id}">${procedure.name}</option>`).join('');
                appointmentSelect.innerHTML = '<option value="">Select a procedure</option>' + options;
            })
            .catch(error => {
                console.error('Error fetching procedures for appointment:', error);
            });
    }

    function updateClinicOptions() {
        const procedureId = document.getElementById('appointment-procedure').value;
        fetch(`/clinics/api/clinics/by-procedure/${procedureId}/`)
            .then(response => response.json())
            .then(data => {
                // window.alert(JSON.stringify(data));

                const clinic_select = document.getElementById('appointment-clinic');
                const options = data.map(clinic => `<option value="${clinic.id}">${clinic.name}</option>`).join('');
                clinic_select.innerHTML = '<option value="">Select a Clinic</option>' + options;
                updateDoctorOptions();
            });
    }
    function updateDoctorOptions() {
        const procedureId = document.getElementById('appointment-procedure').value;
        const clinicId = document.getElementById('appointment-clinic').value;
        
        // Check if both procedureId and clinicId are valid
        if (!procedureId || !clinicId) {
            console.error('Procedure ID or Clinic ID is missing');
            return;
        }
    
        fetch(`/doctors/api/doctors/by-procedure-and-clinic/${procedureId}/${clinicId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                const select = document.getElementById('appointment-doctor');
                let options;
                if (data.length > 0) {
                    options = data.map(doctor => `<option value="${doctor.id}">${doctor.name}</option>`).join('');
                } else {
                    options = '<option value="">No doctors available</option>';
                }
                select.innerHTML = '<option value="">Select a Doctor</option>' + options;
                // updateAvailableTimeSlots();
            })
            .catch(error => {
                console.error('Error updating doctor options:', error);
                const select = document.getElementById('appointment-doctor');
                select.innerHTML = '<option value="">Error loading doctors</option>';
            });
    }
   
    // Function to display the next appointment
    function displayNextAppointment(appointment) {
        const nextAppointmentDiv = document.getElementById('next-appointment');
        if (appointment) {
            nextAppointmentDiv.innerHTML = `
                <p><strong>Date and Time:</strong> ${appointment.date_time}</p>
                <p><strong>Doctor:</strong> ${appointment.doctor_name}</p>
                <p><strong>Clinic:</strong> ${appointment.clinic_name}</p>
                <p><strong>Procedure:</strong> ${appointment.procedure_name}</p>
            `;
        } else {
            nextAppointmentDiv.innerHTML = '<p>No upcoming appointments scheduled.</p>';
        }
    }

    // =====================
// Modify the book-appointment-btn event listener
document.getElementById('book-appointment-btn').addEventListener('click', function() {
    const form = document.getElementById('book-appointment-form');
    form.innerHTML = `
        <div class="form-group">
            <label for="appointment-procedure">Procedure</label>
            <select class="form-control" id="appointment-procedure" name="appointment-procedure" required>
                <!-- Options will be populated dynamically -->
            </select>
        </div>
        <div class="form-group">
            <label for="appointment-clinic">Clinic</label>
            <select class="form-control" id="appointment-clinic" name="appointment-clinic" required>
                <!-- Options will be populated dynamically -->
            </select>
        </div>
        <div class="form-group">
            <label for="appointment-doctor">Doctor</label>
            <select class="form-control" id="appointment-doctor" name="appointment-doctor" required>
                <!-- Options will be populated dynamically -->
            </select>
        </div>
        <div class="form-group">
            <label for="appointment-date">Date</label>
            <input type="date" class="form-control" id="appointment-date" name="appointment-date" required>
        </div>
        <div class="form-group">
            <label for="appointment-time">Time</label>
            <select class="form-control" id="appointment-time" name="appointment-time" required>
                <option value="">Select a time</option>
                <!-- Options will be populated dynamically -->
            </select>
        </div>
    `;
    
    // Populate procedures
    fetchProceduresForAppointment();
    
    // Add event listeners for real-time validation
    document.getElementById('appointment-procedure').addEventListener('change', updateClinicOptions);
    document.getElementById('appointment-clinic').addEventListener('change', updateDoctorOptions);
    document.getElementById('appointment-doctor').addEventListener('change', enableDateSelection);
    document.getElementById('appointment-date').addEventListener('change', updateTimeSlots);
    
    $('#bookAppointmentModal').modal('show');
});

// Add new function to enable date selection
function enableDateSelection() {
    const dateInput = document.getElementById('appointment-date');
    dateInput.disabled = false;
    
    // Set min date to today and max date to 3 months from now
    const today = new Date().toISOString().split('T')[0];
    const threeMonthsLater = new Date();
    threeMonthsLater.setMonth(threeMonthsLater.getMonth() + 3);
    dateInput.min = today;
    dateInput.max = threeMonthsLater.toISOString().split('T')[0];
}

// Add new function to update time slots
function updateTimeSlots() {
    const doctorId = document.getElementById('appointment-doctor').value;
    const clinicId = document.getElementById('appointment-clinic').value;
    const date = document.getElementById('appointment-date').value;
    const timeSelect = document.getElementById('appointment-time');

    if (!doctorId || !clinicId || !date) {
        console.log('Doctor, clinic, or date not selected');
        return;
    }

    // Generate all time slots from 9 AM to 6 PM
    const allTimeSlots = [];
    for (let hour = 9; hour < 18; hour++) {
        allTimeSlots.push(`${hour.toString().padStart(2, '0')}:00`);
    }

    // Fetch available time slots from the server
    fetch(`/appointments/api/available-time-slots/?doctor_id=${doctorId}&clinic_id=${clinicId}&date=${date}`)
        .then(response => response.json())
        .then(data => {
            // Clear existing options
            timeSelect.innerHTML = '<option value="">Select a time</option>';
            
            // Add new options
            allTimeSlots.forEach(slot => {
                const option = document.createElement('option');
                option.value = slot;
                option.textContent = slot;
                if (!data.includes(slot)) {
                    option.disabled = true;
                }
                timeSelect.appendChild(option);
            });

            timeSelect.disabled = false;
        })
        .catch(error => {
            console.error('Error fetching time slots:', error);
            timeSelect.innerHTML = '<option value="">Error loading time slots</option>';
            timeSelect.disabled = true;
        });
}



});