<script setup lang="ts">
    import TemplateSelector from "./TemplateSelector.vue"

    // Emit updated selected template
    const emit = defineEmits(["updateTemplate"])

    // Accept info on the PDF URL
    const props = defineProps({
        pdfUrl: {
            type: String,
            required: true
        }
    })

    function updateTemplate(selectedTemplate: string) {
        emit("updateTemplate", selectedTemplate)
    }

</script>

<template>
    <!-- Allow user to download PDF -->
    <div class="pdf-compile-menu">
        <TemplateSelector @update-template="(selectedTemplate: string) => updateTemplate(selectedTemplate)"/>
        <a :href="pdfUrl" download><img src="/static/downloadpdf.png" alt="Download PDF"></a>
    </div>
    <!-- Display pdf when compiled -->
    <div class="pdf">
        <object id="pdf-embed" :data="pdfUrl" width="100%"></object>
    </div>
</template>

<style>
    .pdf-compile-menu {
        width: 100%;
        height: 2.5rem;
        background-color: #38383D;
        display: flex;
        justify-content: space-between;
    }

    .pdf-compile-menu img {
        height: 2.5rem;
    }

    .pdf-compile-menu a {
        padding: 0 0.5rem;
    }

    .pdf {
        width: 100%;
        height: calc(100% - 2.5rem);
    }

    #pdf-embed {
        width: 100%;
        height: 100%;
    }
</style>
