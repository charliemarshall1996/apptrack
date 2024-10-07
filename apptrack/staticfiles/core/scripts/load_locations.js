$(document).ready(function() {
    // Listen for changes in the country dropdown
    $('#id_country').change(function() {
        var country_code = $(this).val();
        if (country_code) {
            $.ajax({
                url: '/get-subdivisions/' + country_code + '/',
                type: 'GET',
                success: function(data) {
                    $('#id_region').empty();
                    $('#id_region').append('<option value="">Select a region</option>');
                    data.regions.forEach(function(region) {
                        $('#id_region').append('<option value="' + region.code + '">' + region.name + '</option>');
                    });
                },
                error: function() {
                    console.error("Failed to fetch subdivisions.");
                }
            });
        } else {
            $('#id_region').empty();
            $('#id_region').append('<option value="">Select a region</option>');
        }
    });
});
