<template>
  <div class="etiqueta relative h-[4cm] w-[10cm] p-2 mb-2 bg-white border border-gray-400 rounded-md shadow text-black text-[10px]">
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
        <img src="../assets/logo-rede-norte.png" alt="Logo" class="h-8 mr-2" />
        <h2 class="font-bold max-w-[7cm] text-[10px]">
          {{ description }}
        </h2>
      </div>
      <span class="text-[10px]">{{ data_pedido }}</span>
    </div>

    <!-- Dados principais -->
    <div class="grid grid-cols-2 gap-1 text-[10px] mb-1">
      <div class="flex flex-col gap-0.5">
        <p><span class="font-semibold">Tipo Pedido:</span> {{ tipo_pedido }}</p>
        <p><span class="font-semibold">Número:</span> {{ numero_pedido }}</p>
        <p><span class="font-semibold">Filial:</span> {{ filial_pedido }}</p>
      </div>
      <div class="flex flex-col gap-0.5">
        <p><span class="font-semibold">Volume:</span> {{ vol_ace }}</p>
        <p><span class="font-semibold">Código:</span> {{ code }}</p>
      </div>
    </div>

    <!-- Endereço -->
    <div class="text-[10px]">
      <p class="font-semibold mb-0.5">Endereço:</p>
      <p class="leading-snug">{{ endereco_entrega }}</p>
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
  code: String,
  vol_ace: String,
  description: String
})

defineEmits(["deletar"])
</script>
