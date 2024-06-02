<script setup lang="ts">

const props = defineProps({
    pdfUrl: {
        type: String,
        required: true
    }
})

</script>

<template>
    <div class="pdf">
        <embed :src="pdfUrl" width="100%" height="100%" />
    </div>
</template>

<style>
    .pdf {
        width: 100%;
        height: 100%;
    }
</style>
