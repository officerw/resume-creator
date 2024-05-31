<script setup lang="ts">
    import { ref, watch } from "vue"

    // Emit experience information to parent component
    const emit = defineEmits(["updateListTitle", "updateListContent"])

    // Store list information
    const title = ref("")
    const content = ref("")

    // Whenever values change, emit values to parent component
    watch(title, (newTitle) => {
        emit("updateListTitle", newTitle)
    })

    watch(content, (newContent) => {
        emit("updateListContent", newContent)
    })

</script>

<template>
    <div class="list-container">
        <textarea id="list-title" v-model="title" rows="1" name="listTitle" placeholder="List Title" maxlength="30"></textarea>
        <textarea id="list-content" v-model="content" rows="1" name="listContent" placeholder="List Content" maxlength="120"></textarea>
    </div>
</template>

<style>

    .list-container {
        padding: 8px;
        margin: 0.5rem;
    }

</style>
