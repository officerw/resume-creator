<script setup lang="ts">
    import { ref, watch } from "vue"

    // Emit experience information to parent component
    const emit = defineEmits(["updateListTitle", "updateListContent"])
    const props = defineProps({
        content: {
            type: Array<Experience | List>
        }
    })

    type Experience = {
        experience_title: string
        location: string
        organization: string
        tenure: string
    }

    type List = {
        list_title: string
        list_content: string
    }

    // Store list information
    const list_title = ref("")
    const list_content = ref("")

    // Whenever values change, emit values to parent component
    watch(list_title, (newTitle) => {
        emit("updateListTitle", newTitle)
    })

    watch(list_content, (newContent) => {
        emit("updateListContent", newContent)
    })

    // Whenever the content value set by JSON changes, update
    // textarea content


</script>

<template>
    <div class="list-container">
        <textarea id="list-title" v-model="list_title" rows="1" name="listTitle" placeholder="List Title" maxlength="30"></textarea>
        <textarea id="list-content" v-model="list_content" rows="1" name="listContent" placeholder="List Content" maxlength="120"></textarea>
    </div>
</template>

<style>

    .list-container {
        padding: 8px;
        margin: 0.5rem;
    }

</style>
