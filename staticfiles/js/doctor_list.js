document.addEventListener('DOMContentLoaded', function() {
    let table;

    function loadDoctors() {
        fetch('/doctors/api/doctors/')
            .then(response => response.json())
            .then(data => {
                if ($.fn.DataTable.isDataTable('#doctorsTable')) {
                    $('#doctorsTable').DataTable().destroy();
                }
                table = $('#doctorsTable').DataTable({
                    data: data,
                    columns: [
                        { data: 'npi' },
                        { data: 'name' },
                        { data: 'specialties', render: data => data.join(', ') },
                        { data: 'affiliated_clinics' },
                        { data: 'affiliated_patients' },
                        {
                            data: null,
                            render: function(data, type, row) {
                                return `<a href="/doctors/${row.id}/" class="btn btn-primary btn-sm">View/Edit</a>`;
                            }
                        }
                    ],
                    pageLength: 25,
                    lengthMenu: [25, 50, 100],
                    order: [[1, 'asc']],
                    language: {
                        search: "",
                        searchPlaceholder: "Search..."
                    },
                    dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rtip'
                });
            })
            .catch(error => {
                console.error("An error occurred: ", error);
                alert("Failed to load doctors. Please try again.");
            });
    }

    function loadSpecialties() {
        fetch('/procedures/api/procedures/')
            .then(response => response.json())
            .then(data => {
                const specialtiesSelect = document.getElementById('specialties');
                specialtiesSelect.innerHTML = ''; // Clear existing options
                data.forEach(specialty => {
                    const option = document.createElement('option');
                    option.value = specialty.id;
                    option.textContent = specialty.name;
                    specialtiesSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error("An error occurred while loading specialties: ", error);
            });
    }

    document.getElementById('addDoctorBtn').addEventListener('click', function() {
        $('#addDoctorModal').modal('show');
    });

    document.getElementById('submitAddDoctor').addEventListener('click', function() {
        const form = document.getElementById('addDoctorForm');
        
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

        fetch('/doctors/api/add_doctor/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                $('#addDoctorModal').modal('hide');
                loadDoctors(); // Reload the entire table
                alert('Doctor added successfully!');
                form.reset();
            } else {
                alert('Failed to add doctor. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while adding the doctor.');
        });
    });

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

    loadDoctors();
    loadSpecialties();
});