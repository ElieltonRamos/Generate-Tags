<template>
  <div class="relative w-full max-w-lg p-4 mb-6 bg-white border border-gray-400 rounded-xl shadow-md text-black">
    <!-- Botão de deletar -->
    <button 
      @click="$emit('deletar')" 
      class="absolute top-2 right-2 text-red-600 hover:text-red-800 text-sm font-bold"
    >
      ✖
    </button>

    <!-- Cabeçalho com logo -->
    <div class="flex items-center justify-between border-b border-gray-400 pb-2 mb-3">
      <div class="flex items-center">
        <img src="../assets/logo-rede-norte.png" alt="Logo Empresa" class="h-10 mr-3" />
        <h2 class="font-bold">{{ description }}</h2>
      </div>
      <span class="text-sm">{{ data_pedido }}</span>
    </div>

    <!-- Dados principais -->
    <div class="grid grid-cols-2 gap-3 text-sm">
      <div>
        <p><span class="font-semibold">Tipo Pedido:</span> {{ tipo_pedido }}</p>
        <p><span class="font-semibold">Número:</span> {{ numero_pedido }}</p>
        <p><span class="font-semibold">Filial:</span> {{ filial_pedido }}</p>
      </div>
      <div>
        <p><span class="font-semibold">Volume:</span> {{ vol_ace }}</p>
        <p><span class="font-semibold">Código Produto:</span> {{ code }}</p>
      </div>
    </div>

    <!-- Endereço -->
    <div class="mt-3">
      <p class="font-semibold">Endereço de Entrega:</p>
      <p class="text-sm">{{ endereco_entrega }}</p>
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
