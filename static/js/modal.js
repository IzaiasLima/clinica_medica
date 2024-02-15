document.addEventListener(
    "htmx:confirm",
    function (e) {
        if (e.detail.question !== null) {
            e.preventDefault();
            Swal.fire({
                // animation: false,
                buttonsStyling: false,
                showCancelButton: true,
                reverseButtons: true,
                // icon: 'question',
                title: 'Favor confirmar!',
                text: `Deseja mesmo excluir o cadastro de ${(e.detail.question).toUpperCase()}?`,
                showClass: { popup: 'animate__animated animate__fadeInUp animate__faster' },
                hideClass: { popup: 'animate__animated animate__fadeOutDown animate__faster' },
            }).then(function (res) {
                if (res.isConfirmed) e.detail.issueRequest(true)
            })
        }
    }
);

