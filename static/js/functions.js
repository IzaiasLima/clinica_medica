
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

function showToast(msg) {
    const toast = document.getElementById('toast');
    toast.innerHTML = msg;
    toast.classList.add('show', 'animate__fadeInUp');
    setTimeout(function () { toast.classList.remove('show', 'animate__fadeInUp') }, 3000);
}

function showDetail() {
    const detalhe = document.getElementById('detalhe');
    const info = document.getElementById('info');
    detalhe.classList.add('show');
    info.classList.add('show', 'animate__fadeInUp');
}

function hideDetail() {
    const detalhe = document.getElementById('detalhe');
    const info = document.getElementById('info');
    detalhe.classList.remove('show');
    info.classList.remove('show', 'animate__fadeInUp');
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

function phoneMask(value) {
    mask = "(##) #####-####";
    format(value, mask);
}

function format(value, mask) {
    var vlr = value.value
    var resultado = "";

    if (vlr.length >= mask.length - 1) vlr = vlr.substring(0, mask.length)
    vlr = vlr.replace(/[^\d]+/gi, '').reverse();

    var mask = mask.reverse();

    for (var x = 0, y = 0; x <= mask.length && y <= vlr.length;) {
        if (mask.charAt(x) != '#')
            resultado += mask.charAt(x);
        else {
            resultado += vlr.charAt(y);
            y++;
        }
        x++;
    }

    value.value = resultado.reverse();
}