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
                console.log("Received data:", data); // Log the received data

                document.getElementById('doctor-info').innerHTML = `
                    <p><strong>NPI:</strong> <span id="doctor-npi">${data.npi}</span></p>
                    <p><strong>Name:</strong> <span id="doctor-name">${data.name}</span></p>
                    <p><strong>Email:</strong> <span id="doctor-email">${data.email}</span></p>
                    <p><strong>Phone:</strong> <span id="doctor-phone">${data.phone_number}</span></p>
                    <p><strong>Specialties:</strong> <span id="doctor-specialties">${data.specialties.join(', ')}</span></p>
                `;

                // Check if tables already exist and destroy them if they do
                if ($.fn.DataTable.isDataTable('#clinicsTable')) {
                    $('#clinicsTable').DataTable().destroy();
                }
                if ($.fn.DataTable.isDataTable('#patientsTable')) {
                    $('#patientsTable').DataTable().destroy();
                }

                // Initialize clinics table
                if (data.affiliated_clinics && data.affiliated_clinics.length > 0) {
                    $('#clinicsTable').DataTable({
                        data: data.affiliated_clinics,
                        columns: [
                            { data: 'name' },
                            { data: 'office_address' },
                            { data: 'working_schedule' }
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
                } else {
                    console.log("No clinic data available");
                    $('#clinicsTable').html('<tr><td colspan="3">No affiliated clinics.</td></tr>');
                }

                // Initialize patients table
                if (data.affiliated_patients && data.affiliated_patients.length > 0) {
                    $('#patientsTable').DataTable({
                        data: data.affiliated_patients,
                        columns: [
                            { data: 'name' },
                            { data: 'date_of_birth' },
                            { data: 'last_visit_date' }
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
                } else {
                    console.log("No patient data available");
                    $('#patientsTable').html('<tr><td colspan="3">No affiliated patients.</td></tr>');
                }
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
                const doctorInfo = document.getElementById('doctor-info');
                const specialtiesOptions = data.all_procedures.map(proc => 
                    `<option value="${proc.id}" ${data.specialties.includes(proc.name) ? 'selected' : ''}>${proc.name}</option>`
                ).join('');

                doctorInfo.innerHTML = `
                    <form id="edit-doctor-form">
                        <p><strong>NPI:</strong> <input type="text" name="npi" value="${data.npi}"></p>
                        <p><strong>Name:</strong> <input type="text" name="name" value="${data.name}"></p>
                        <p><strong>Email:</strong> <input type="email" name="email" value="${data.email}"></p>
                        <p><strong>Phone:</strong> <input type="text" name="phone_number" value="${data.phone_number}"></p>
                        <p><strong>Specialties:</strong> 
                            <select name="specialties" id="specialties-select" multiple>
                                ${specialtiesOptions}
                            </select>
                        </p>
                        <button type="submit" class="btn btn-primary">Save</button>
                        <button type="button" id="cancel-edit" class="btn btn-secondary">Cancel</button>
                    </form>
                `;

                // Initialize multiselect dropdown
                MultiselectDropdown({
                    search: true,
                    placeholder: 'Select specialties',
                    txtSelected: 'selected',
                    txtAll: 'All',
                    txtRemove: 'Remove',
                    txtSearch: 'Search specialties',
                });

                document.getElementById('cancel-edit').addEventListener('click', loadDoctorData);
            })
            .catch(error => {
                console.error("Error fetching doctor data for edit:", error);
                alert("Failed to load doctor data for editing. Please try again.");
            });
    });

    document.addEventListener('submit', function(e) {
        if (e.target && e.target.id === 'edit-doctor-form') {
            e.preventDefault();
            const formData = new FormData(e.target);
            
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
                    loadDoctorData();
                } else {
                    alert('Failed to update doctor information. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while updating doctor information.');
            });
        }
    });

    // document.getElementById('edit-doctor-btn').addEventListener('click', function() {
    //     fetch(`/doctors/api/doctors/${doctorId}/`)
    //         .then(response => response.json())
    //         .then(data => {
    //             const doctorInfo = document.getElementById('doctor-info');
    //             const specialtiesOptions = data.all_procedures.map(proc => 
    //                 `<option value="${proc.id}" ${data.specialties.includes(proc.name) ? 'selected' : ''}>${proc.name}</option>`
    //             ).join('');

    //             doctorInfo.innerHTML = `
    //                 <form id="edit-doctor-form">
    //                     <p><strong>NPI:</strong> <input type="text" name="npi" value="${data.npi}"></p>
    //                     <p><strong>Name:</strong> <input type="text" name="name" value="${data.name}"></p>
    //                     <p><strong>Email:</strong> <input type="email" name="email" value="${data.email}"></p>
    //                     <p><strong>Phone:</strong> <input type="text" name="phone_number" value="${data.phone_number}"></p>
    //                     <p><strong>Specialties:</strong> 
    //                         <select name="specialties" multiple>
    //                             ${specialtiesOptions}
    //                         </select>
    //                     </p>
    //                     <button type="submit" class="btn btn-primary">Save</button>
    //                     <button type="button" id="cancel-edit" class="btn btn-secondary">Cancel</button>
    //                 </form>
    //             `;

    //             document.getElementById('cancel-edit').addEventListener('click', loadDoctorData);
    //         })
    //         .catch(error => {
    //             console.error("Error fetching doctor data for edit:", error);
    //             alert("Failed to load doctor data for editing. Please try again.");
    //         });
    // });

    // document.addEventListener('submit', function(e) {
    //     if (e.target && e.target.id === 'edit-doctor-form') {
    //         e.preventDefault();
    //         const formData = new FormData(e.target);
    //         fetch(`/doctors/api/doctors/${doctorId}/update/`, {
    //             method: 'POST',
    //             body: formData,
    //             headers: {
    //                 'X-CSRFToken': csrftoken
    //             }
    //         })
    //         .then(response => response.json())
    //         .then(data => {
    //             if (data.status === 'success') {
    //                 loadDoctorData();
    //             } else {
    //                 alert('Failed to update doctor information. Please try again.');
    //             }
    //         })
    //         .catch(error => {
    //             console.error('Error:', error);
    //             alert('An error occurred while updating doctor information.');
    //         });
    //     }
    // });
});