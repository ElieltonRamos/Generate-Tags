<template>
  <div class="min-h-screen flex flex-col items-center bg-gradient-to-b from-gray-100 to-gray-200 text-black">
    <!-- Topo com logo -->
    <header class="w-full py-4 flex items-center justify-center shadow bg-gray-50">
      <img src="/logo.png" alt="Logo Empresa" class="h-12 mr-3" />
      <h1 class="text-2xl font-bold text-gray-900">Gerador de Etiquetas</h1>
    </header>

    <!-- Conteúdo principal -->
    <main class="flex flex-col items-center w-full max-w-3xl p-6">
      <!-- Input PDF -->
      <div class="w-full bg-gray-50 p-6 rounded-2xl shadow-md mt-8 text-center">
        <label class="block mb-4 text-lg font-semibold text-gray-900"> Selecione um arquivo PDF </label>

        <!-- Input escondido -->
        <input ref="fileInput" type="file" accept="application/pdf" class="hidden" @change="handleFileUpload" />

        <!-- Botão customizado -->
        <button
          type="button"
          @click="$refs.fileInput.click()"
          class="px-6 py-3 rounded-xl bg-gradient-to-r from-gray-400 to-gray-500 text-white font-medium shadow hover:shadow-lg hover:from-gray-500 hover:to-gray-600 transition-all duration-300"
        >
          📂 Escolher Arquivo
        </button>

        <!-- Nome do arquivo -->
        <p v-if="selectedFile" class="mt-3 text-sm text-gray-700">
          Arquivo selecionado: <span class="font-medium">{{ selectedFile }}</span>
        </p>
      </div>

      <!-- Formulário Manual -->
      <div class="w-full bg-gray-50 p-6 rounded-2xl shadow-md mt-8">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Criar Etiqueta Manual</h2>
        <form @submit.prevent="adicionarEtiqueta" class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-900">Tipo Pedido</label>
            <input v-model="form.tipoPedido" class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-900">Número Pedido</label>
            <input v-model="form.numeroPedido" class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-900">Filial</label>
            <input v-model="form.filial" class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-900">Data</label>
            <input type="date" v-model="form.data" class="input" />
          </div>
          <div class="col-span-2">
            <label class="block text-sm font-medium text-gray-900">Endereço Entrega</label>
            <input v-model="form.enderecoEntrega" class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-900">Código Produto</label>
            <input v-model="form.codigoProduto" class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-900">Volume</label>
            <input v-model="form.volume" class="input" />
          </div>
          <div class="col-span-2">
            <label class="block text-sm font-medium text-gray-900">Nome</label>
            <input v-model="form.nome" class="input" />
          </div>
          <div class="col-span-2 text-right">
            <button type="submit" class="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700">
              ➕ Adicionar Etiqueta
            </button>
          </div>
        </form>
      </div>

      <!-- Lista de etiquetas -->
      <section class="w-full mt-10">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Etiquetas Geradas</h2>
        <div v-if="etiquetas.length > 0">
          <Etiqueta v-for="(et, index) in etiquetas" :key="index" v-bind="et" @deletar="removerEtiqueta(index)" />
        </div>
        <p v-else class="text-gray-600 text-center">Nenhuma etiqueta gerada ainda.</p>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Etiqueta from './components/Etiqueta.vue';

// Lista de etiquetas
const etiquetas = ref([]);

// Formulário
const form = ref({
  tipoPedido: '',
  numeroPedido: '',
  filial: '',
  data: '',
  enderecoEntrega: '',
  codigoProduto: '',
  volume: '',
  nome: '',
});

const selectedFile = ref('');

function handleFileUpload(event) {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file.name;
    // 🔹 Aqui segue sua lógica de leitura do PDF
  }
}

function adicionarEtiqueta() {
  etiquetas.value.push({ ...form.value });
  // limpa o formulário
  form.value = {
    tipoPedido: '',
    numeroPedido: '',
    filial: '',
    data: '',
    enderecoEntrega: '',
    codigoProduto: '',
    volume: '',
    nome: '',
  };
}

function removerEtiqueta(index) {
  etiquetas.value.splice(index, 1);
}
</script>
