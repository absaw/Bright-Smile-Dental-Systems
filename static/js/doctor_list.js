document.addEventListener('DOMContentLoaded', function() {
    function loadDoctors() {
        fetch('/doctors/api/doctors/')
            .then(response => response.json())
            .then(data => {
                const table = $('#doctorsTable').DataTable({
                    data: data,
                    columns: [
                        { data: 'npi' },
                        { data: 'name' },
                        { data: 'specialties' },
                        { data: 'affiliated_clinics' },
                        { data: 'affiliated_patients' },
                        {
                            data: null,
                            render: function(data, type, row) {
                                return `<a href="/doctors/${row.id}/" class="btn btn-primary btn-sm">View</a>`;
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
                    // dom: '<"row"<"col-sm-6 search-bar"f><"col-sm-6">>rt<"row"<"col-sm-6"i><"col-sm-6 entries-selector"l>>p',
                    // dom: '<"row"<"col-sm-6"f><"col-sm-6">>rt<"row"<"col-sm-6"i><"col-sm-6"l>>p',
                    // dom: 'f<"row"<"col-sm-12"tr>>i<"row"<"col-sm-12"l>>p'
                    // dom: 'f<"row"<"col-sm-12"tr>><"row"<"col-sm-12"l>i>p'
                    dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rtip'
                });
            })
            .catch(error => {
                console.error("An error occurred: ", error);
                alert("Failed to load doctors. Please try again.");
            });
    }

    loadDoctors();
});