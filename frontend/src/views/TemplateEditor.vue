<!--
  TemplateEditor

  This page contains the resume builder component and the PDF viewer component.
-->

<script setup lang="ts">
import { ref } from "vue"
import PDFViewer from "../components/PDFViewer.vue"
import ResumeBuilder from "../components/ResumeBuilder.vue"

const pdfURL = ref("/static/default.pdf")

</script>

<template>
    <div class="editor">
        <div id="left-editor">
            <ResumeBuilder @send-pdf-url="(pdfURLStr) => (pdfURL = pdfURLStr)"/>
        </div>

        <div id="right-editor">
            <PDFViewer :pdf-url="pdfURL"/>
        </div>
    </div>
</template>

<style>
    .editor {
        width: 100%;
        padding: 0 2% 0 2%;
        display: flex;
    }

    #left-editor {
        display: block;
        float: left;
        padding: 0.5rem 1rem;
        width: 50%;
        height: 100%;
        background-color: #9dbdd9;
    }

    #right-editor {
        display: block;
        float: right;
        width: 50%;
        background-color: blue;
    }

</style>
