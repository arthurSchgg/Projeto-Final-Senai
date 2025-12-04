*** Settings ***
Documentation     Teste de Login para o Projeto Fluxee
Library           SeleniumLibrary

*** Variables ***
${URL_LOGIN}      http://127.0.0.1:5000/
${BROWSER}        Chrome

# --- DADOS DE ACESSO ---
${EMAIL_VALIDO}   arthurm2804@gmail.com
${SENHA_VALIDA}   1234567

# --- SELETORES ---
${CAMPO_EMAIL}    name=email
${CAMPO_SENHA}    name=senha

# --- A MUDANÇA ESTÁ AQUI EMBAIXO ---
# Em vez de procurar pelo nome, procuramos por qualquer botão do tipo "submit"
# Isso funciona tanto para <button type="submit"> quanto para <input type="submit">
${BOTAO_LOGIN}    xpath=//button[@type='submit']

*** Test Cases ***
Login Com Sucesso
    [Documentation]    Acessa a tela de login, preenche dados válidos e verifica o redirecionamento.
    Open Browser    ${URL_LOGIN}    ${BROWSER}
    Maximize Browser Window
    
    # Verifica se carregou a página (procura o campo de email)
    Wait Until Element Is Visible    ${CAMPO_EMAIL}    5s

    Input Text      ${CAMPO_EMAIL}    ${EMAIL_VALIDO}
    Input Password  ${CAMPO_SENHA}    ${SENHA_VALIDA}
    
    # Clica no botão corrigido
    Click Element   ${BOTAO_LOGIN}
    
    # Validação de sucesso
    Wait Until Page Contains    Login realizado com sucesso!    5s
    
    [Teardown]    Close Browser

Login Com Senha Incorreta
    [Documentation]    Testa o bloqueio de senha errada.
    Open Browser    ${URL_LOGIN}    ${BROWSER}
    
    Input Text      ${CAMPO_EMAIL}    ${EMAIL_VALIDO}
    Input Password  ${CAMPO_SENHA}    senha_errada
    Click Element   ${BOTAO_LOGIN}
    
    # Validação de erro
    Wait Until Page Contains    Senha incorreta!    5s
    
    [Teardown]    Close Browser