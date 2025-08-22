<template>
  <div class="min-h-screen flex flex-col items-center bg-gradient-to-b from-blue-50 to-blue-100 text-gray-800">
    <!-- Topo com logo -->
    <header class="w-full py-4 flex items-center justify-center shadow bg-white">
      <img src="./assets/logo-rede-norte.png" alt="Logo Empresa" class="h-12 mr-3" />
      <h1 class="text-2xl font-bold text-blue-700">Gerador de Etiquetas</h1>
    </header>

    <!-- Conteúdo principal -->
    <main class="flex flex-col items-center w-full max-w-lg p-6">
      <!-- Input PDF -->
      <div class="w-full bg-white p-6 rounded-2xl shadow-md mt-8 text-center">
        <label class="block mb-4 text-lg font-medium text-blue-700">
          Selecione um arquivo PDF
        </label>
        <input 
          type="file" 
          accept="application/pdf"
          class="block w-full text-sm text-gray-600 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-blue-400"
          @change="handleFileUpload"
        />
      </div>

      <!-- Lista de etiquetas -->
      <section class="w-full mt-10">
        <h2 class="text-xl font-semibold text-blue-700 mb-4">Etiquetas Geradas</h2>
        <div v-if="etiquetas.length > 0">
          <Etiqueta 
            v-for="(et, index) in etiquetas" 
            :key="index"
            v-bind="et"
          />
        </div>
        <p v-else class="text-gray-500 text-center">Nenhuma etiqueta gerada ainda.</p>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Etiqueta from './components/Etiqueta.vue'

const etiquetas = ref([])

function handleFileUpload(event) {
  const file = event.target.files[0]
  if (file) {
    // 🔹 Por enquanto: simulação de etiquetas extraídas
    etiquetas.value = [
      {
        tipoPedido: "PV",
        numeroPedido: "12345",
        filial: "SP-01",
        data: "22/08/2025",
        enderecoEntrega: "Av. Paulista, 1000 - São Paulo/SP",
        codigoProduto: "ABC123",
        volume: "Caixa 1/3",
        nome: "Produto Exemplo"
      },
      {
        tipoPedido: "PV",
        numeroPedido: "12346",
        filial: "SP-02",
        data: "22/08/2025",
        enderecoEntrega: "Rua XV de Novembro, 200 - Curitiba/PR",
        codigoProduto: "XYZ789",
        volume: "Caixa 2/3",
        nome: "Outro Produto"
      }
    ]
  }
}
</script>
