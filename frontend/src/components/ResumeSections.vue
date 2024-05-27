
<script setup lang="ts">
    import { ref } from "vue"

    const sections = ref([])

    // Add a section based on the type
    function addExperienceSection(type: string) {
        sections.value.push(type)
    }


</script>

<template>
    <div class="resume-sections">
        <h4>Sections</h4>
        <!-- The following section allows the user to add different kinds of sections to the resume builder -->
        <div class="contact-list-buttons">
            <button id="add-experience" @click="addSection("experience")">Add Experience Section</button>
            <button id="add-list" @click="addSection("list")">Add List Section</button>
        </div>

        <!-- List of sections -->
        <div class="sections-list">

        </div>
    </div>
</template>

<style>

</style>
