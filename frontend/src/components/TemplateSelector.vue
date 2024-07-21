<script setup lang="ts">
    import { ref, watch } from "vue"

    // Update parent component's selected template for compilation
    const emit = defineEmits(["updateTemplate"])
    
    var selectedTemplate = ref("")

    // Templates for the user to select from
    const templates = [
        { templateName: "Template 1" },
        { templateName: "Template 2" },
        { templateName: "Template 3" },
        { templateName: "Template 4" },
        { templateName: "Template 5" }
    ]

    function setTemplate(newTemplate: string) {
        selectedTemplate.value = newTemplate.replace(" ", "").toLowerCase()
    }

    // Watch for selected template change and emit to parent
    watch(selectedTemplate, (newSelectedTemplate) => {
        emit("updateTemplate", newSelectedTemplate)
    })

</script>

<template>
    <div class="template-selector">
        <ul>
            <li v-for="template in templates">
                <button @click="setTemplate(template.templateName)">
                    {{ template.templateName }}
                </button>
            </li>
        </ul>
    </div>
</template>

<style>
    .template-selector {
        margin: 0 5px;
    }

    .template-selector ul {
        list-style: none;
        height: 100%;
        padding: 0;
    }

    .template-selector li {
        display: inline-block;
        height: 100%;
    }

    .template-selector button {
        height: 100%;
        background-color: #4A4A4F;
        border-radius: 0;
        color: white;
        display: flex;
        border: none;
        align-items: center;
        justify-content: center;
        margin: 0 3px;
        font-size: var(--normal-font-size);
        padding: 0 3px;
    }

    .template-selector button:hover {
        background-color: #666667;
        color: white;
    }
</style>
