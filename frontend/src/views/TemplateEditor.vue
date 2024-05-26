<script setup lang="ts">
import PDFViewer from "../components/PDFViewer.vue"
import ResumeBuilder from "../components/ResumeBuilder.vue"
</script>

<template>
    <div class="editor">
        <div id="left-editor">
            <ResumeBuilder/>
        </div>

        <div id="right-editor">
            <PDFViewer/>
        </div>
    </div>
</template>

<style>
    .editor {
        width: 100%;
        padding: 0 5% 0 5%;
        height: 300px;
        display: block;
    }

    #left-editor {
        display: block;
        float: left;
        padding: 0.5rem 1rem;
        width: 50%;
        height: 100%;
        background-color: green;
    }

    #right-editor {
        display: block;
        float: right;
        width: 50%;
        height: 100%;
        background-color: blue;
    }

</style>
