<!--
  TemplateEditor

  This page contains the resume builder component and the PDF viewer component.
-->

<script setup lang="ts">
    import { ref } from "vue"
    import PDFViewer from "../components/PDFViewer.vue"
    import ResumeBuilder from "../components/ResumeBuilder.vue"

    // PDF URL for displaying and downloading
    const pdfURL = ref("/static/default.pdf")
    // Chosen template for resume
    const selectedTemplate = ref("template1")

</script>

<template>
    <div class="editor">
        <!-- Allow user to construct resume info and organization -->
        <div id="left-editor">
            <ResumeBuilder :template="selectedTemplate"
                @send-pdf-url="(pdfURLStr) => (pdfURL = pdfURLStr)"/>
        </div>

        <!-- Display PDF based on constructed resume PDF from ResumeBuilder -->
        <div id="right-editor">
            <PDFViewer @update-template="(newSelectedTemplate) => { selectedTemplate = newSelectedTemplate }" 
                :pdf-url="pdfURL"/>
        </div>
    </div>
</template>

<style>
    .editor {
        width: 100%;
        padding: 0 2% 0 2%;
        height: calc(100% - 9rem);
        display: flex;
        justify-content: center;
    }

    #left-editor {
        display: block;
        float: left;
        padding: 0.5rem 1rem;
        width: var(--editor-section-width);
        overflow-y: auto;
        height: auto;
        background-color: #9dbdd9;
    }

    #right-editor {
        display: block;
        float: right;
        width: var(--editor-section-width);
        background-color: #38383D;
    }

</style>
