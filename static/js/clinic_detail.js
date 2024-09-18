document.addEventListener('DOMContentLoaded', function() {
    const clinicId = window.location.pathname.split('/')[2];
    
    fetch(`/clinics/api/clinics/${clinicId}/`)
        .then(response => response.json())
        .then(data => {
            // Populate clinic info
            document.getElementById('clinic-info').innerHTML = `
                <p><strong>Name:</strong> ${data.name}</p>
                <p><strong>Address:</strong> ${data.address}</p>
                <p><strong>Phone:</strong> ${data.phone_number}</p>
                <p><strong>Email:</strong> ${data.email}</p>
            `;

            // Initialize DataTable for doctors
            $('#doctorsTable').DataTable({
                data: data.doctors,
                columns: [
                    { data: 'name' },
                    { data: 'office_address' },
                    { data: 'schedule' }
                ]
            });
        })
        .catch(error => {
            console.error("An error occurred: ", error);
            alert("Failed to load clinic details. Please try again.");
        });
});