# Problemas no sistema de chat multi-cliente

1. Servidor não verifica se cliente realmente recebeu a mensagem

2. Cliente não tenta reconectar caso perca conexão com servidor; programa simplesmente para

3. Servidor não valida comandos, como por exemplo a troca de nome (deveria verificar se o nome já existe)