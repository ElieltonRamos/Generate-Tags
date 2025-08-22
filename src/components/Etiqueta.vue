<template>
  <div class="w-full max-w-lg p-4 mb-6 bg-white border border-gray-400 rounded-xl shadow-md text-black">
    <!-- Cabeçalho com logo -->
    <div class="flex items-center justify-between border-b border-gray-400 pb-2 mb-3">
      <div class="flex items-center">
        <img src="../assets/logo-rede-norte.png" alt="Logo Empresa" class="h-10 mr-3" />
        <h2 class="text-lg font-bold">{{ nome }}</h2>
      </div>
      <span class="text-sm">{{ data }}</span>
    </div>

    <!-- Dados principais -->
    <div class="grid grid-cols-2 gap-3 text-sm">
      <div>
        <p><span class="font-semibold">Tipo Pedido:</span> {{ tipoPedido }}</p>
        <p><span class="font-semibold">Número:</span> {{ numeroPedido }}</p>
        <p><span class="font-semibold">Filial:</span> {{ filial }}</p>
      </div>
      <div>
        <p><span class="font-semibold">Volume:</span> {{ volume }}</p>
        <p><span class="font-semibold">Código Produto:</span> {{ codigoProduto }}</p>
      </div>
    </div>

    <!-- Endereço -->
    <div class="mt-3">
      <p class="font-semibold">Endereço de Entrega:</p>
      <p class="text-sm">{{ enderecoEntrega }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  tipoPedido: String,
  numeroPedido: String,
  filial: String,
  data: String,
  enderecoEntrega: String,
  codigoProduto: String,
  volume: String,
  nome: String
})
</script>
