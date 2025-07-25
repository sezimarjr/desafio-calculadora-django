// portal/static/js/calculator.js

const display = document.getElementById("display");
const historyList = document.getElementById("history-list");
let currentInput = "0";
let operator = null;
let previousInput = null;
let waitingForNewInput = false; // Flag para indicar que um novo número deve começar

// Função para adicionar números e o ponto decimal ao display
function appendToDisplay(value) {
  if (waitingForNewInput) {
    // Se estamos esperando novo input, comece uma nova entrada
    currentInput = value;
    waitingForNewInput = false;
    // Atualiza o display com o número anterior, operador e novo número
    display.textContent = `${previousInput} ${operator} ${currentInput}`;
  } else {
    if (currentInput === "0" && value !== ".") {
      currentInput = value;
    } else if (value === "." && currentInput.includes(".")) {
      return; // Evita múltiplos pontos decimais
    } else {
      currentInput += value;
    }
    // Atualiza o display com a expressão completa
    if (operator) {
      display.textContent = `${previousInput} ${operator} ${currentInput}`;
    } else {
      display.textContent = currentInput;
    }
  }
}

function setOperator(op) {
  if (previousInput !== null && operator !== null && !waitingForNewInput) {
    calculate(); // Calcula o resultado da operação anterior antes de aplicar a nova
  }

  // Se não há input atual (primeira operação), usa o input atual como previous
  if (previousInput === null) {
    previousInput = currentInput || "0";
  }

  operator = op;
  waitingForNewInput = true;

  // Atualiza o display para mostrar a expressão até agora
  display.textContent = `${previousInput} ${operator}`;

  // Se já tínhamos uma operação em andamento, mostra o novo operador
  if (!waitingForNewInput && currentInput) {
    display.textContent = `${currentInput} ${operator}`;
    previousInput = currentInput;
    currentInput = "";
  }
}

// Função para limpar o display e resetar a calculadora
function clearDisplay() {
  currentInput = "0";
  operator = null;
  previousInput = null;
  waitingForNewInput = false;
  display.textContent = currentInput;
}

// Função para realizar o cálculo
async function calculate() {
  if (operator === null || previousInput === null) {
    return; // Não há operação completa para calcular
  }

  let result;
  const num1 = parseFloat(previousInput);
  const num2 = parseFloat(currentInput);

  if (isNaN(num1) || isNaN(num2)) {
    display.textContent = "Erro";
    currentInput = "0";
    previousInput = null;
    operator = null;
    waitingForNewInput = false;
    return;
  }

  let operationTypeForBackend; // Variável para mapear o símbolo para o tipo de operação do backend

  switch (operator) {
    case "+":
      result = num1 + num2;
      operationTypeForBackend = "soma";
      break;
    case "-":
      result = num1 - num2;
      operationTypeForBackend = "subtracao";
      break;
    case "×": // Usar o símbolo '×' para multiplicação
      result = num1 * num2;
      operationTypeForBackend = "multiplicacao";
      break;
    case "÷": // Usar o símbolo '÷' para divisão
      if (num2 === 0) {
        display.textContent = "Erro: Divisão por zero";
        currentInput = "0";
        previousInput = null;
        operator = null;
        waitingForNewInput = false;
        return;
      }
      result = num1 / num2;
      operationTypeForBackend = "divisao";
      break;
    case "%": // Lógica para porcentagem (ex: 50 % 100 = 50) ou (100 * 10% = 10)
      result = (num1 * num2) / 100; // Ex: 100 * 10% = 10
      operationTypeForBackend = "porcentagem"; // Pode precisar de um novo tipo no backend
      break;
    case "±": // Lógica para inverter sinal
      result = -num2; // Aplica ao segundo número ou ao resultado atual
      operationTypeForBackend = "inverter_sinal"; // Pode precisar de um novo tipo no backend
      break;
    default:
      display.textContent = "Erro: Operação inválida";
      currentInput = "0";
      previousInput = null;
      operator = null;
      waitingForNewInput = false;
      return;
  }

  display.textContent = result;
  currentInput = result.toString();
  previousInput = null;
  operator = null;
  waitingForNewInput = true; // Pronto para nova operação ou continuar com o resultado

  // Enviar a operação para o backend via AJAX
  // Nota: Para % e ±, o backend pode precisar de ajustes no modelo Operacao
  // Por enquanto, vamos enviar como os tipos existentes ou adicionar novos no modelo se necessário.
  // Apenas salve se for uma operação de cálculo válida (soma, subtracao, multiplicacao, divisao)
  if (
    ["soma", "subtracao", "multiplicacao", "divisao"].includes(
      operationTypeForBackend
    )
  ) {
    await saveOperation(num1, num2, operationTypeForBackend, result);
  }
}

