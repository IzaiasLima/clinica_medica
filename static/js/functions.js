document.addEventListener(
    "htmx:confirm",
    function (evt) {
        if (evt.detail.question !== null) {
            evt.preventDefault();
            Swal.fire({
                // animation: false,
                buttonsStyling: false,
                showCancelButton: true,
                reverseButtons: true,
                // icon: 'question',
                title: 'Favor confirmar!',
                text: `Deseja mesmo excluir o cadastro de ${(evt.detail.question).toUpperCase()}?`,
                showClass: { popup: 'animate__animated animate__fadeInUp animate__faster' },
                hideClass: { popup: 'animate__animated animate__zoomOut animate__faster' },
            }).then(function (res) {
                if (res.isConfirmed) evt.detail.issueRequest(true)
            })
        }
    }
);

document.addEventListener('htmx:responseError', evt => {
    const error = JSON.parse(evt.detail.xhr.responseText);
    showToast(error.detail);
})

function defaultOption(id, defaultValue) {
    let select = document.getElementById(id);
    select.value = defaultValue;
}

function showToast(msg) {
    const toast = document.getElementById('toast');
    toast.innerHTML = msg;
    toast.classList.add('show', 'animate__fadeInUp');
    setTimeout(function () { toast.classList.remove('show', 'animate__fadeInUp') }, 3000);
}

function showDialog(id) {
    const dialog = document.getElementById(id);
    const info = document.querySelector('.info');
    dialog.classList.add('show');
    info.classList.add('animate__fadeInUp');
}

function closeDialog(id) {
    const dialog = document.getElementById(id);
    const info = document.querySelector('.info');
    dialog.classList.remove('show');
    info.classList.remove('animate__fadeInUp');
}

function allowsEditing(obj) {
    let editing = document.querySelector('.editing');

    if (editing) {
        htmx.trigger(editing, 'cancel')
    } else {
        htmx.trigger(obj, 'edit')

    }
}

String.prototype.reverse = function () {
    return this.split('').reverse().join('');
};

function phoneMask(obj) {
    mask = "(##) #####-####";
    var fmt = format(obj.value, mask);
    obj.value = fmt
}

function cpfMask(obj) {
    mask = "###.###.###-##";
    var fmt = format(obj.value, mask);
    obj.value = fmt
}

function format(value, mask) {
    var resultado = "";

    if (value.length >= mask.length - 1) value = value.substring(0, mask.length)
    value = value.replace(/[^\d]+/gi, '').reverse();

    var mask = mask.reverse();

    for (var x = 0, y = 0; x <= mask.length && y <= value.length;) {
        if (mask.charAt(x) != '#')
            resultado += mask.charAt(x);
        else {
            resultado += value.charAt(y);
            y++;
        }
        x++;
    }
    return resultado.reverse();
}