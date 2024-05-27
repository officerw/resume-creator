
<script setup lang="ts">
    import { ref } from "vue"

    const sectionTitle = ref("")

    // Delete this section when requested
    const emit = defineEmits(["deleteSection"])

    // Accept whether this section is a list type or experience type
    const props = defineProps({
        sectionType: {
            type: String,
            required: true
        },
        id: {
            type: Number,
            required: true
        }
    })

    // Delete this section
    function deleteSection(idToRemove: number) {
        emit("deleteSection", idToRemove)
    }

</script>

<template>
    <div class="resume-section-instance">
        <h4>Section Title:</h4>
        <button @click="deleteSection(id)">Delete Section</button>
        <textarea id="section-title" v-model="sectionTitle" rows="1" name="sectionTitle" placeholder="Section Title Goes Here" maxlength="30"></textarea>

        <!-- Here, we outline the layout of a list type section -->
        <div v-if="sectionType == 'list'" class="list-section">
            I am a list
        </div>
        <div v-else class="experience-section">
            I am an experience
        </div>
    </div>
</template>

<style>

</style>
