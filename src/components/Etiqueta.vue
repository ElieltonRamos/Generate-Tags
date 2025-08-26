<template>
  <div class="etiqueta relative h-[5cm] w-[10cm] p-1 mb-2 bg-white border border-gray-400 rounded-md shadow text-black text-[10px]">
    <!-- Botão de deletar -->
    <button 
      @click="$emit('deletar')" 
      class="absolute top-1 right-1 text-red-600 hover:text-red-800 text-xs font-bold"
    >
      ✖
    </button>

    <!-- Cabeçalho com logo e descrição -->
    <div class="flex items-center justify-between border-b border-gray-400 pb-1 mb-1">
      <div class="flex items-center">
        <img src="../assets/logo-rede-norte.png" alt="Logo" class="h-11 mr-2" />
        <h2 class="font-bold max-w-[7cm] text-[10px]">
          {{ nome }}
        </h2>
      </div>
      <span class="text-[11px] font-bold">{{ data_pedido }}</span>
    </div>

    <!-- Dados principais -->
    <div class="grid grid-cols-2 gap-1 text-[11px] mb-1">
      <div class="flex flex-col">
        <p class="font-bold"><span>Tipo Pedido:</span> {{ tipo_pedido }}</p>
        <p class="font-bold"><span>Número:</span> {{ numero_pedido }}</p>
        <p class="font-bold"><span>Filial:</span> {{ filial_pedido }}</p>
      </div>
      <div class="flex flex-col">
        <p class="font-bold"><span>Volume:</span> {{ vol_ace }}</p>
        <p class="font-bold"><span>Código:</span> {{ code }}</p>
      </div>
    </div>

    <!-- Endereço -->
    <div class="font-bold text-[10px]">
      <p class="mb-0.5">Endereço:</p>
      <p class="">{{ endereco_entrega }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  tipo_pedido: String,
  numero_pedido: String,
  filial_pedido: String,
  data_pedido: String,
  endereco_entrega: String,
  endereco_entrega_original: String,
  nome: String,
  especificacoes: String,
  descricao: String,
  code: String,
  supplier_code: String,
  ean: String,
  quantity: String,
  vol_ace: String
})
defineEmits(["deletar"])
</script>
