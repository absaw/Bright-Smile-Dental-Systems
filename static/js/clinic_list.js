document.addEventListener('DOMContentLoaded', function() {
    fetch('/clinics/api/clinics/')
        .then(response => response.json())
        .then(clinics => {
            const clinicsList = document.getElementById('clinics-list');
            clinics.forEach(clinic => {
                const clinicElement = document.createElement('div');
                clinicElement.className = 'card mb-4';
                clinicElement.innerHTML = `
                    <div class="card-body">
                        <h5 class="card-title">${clinic.name}</h5>
                        <p class="card-text">
                            Phone: ${clinic.phone_number}<br>
                            Location: ${clinic.city}, ${clinic.state}<br>
                            Doctors: ${clinic.doctor_count}<br>
                            Patients: ${clinic.patient_count}<br>
                            id: ${clinic.id}
                        </p>
                        <a href="/clinics/${clinic.id}/" class="btn btn-primary">View Details</a>
                    </div>
                `;
                clinicsList.appendChild(clinicElement);
            });
        });
});