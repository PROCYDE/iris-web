$(document).ready(function(){
    $('#case_quick_status').change(function(){
        post_request_api('/case/update-status', JSON.stringify({
            'status_id': $('#case_quick_status').val(),
            'csrf_token': $('#csrf_token').val()
        }))
        .done((data) => {
            if (notify_auto_api(data)) {
                window.location.reload();
            }
        })
    });
});

function assign_case_to_me(case_id) {
    // Disable button to prevent multiple clicks
    let btn = $('#assign_to_me_btn');
    if (btn.prop('disabled')) {
        return;
    }
    btn.prop('disabled', true);

    // Fetch current user from server to ensure we have the correct user
    get_request_api('/user/whoami')
    .done((response) => {
        if (response.status === 'success' && response.data && response.data.user_id) {
            const userId = response.data.user_id;
            
            // Call v2 cases update with owner_id
            put_request_api(`/api/v2/cases/${case_id}`, JSON.stringify({ owner_id: userId }))
            .done((data, textStatus) => {
                if (textStatus === 'success') {
                    notify_success('You are now the owner of this case');
                    window.location.reload();
                } else {
                    btn.prop('disabled', false);
                    notify_error('Failed to assign case');
                }
            })
            .fail((jqXHR) => {
                btn.prop('disabled', false);
                if (jqXHR.responseJSON) {
                    notify_error(jqXHR.responseJSON.message || 'Failed to assign case');
                } else {
                    notify_error('Failed to assign case');
                }
            });
        } else {
            btn.prop('disabled', false);
            notify_error('Unable to determine current user');
        }
    })
    .fail(() => {
        btn.prop('disabled', false);
        notify_error('Failed to fetch user information');
    });
}
