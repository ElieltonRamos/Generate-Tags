<template>
  <div class="min-h-screen flex flex-col items-center bg-gradient-to-b from-gray-100 to-gray-200 text-black">
    <!-- Topo com logo -->
    <header class="w-full py-4 flex items-center justify-center shadow bg-gray-50">
      <img src="./assets/logo-rede-norte.png" alt="Logo Empresa" class="h-12 mr-3" />
      <h1 class="text-2xl font-bold text-gray-900">Gerador de Etiquetas</h1>
    </header>

    <!-- Conteúdo principal -->
    <main class="flex flex-col items-center w-full max-w-3xl p-6">
      <!-- Input PDF -->
      <!-- Input PDF refatorado -->
      <div class="w-full bg-gray-50 p-6 rounded-2xl shadow-md mt-8 text-center">
        <label class="block mb-4 text-lg font-semibold text-gray-900">
          Selecione um arquivo PDF
        </label>

        <!-- Botão que chama diretamente a função -->
        <button
          type="button"
          @click="handleFileUpload"
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
            <input v-model="form.tipo_pedido" class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-900">Número Pedido</label>
            <input v-model="form.numero_pedido" class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-900">Filial</label>
            <input v-model="form.filial_pedido" class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-900">Data</label>
            <input type="date" v-model="form.data_pedido" class="input" />
          </div>
          <div class="col-span-2">
            <label class="block text-sm font-medium text-gray-900">Endereço Entrega</label>
            <input v-model="form.endereco_entrega" class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-900">Código Produto</label>
            <input v-model="form.code" class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-900">Volume</label>
            <input v-model="form.vol_ace" class="input" />
          </div>
          <div class="col-span-2">
            <label class="block text-sm font-medium text-gray-900">Nome</label>
            <input v-model="form.description" class="input" />
          </div>
          <div class="col-span-2 text-right">
            <button @click="print" class="px-6 mr-3 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700">
              🖨️ Imprimir Etiquetas
            </button>
            <button type="submit" class="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700">
              ➕ Adicionar Etiqueta
            </button>
          </div>
        </form>
      </div>

      <!-- Lista de etiquetas -->
      <section class="w-full mt-10">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Etiquetas Geradas</h2>
        <div id="invoiceContent" v-if="etiquetas.length > 0">
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
import { invoke } from '@tauri-apps/api/core'
import { open } from '@tauri-apps/plugin-dialog';

const etiquetas = ref([]);

// Formulário
const form = ref({
  tipo_pedido: '',
  numero_pedido: '',
  filial_pedido: '',
  data_pedido: '',
  endereco_entrega: '',
  code: '',
  vol_ace: '',
  description: '',
});

const selectedFile = ref('');

async function handleFileUpload(event) {
  const file = await open({
    multiple: false,
    directory: false,
  });

  try {
    const result = await invoke('process_pdf', { file: file });
    const produtos = JSON.parse(result);

    // Expande volumes se necessário
    const etiquetasComVolumes = [];
    produtos.forEach(p => {
        if (p.vol_ace) {
          let total = parseInt(p.vol_ace.split("/")[1]);
          if (!total || total < 1) {
            total = 1; // fallback
          }
          for (let i = 1; i <= total; i++) {
            etiquetasComVolumes.push({ 
              ...p, 
              vol_ace: `${String(i).padStart(2,'0')}/${String(total).padStart(2,'0')}` 
            });
          }
        } else {
          etiquetasComVolumes.push(p);
        }

    });

    etiquetas.value = etiquetasComVolumes;
  } catch (err) {
    console.error("Erro ao processar PDF:", err);
  }
}

function adicionarEtiqueta() {
  const dados = { ...form.value };

  // Expande volumes se necessário
  const etiquetasComVolumes = [];
  if (dados.vol_ace) {
    const parts = dados.vol_ace.split('/');
    let total = parseInt(parts[1]);
    if (!total || total < 1) total = 1; // fallback
    for (let i = 1; i <= total; i++) {
      etiquetasComVolumes.push({
        ...dados,
        vol_ace: `${String(i).padStart(2, '0')}/${String(total).padStart(2, '0')}`,
      });
    }
  } else {
    etiquetasComVolumes.push(dados);
  }

  // Adiciona à lista global
  etiquetas.value = [...etiquetas.value, ...etiquetasComVolumes];

  // Limpa o formulário
  form.value = {
    tipo_pedido: '',
    numero_pedido: '',
    filial_pedido: '',
    data_pedido: '',
    endereco_entrega: '',
    code: '',
    vol_ace: '',
    description: '',
  };
}


function removerEtiqueta(index) {
  etiquetas.value.splice(index, 1);
}

function print() {
  const content = document.getElementById('invoiceContent')?.innerHTML;
  if (!content) return;

  const iframe = document.createElement('iframe');
  iframe.style.position = 'fixed';
  iframe.style.width = '0';
  iframe.style.height = '0';
  iframe.style.border = '0';
  document.body.appendChild(iframe);

  const doc = iframe.contentWindow?.document;
  if (!doc) return;

  // Importa os estilos do Tailwind do app
  const styles = Array.from(document.styleSheets)
    .map((style) => {
      try {
        return `<link rel="stylesheet" href="${style.href}">`;
      } catch {
        return '';
      }
    })
    .join('');

  doc.open();
  doc.write(`
    <html>
      <head>
        ${styles}
        <style>
          /* Ajustes específicos de impressão */
          @media print {
            body { background: white; width: 100mm; }
            button { display: none; }
            .etiqueta {
              page-break-inside: avoid;
              break-inside: avoid;
            }
          }
        </style>
      </head>
      <body onload="window.print(); setTimeout(() => window.close(), 100);">
        ${content}
      </body>
    </html>
  `);
  doc.close();

  setTimeout(() => document.body.removeChild(iframe), 2000);
}
</script>
