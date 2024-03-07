def paciente_html():
    html = f"""
        <table class="form">
            <tr><td colspan="4"><h4>Cadastrar Paciente</h4></td></tr>
            
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
                        <a class="button secondary" hx-get="/api/pacientes"
                            title="Cancelar a alteração"
                            hx-swap="outerHTML" 
                            hx-target="closest table">
                            Cancelar
                        </a>
                        <a class="button" hx-trigger="click" 
                            hx-include="closest tr"
                            hx-post="/api/pacientes" 
                            title="Salvar"
                            hx-swap="outerHTML" 
                            hx-target="closest table">
                            Salvar
                        </a>
                    </div>
                </td>
            </tr>
        </table>
        """
    return html


def medico_html():
    html = f"""
        <table class="form">
            <tr><td colspan="4"><h4>Cadastrar Médico</h4></td></tr>
            <tr trigger="cancel" class="form editing">
                <td><input placeholder="Nome do médico" name="nome" value=""></td>
                <td><input placeholder="CRM do médico" name="crm" value=""></td>
                <td><input placeholder="E-mail do médico" name="email" value=""></td>
                <td><input placeholder="Especialidade" name="especialidade" value=""></td>
                <td>
                    <select name="turno">
                        <option value="" selected disabled hidden>Selecione</option>
                        <option value="diurno">Diurno</option>
                        <option value="noturno">Noturno</option>
                        <option value="vespertino">Vespertino</option>
                    </select>
                    <!-- <input placeholder="Turno" name="turno" value=""> -->
                </td>
                <td>
                    <select name="status">
                        <option value="" selected disabled hidden>Selecione</option>
                        <option value="em atendimento">Em atendimento</option>
                        <option value="de plantão">De plantão</option>
                        <option value="indisponível">Indisponível</option>
                    </select>
                    <!-- <input placeholder="Situação" name="status" value=""> -->
                </td>
                <td class="icon">
                    <div>
                        <a class="button secondary" hx-get="/api/medicos"
                            title="Cancelar a alteração"
                            hx-swap="outerHTML" 
                            hx-target="closest table">
                            Cancelar
                        </a>

                        <a class="button" hx-trigger="click" 
                            hx-include="closest tr"
                            hx-post="/api/medicos" 
                            title="Salvar"
                            hx-target="closest table"
                            hx-swap="outerHTML">
                            Salvar
                        </a>
                    </div>

                    <!--i class="material-symbols-outlined small-icon">undo</!--i>
                    <!-- i class="material-symbols-outlined small-icon">save</!-->

                </td>
            </tr>
        </table>
        """
    return html
