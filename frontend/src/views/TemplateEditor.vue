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
    <div class="buffer">
        <div class="left-buffer"></div>
        <div class="right-buffer"></div>
    </div>
</template>

<style>
    .editor {
        width: 100%;
        padding: 0 2% 0 2%;
        height: calc(100% - var(--header-height));
        display: flex;
        justify-content: center;
        flex-direction: var(--flex-direction-editor-sections);
    }

    #left-editor {
        display: block;
        float: left;
        padding: 0.5rem 1rem;
        width: var(--editor-section-width);
        overflow-y: auto;
        height: auto;
        min-height: var(--min-height-editor-sections);
        background-color: #9dbdd9;
    }

    #right-editor {
        display: block;
        float: right;
        width: var(--editor-section-width);
        min-height: var(--min-height-editor-sections);
        background-color: #38383D;
    }

    .left-buffer {
        display: block;
        float: left;
        background-color: #9dbdd9;
        width: var(--editor-section-width);
        height: var(--buffer-height);
    }

    .right-buffer {
        display: block;
        float: right;
        background-color: #2a2a2e;
        width: var(--editor-section-width);
        height: var(--buffer-height);
    }

    .buffer {
        width: 100%;
        padding: 0 2% 0 2%;
        display: flex;
        justify-content: center;
    }

</style>
