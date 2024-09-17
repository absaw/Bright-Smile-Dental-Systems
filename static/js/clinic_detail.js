document.addEventListener('DOMContentLoaded', function() {
    const clinicId = window.location.pathname.split('/')[2];
    fetch(`/clinics/api/clinics/${clinicId}/`)
        .then(response => response.json())
        .then(clinic => {
            const clinicDetail = document.getElementById('clinic-detail');
            clinicDetail.innerHTML = `
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">${clinic.name}</h5>
                        <p class="card-text">
                            Address: ${clinic.address}<br>
                            Phone: ${clinic.phone_number}<br>
                            Email: ${clinic.email}
                        </p>
                        <button class="btn btn-primary" onclick="editClinic()">Edit</button>
                    </div>
                </div>
                <h3>Affiliated Doctors</h3>
                <div id="doctors-list"></div>
            `;

            const doctorsList = document.getElementById('doctors-list');
            clinic.doctors.forEach(doctor => {
                const doctorElement = document.createElement('div');
                doctorElement.className = 'card mb-3';
                doctorElement.innerHTML = `
                    <div class="card-body">
                        <h5 class="card-title">${doctor.name}</h5>
                        <p class="card-text">
                            Office Address: ${doctor.office_address}<br>
                            Schedule: ${doctor.schedule}
                        </p>
                    </div>
                `;
                doctorsList.appendChild(doctorElement);
            });
        });
});

function editClinic() {
    // Implement edit functionality here
    console.log('Edit clinic');
}