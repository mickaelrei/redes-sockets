# Conclusões

### Quais foram os principais desafios ao implementar aplicações com UDP?

 - A falta de uma lógica de tentar novamente em caso de perdas, ou seja, isto teve que ser implementado manualmente, ao contrário do TCP que já resolve isso internamente (portanto, mais rápido do que em python)

 - A necessidade de confirmação do recebimento de pacotes manualmente (novamente, diferente do TCP que faz internamente)

### Como você contornou a falta de garantias de entrega do UDP?

Após o envio de cada fragmento, o cliente esperava um ACK do server com o número correto, simbolizando que o servidor recebeu o fragmento atual e o cliente pode seguir adiante

### Em quais situações você recomendaria o uso de UDP ao invés de TCP?

Em aplicações que muitos pacotes são enviados, mas que não é crítico o recebimento de 100% dos pacotes, ou seja, onde existe tolerância para perdas

### Como o comportamento do UDP poderia impactar aplicações de tempo real?

O protocolo UDP é muito útil para aplicações que transmitem dados constantemente, isto é, em tempo real entre clientes ou entre cliente e servidor. Exemplos são serviços de streaming de vídeo, onde o cliente necessita do recebimento constante de novos frames do vídeo, e um pouco de perda é tolerável