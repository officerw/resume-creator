<script setup lang="ts">

const props = defineProps({
    pdfUrl: {
        type: String,
        required: true
    }
})

</script>

<template>
    <div class="pdf-download">
        <a :href="pdfUrl" download><img src="/static/downloadpdf.png" alt="Download PDF"></a>
    </div>
    <div class="pdf">
        <embed id="pdf-embed" :src="pdfUrl" />
    </div>
</template>

<style>
    .pdf-download {
        width: 100%;
        height: 2.5rem;
        background-color: #38383D;
        display: flex;
        justify-content: right;
    }

    .pdf-download img {
        height: 2.5rem;
    }

    .pdf-download a {
        padding: 0 0.5rem;
    }

    .pdf {
        width: 100%;
        height: calc(100% - 2rem);
    }

    #pdf-embed {
        width: 100%;
        height: 100%;
    }
</style>
