def paciente_html():
    html = f"""
        <tr trigger="cancel" class="editing">
            <td><input placeholder="Nome do paciente" name="nome" value=""></td>
            <td><input placeholder="E-mail do paciente" name="email" value=""></td>
            <td><input placeholder="Telefone do paciente" name="telefone" value=""></td>
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
                        hx-post="/api/pacientes" 
                        title="Salvar"
                        hx-swap="outerHTML" 
                        hx-target="closest table">
                        <i class="material-symbols-outlined small-icon">save</i>
                    </a>
                </div>
            </td>
        </tr>
        """
    return html


def medico_html():
    html = f"""
        <tr trigger="cancel" class="editing">
            <td><input placeholder="Nome do médico" name="nome" value=""></td>
            <td><input placeholder="CRM do médico" name="crm" value=""></td>
            <td><input placeholder="E-mail do médico" name="email" value=""></td>
            <td><input placeholder="Especialidade" name="especialidade" value=""></td>
            <td>
                <select name="turno">
                    <option value="" selected disabled hidden>Selecione a opção&nbsp;</option>
                    <option value="diurno">Diurno</option>
                    <option value="noturno">Noturno</option>
                    <option value="vespertino">Vespertino</option>
                </select>
                <!-- <input placeholder="Turno" name="turno" value=""> -->
            </td>
            <td>
                <select name="status">
                    <option value="" selected disabled hidden>Selecione a opção&nbsp;</option>
                    <option value="em atendimento">Em atendimento</option>
                    <option value="de plantão">De plantão</option>
                    <option value="indisponível">Indisponível</option>
                </select>
                <!-- <input placeholder="Situação" name="status" value=""> -->
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
                        hx-post="/api/medicos" 
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