// Função para salvar a operação no backend
async function saveOperation(num1, num2, type, result) {
  try {
    const response = await fetch("/save_operation/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken, // csrfToken é definido no template HTML
      },
      body: JSON.stringify({
        number1: num1,
        number2: num2,
        operation_type: type,
        result: result,
      }),
    });

    if (response.ok) {
      const data = await response.json();
      if (data.success) {
        // Atualiza o histórico na interface
        updateHistory(data.new_operation);
      } else {
        console.error("Erro ao salvar operação:", data.error);
      }
    } else {
      console.error("Erro na requisição HTTP:", response.statusText);
    }
  } catch (error) {
    console.error("Erro de rede ou ao processar requisição:", error);
  }
}

// Função para atualizar o histórico na interface
function updateHistory(operation) {
  const historyItem = document.createElement("div");
  historyItem.classList.add("history-item");

  const operationText = `${operation.number1} ${getOperatorSymbol(
    operation.operation_type
  )} ${operation.number2}`;
  const resultText = `= ${operation.result}`;
  const timeText = new Date(operation.operation_date).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  historyItem.innerHTML = `
        <div class="operation">${operationText}</div>
        <div class="result">${resultText}</div>
        <div class="time">${timeText}</div>
    `;
  historyList.prepend(historyItem); // Adiciona no início para os mais recentes aparecerem primeiro

  // Remove a mensagem de "Nenhuma operação" se ela existir
  const noHistoryMessage = historyList.querySelector(".no-history");
  if (noHistoryMessage) {
    noHistoryMessage.remove();
  }
}

// Função auxiliar para obter o símbolo do operador
function getOperatorSymbol(type) {
  switch (type) {
    case "soma":
      return "+";
    case "subtracao":
      return "-";
    case "multiplicacao":
      return "×";
    case "divisao":
      return "÷";
    case "porcentagem":
      return "%";
    case "inverter_sinal":
      return "±";
    default:
      return "";
  }
}

// Event Listeners para os botões
document.querySelectorAll(".btn-number").forEach((button) => {
  button.addEventListener("click", () => appendToDisplay(button.textContent));
});

document.querySelectorAll(".btn-operator").forEach((button) => {
  button.addEventListener("click", () => setOperator(button.textContent));
});

document.querySelector(".btn-clear").addEventListener("click", clearDisplay);
document.querySelector(".btn-equals").addEventListener("click", calculate);

// Função para limpar o histórico (frontend e backend)
async function clearHistory() {
  if (confirm("Tem certeza que deseja limpar todo o histórico de operações?")) {
    try {
      const response = await fetch("/clear_history/", {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          historyList.innerHTML = `<div class="no-history">Nenhuma operação realizada ainda.</div>`;
        } else {
          console.error("Erro ao limpar histórico:", data.error);
        }
      } else {
        console.error("Erro na requisição HTTP:", response.statusText);
      }
    } catch (error) {
      console.error("Erro de rede ou ao processar requisição:", error);
    }
  }
}

document;
// .querySelector(".clear-history-btn")
// .addEventListener("click", clearHistory);
