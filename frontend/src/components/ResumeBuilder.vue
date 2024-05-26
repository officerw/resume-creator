<!--
  ResumeBuilder

  This contains fields for the user to populate with information that would be
  contained in their resume. This information is compiled into a Javascript
  object and is sent to the TemplateEditor for processing.
-->

<script setup lang="ts">
    import NameContactInfo from "../components/NameContactInfo.vue"


</script>

<template>
    <div class="resume-builder">
        <NameContactInfo/>
    </div>
</template>

<style>
    .resume-builder {
        width: 100%;
        height: fit-content;
    }
</style>
