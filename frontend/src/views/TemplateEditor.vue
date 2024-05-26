<script setup lang="ts">
import PDFViewer from "../components/PDFViewer.vue"
import ResumeBuilder from "../components/ResumeBuilder.vue"
</script>

<template>
    <div class="main">
        <div id="left-panel">
            <ResumeBuilder/>
        </div>

        <div id="right-panel">
            <PDFViewer/>
        </div>
    </div>
</template>

<style>
    .main {
        width: 100%;
        padding: 0 5% 0 5%;
        height: max-content;
        display: block;
    }

    #left-panel {
        display: inline-block;
        width: 50%;
        height: 100%;
        background-color: green;
    }

    #right-panel {
        display: inline-block;
        width: 50%;
        height: 100%;
        background-color: blue;
    }

</style>
