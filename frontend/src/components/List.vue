<script setup lang="ts">
    import { onMounted, ref, watch } from "vue"

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

    // Emit list title and content to parent component
    const emit = defineEmits(["updateListTitle", "updateListContent"])
    // Props to accept imported JSON info
    const props = defineProps({
        content: {
            type: Array<Experience | List>,
            required: true
        },
        id: {
            type: Number,
            required: true
        }
    })

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
    watch(() => props.content, (newContent) => {
        if (newContent != undefined)
            updateListWithJSON(newContent)
    })

    // If the list info has been set by JSON upon mount, set textarea
    // values accordingly
    onMounted(() => {
        if (props.content != undefined)
            updateListWithJSON(props.content)
    })

    // Update textareas upon JSON import
    function updateListWithJSON(newContent: (Experience | List)[]) {
        // Remember that newContent is just the list of all imported content
        // for the section this list is inside
        if (newContent != undefined && props.id <= newContent.length) {
            var newList = newContent[props.id - 1]
            // Type guard newList is in fact a List, not an Experience
            if ("list_title" in newList) {
                list_title.value = newList.list_title
                list_content.value = newList.list_content
            }
        }
    }

</script>

<template>
    <div class="list-container">
        <textarea id="list-title" v-model="list_title" rows="1" name="listTitle" placeholder="List Title" maxlength="50"></textarea>
        <textarea id="list-content" v-model="list_content" rows="1" name="listContent" placeholder="List Content" maxlength="400"></textarea>
    </div>
</template>

<style>

    .list-container {
        padding: 8px;
        margin: 0.5rem;
    }

    #list-content {
        field-sizing: content;
    }

</style>
