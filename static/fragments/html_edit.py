def paciente_html(dados):
    html = f"""
        <tr trigger="cancel" class="editing">
            <td><input name="nome" value="{dados['nome']}"></td>
            <td><input name="email" value="{dados['email']}"></td>
            <td><input name="telefone" onkeyup="phoneMask(this)" value="{dados['telefone']}"></td>
            <td>
                <select name="status">
                    <option value="" selected disabled hidden>Selecione</option>
                    <option value="aguardando">Aguardando</option>
                    <option value="em atendimento">Em atendimento</option>
                    <option value="atendido">Atendido</option>
                    <option value="internado">Internado</option>
                    <option value="liberado">Liberado</option>
                </select>
            </td>
            <td class="icon">
                <div>
                    <a hx-get="/api/pacientes"
                        title="Cancelar a alteração"
                        hx-swap="outerHTML" 
                        hx-target="closest table">
                        <i class="material-symbols-outlined small-icon">undo</i>
                    </a>
                    <a hx-trigger="click" 
                        hx-include="closest tr"
                        hx-put="/api/pacientes/{dados['id']}" 
                        title="Salvar"
                        hx-swap="outerHTML" 
                        hx-target="closest table"
                        <i class="material-symbols-outlined small-icon">save</i>
                    </a>
                </div>
            </td>
        </tr>
        """
    return html


def medico_html(dados):
    html = f"""
        <tr trigger="cancel" class="editing">
            <td><input name="nome" value="{dados['nome']}"></td>
            <td><input name="crm" value="{dados['crm']}"></td>
            <td><input name="email" value="{dados['email']}"></td>
            <td><input name="especialidade" value="{dados['especialidade']}"></td>
            <td>
                <select name="turno">
                    <option value="" selected disabled hidden>Selecione</option>
                    <option value="diurno">Diurno</option>
                    <option value="noturno">Noturno</option>
                    <option value="vespertino">Vespertino</option>
                </select>
            </td>
            <td>
                <select name="status">
                    <option value="" selected disabled hidden>Selecione</option>
                    <option value="em atendimento">Em atendimento</option>
                    <option value="de plantão">De plantão</option>
                    <option value="indisponível">Indisponível</option>
                </select>
            </td>

            <td class="icon">
                <div>
                    <a hx-get="/api/medicos"
                        title="Cancelar a alteração"
                        hx-swap="outerHTML" 
                        hx-target="closest table">
                        <i class="material-symbols-outlined small-icon">undo</i>
                    </a>
                    <a hx-trigger="click" 
                        hx-include="closest tr"
                        hx-put="/api/medicos/{dados['id']}" 
                        title="Salvar"
                        hx-target="closest table"
                        hx-swap="outerHTML">
                        <i class="material-symbols-outlined small-icon">save</i>
                    </a>
                </div>
            </td>
        </tr>

        """
    return html
