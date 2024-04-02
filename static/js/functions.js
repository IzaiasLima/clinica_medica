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

document.addEventListener('htmx:beforeSwap', evt => {
    if (evt.detail.xhr.status >= 300) {
        evt.detail.shouldSwap = false
        return
    }
    closeDialog('dialog')
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
    const mask = "(##) #####-####";
    obj.value = format(obj.value, mask);
}

function cpfMask(obj) {
    const mask = "###.###.###-##";
    obj.value = format(obj.value, mask);
}

function dateMask(obj) {
    const mask = "##-##-####";
    obj.value = format(obj.value, mask);
}

function cepMask(obj) {
    const mask = "#####-###";
    obj.value = format(obj.value, mask);
}

function format(value, mask) {
    var result = "";

    if (value.length >= mask.length - 1) value = value.substring(0, mask.length)
    value = value.replace(/[^\d]+/gi, '').reverse();

    var mask = mask.reverse();

    for (var x = 0, y = 0; x <= mask.length && y <= value.length;) {
        if (mask.charAt(x) != '#')
            result += mask.charAt(x);
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

function getEstados() {
    const elm = document.getElementById('uf');

    estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF',
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

function selCidades(uf, id_sel_cidade, default_value) {
    if (uf == "") return;

    const url = `https://servicodados.ibge.gov.br/api/v1/localidades/estados/${uf}/municipios`;
    const sel = document.getElementById('cidade');

    sel.innerHTML = "";

    fetch(url)
        .then(response => response.json())
        .then(data => {
            for (const [k, v] of data.entries()) {
                var opt = document.createElement('option');
                opt.value = v.nome;
                opt.innerHTML = v['nome'];
                sel.appendChild(opt);
            }

            if (id_sel_cidade && default_value) {
                defaultOption(id_sel_cidade, default_value);
            }
        })
        .catch((error) => {
            console.error('Não foi possível obter as cidades: ', error)
        });
}

function getAddress(cep) {
    if (cep == "") return;

    const url = `https://brasilapi.com.br/api/cep/v1/${cep}`
    getEstados()

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const cidade = data['city']
            const uf = data['state']

            selCidades(uf, 'cidade', cidade)
            defaultOption('uf', uf);

            const endereco = document.getElementById('logradouro');
            endereco.value = `${data['street']}, ${data['neighborhood']}`;
        })
        .catch((error) => {
            console.error('CEP não localizado: ', error);
        });
}
