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

document.getElementById('slot-lista').addEventListener('htmx:beforeSwap', evt => {
    console.log('ok');
    if (evt.detail.xhr.status >= 300) {
        evt.detail.shouldSwap = false
        console.log('cancela');
        return
    }
    console.log('close');
    closeDialog('dialog')
})

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
    obj.value = format(obj.value, "(##) #####-####");
}

function cpfMask(obj) {
    obj.value = format(obj.value, "###.###.###-##");
}

function dateMask(obj) {
    obj.value = format(obj.value, "##-##-####");
}

function cepMask(obj) {
    obj.value = format(obj.value, "#####-###");
}

function rgMask(obj) {
    obj.value = format(obj.value, "@##############");
}

function numMask(obj) {
    obj.value = format(obj.value, "###");
}

function format(value, mask) {
    var result = '';

    if (value.length >= mask.length - 1) value = value.substring(0, mask.length)

    if (mask.substring(0, 1) === '#') {
        value = value.replace(/[^\d]+/gi, '')
    }

    value = value.reverse();
    mask = mask.reverse();

    for (var x = 0, y = 0; x <= mask.length && y <= value.length;) {
        if (!(mask.charAt(x) === '#' || mask.charAt(x) === '@')) {
            result += mask.charAt(x);
        }
        else {
            result += value.charAt(y);
            y++;
        }
        x++;
    }
    return result.reverse();
}

function menuToggle() {
    document.querySelector('#menu').classList.toggle('show');
    document.querySelector('.open-icon').classList.toggle('toggle');
    document.querySelector('.close-icon').classList.toggle('toggle');
}

function getTiposSangue() {
    const elm = document.getElementById('tp_sanguineo');

    const tipos = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

    for (const i in tipos) {
        var opt = document.createElement('option');
        opt.value = tipos[i];
        opt.innerHTML = tipos[i];
        elm.appendChild(opt);
    }
}

function getEstados() {
    const elm = document.getElementById('uf');

    const estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF',
        'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB',
        'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR',
        'SC', 'SP', 'SE', 'TO']

    for (const i in estados) {
        var opt = document.createElement('option');
        opt.value = estados[i];
        opt.innerHTML = estados[i];
        elm.appendChild(opt);
    }
}

function selCidades(uf, default_value) {
    if (uf == "") return;

    const url = `https://servicodados.ibge.gov.br/api/v1/localidades/estados/${uf}/municipios`;
    const sel = document.getElementById('cidade');

    sel.innerHTML = "";

    fetch(url,)
        .then(response => response.json())
        .then(data => {
            for (const [_, v] of data.entries()) {
                var opt = document.createElement('option');
                opt.value = v.nome;
                opt.innerHTML = v.nome;
                sel.appendChild(opt);
            }

            if (default_value) {
                defaultOption('cidade', default_value);
            }
        })
        .catch((error) => {
            console.error('Não foi possível obter as cidades: ', error)
        });
}

function getAddress(cep) {
    if (cep == "") return;

    cep = cep.split('-').join('')

    const url = `https://brasilapi.com.br/api/cep/v1/${cep}`

    getEstados()

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const cidade = data.city
            const uf = data.state

            defaultOption('uf', uf);
            selCidades(uf, cidade)

            const endereco = document.getElementById('logradouro');
            endereco.value = `${data.street}, ${data.neighborhood}`;
        })
        .catch((error) => {
            console.error('CEP não localizado: ', error);
        });
}

function defaultOption(id, defaultValue) {
    const select = document.getElementById(id);
    select.value = defaultValue;
}