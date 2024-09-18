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
                // Populate clinic info
                document.getElementById('clinic-info').innerHTML = `
                    <p><strong>Name:</strong> <span id="clinic-name">${data.name}</span></p>
                    <p><strong>Address:</strong> <span id="clinic-address">${data.address}</span></p>
                    <p><strong>Phone:</strong> <span id="clinic-phone">${data.phone_number}</span></p>
                    <p><strong>Email:</strong> <span id="clinic-email">${data.email}</span></p>
                `;

                // Populate procedures
                // const proceduresList = document.getElementById('procedures-list');
                // proceduresList.innerHTML = data.procedures.map(proc => `<li>${proc.name}</li>`).join('');

                // Initialize DataTable for doctors
                if ($.fn.DataTable.isDataTable('#doctorsTable')) {
                    $('#doctorsTable').DataTable().destroy();
                }
                $('#doctorsTable').DataTable({
                    data: data.doctors,
                    columns: [
                        { data: 'name' },
                        { data: 'office_address' },
                        { data: 'schedule' },
                        { data: 'procedures' }
                    ]
                });
            })
            .catch(error => {
                console.error("An error occurred: ", error);
                alert("Failed to load clinic details. Please try again.");
            });
    }

    loadClinicData();

    // Edit clinic info
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

    // Use event delegation for the dynamically created form
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
});