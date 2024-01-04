function send_form() {
    let username_elem = document.getElementById('id_username');
    let error_username_elem = document.getElementById('username__error');
    let password_elem = document.getElementById('id_password');
    let error_password_elem = document.getElementById('password__error');
    if (username_elem.value == '') {
        error_username_elem.style.display = 'flex';
        username_elem.style.borderColor = '#D93025';
    } else {
        error_username_elem.style.display = 'none';
    }

    if (password_elem.value == '') {
        error_password_elem.style.display = 'flex';
        password_elem.style.borderColor = '#D93025';
    } else {
        error_username_elem.style.display = 'none';
    }

    if (username_elem.value != '' && password_elem.value != '') {
        let form = document.getElementById('from');
        form.submit();
    }
}