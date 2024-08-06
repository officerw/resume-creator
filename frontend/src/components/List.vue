<script setup lang="ts">
    import { onMounted, ref, watch } from "vue"

    type List = {
        id: number
        list_title: string
        list_content: string
    }

    const listInfo = defineModel<List>({
        default: {
            id: 1,
            list_title: "",
            list_content: ""
        },
        required: true
    })

</script>

<template>
    <div class="list-container">
        <textarea id="list-title" v-model="listInfo.list_title" rows="1" name="listTitle" placeholder="List Title" maxlength="75"></textarea>
        <div class="list-content-container">
            <img id="list-hierarchy-icon" src="/static/hierarchy-icon.png">
            <textarea oninput='this.style.height = "";this.style.height = this.scrollHeight + "px"' class="experience-detail-textarea" id="list-content" v-model="listInfo.list_content" rows="1" name="listContent" placeholder="List Content" maxlength="800"></textarea>
        </div>
    </div>
</template>

<style>

    .list-container {
        padding: 8px;
        margin: 0.5rem;
    }

    .list-content-container {
        display: flex;
    }

    #list-hierarchy-icon {
        height: 20px;
        width: 20px;
    }

    #list-title {
        width: 67%;
    }

    #list-content {
        field-sizing: content;
    }

</style>
