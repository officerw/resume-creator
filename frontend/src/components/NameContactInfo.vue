<script setup lang="ts">
    import { ref, watch } from "vue"

    // Define emit which will send name/contact info to other components
    const emit = defineEmits(["updateName", "updateContacts"])
    // Import JSON name and contact info
    const props = defineProps({
        setName: {
            type: String,
            required: true
        },
        setContacts: {
            type: Array<String>,
            required: true
        }
    })

    // Give each contact information field an index
    let index = 0
    // Make name and contact information reactive
    const name = ref("")
    const contact_info = ref([
        { id: ++index, info: "" }
    ])

    // Add another field of contact information
    function addContactInfo() {
        contact_info.value.push(
            { id: ++index, info: "" }
        )
    }

    // Remove field of contact information
    function removeContactInfo() {
        contact_info.value.pop()
        index -= 1
    }

    // Whenever name changes, emit updated value to parent component
    watch(name, (newName) => {
        emit("updateName", newName)
    })

    // Whenever the name is set by a JSON, set the textarea value accordingly
    watch(() => props.setName, (newSetName) => {
        name.value = newSetName
    })

    // Whenever contact information changes, emit updated value to parent component
    watch(contact_info.value, (newContacts) => {
        emit("updateContacts", newContacts)
    })

    // Whenever the contacts are set by a JSON, set the textareas and contacts
    // list accordingly
    watch(() => props.setContacts, (newSetContacts: String[]) => {
        // Remove all previous info
        while (contact_info.value.length > 1)
            removeContactInfo()

        // Set contact info for the first item
        contact_info.value[0].info = newSetContacts[0].toString()
        // Set remaining items
        for (let i = 1; i < newSetContacts.length; i++) {
            addContactInfo()
            contact_info.value[i].info = newSetContacts[i].toString()
        }
    })

</script>

<template>
    <div class="name-contact-info-container">
        <h4>Name/Title of Resume:</h4>
        <textarea id="name" v-model="name" rows="1" name="Name" placeholder="Name/Title Goes Here" maxlength="50"></textarea>
 
        <!-- Display contact information textarea fields for user to populate -->
        <h4>Contact Information:</h4>
        <ul class="contact-info-list">
            <li v-for="contact in contact_info" :key="contact.id">
                <textarea v-model="contact.info" rows="1" name="ContactInfo" v-bind:placeholder="'Contact Information ' + contact.id.toString()" maxlength="50"></textarea>
            </li>
        </ul>

        <!-- The following section allows the user to add and remove contact information fields -->
        <div class="contact-list-buttons">
            <button id="add-button-contact" v-if="index<6" @click="addContactInfo()"><img class="contact-info-button-img" src="/static/plus.png" alt="+"/></button>
            <button id="remove-button-contact" v-if="index>1" @click="removeContactInfo()"><img class="contact-info-button-img" src="/static/minus.png" alt="-"/></button>
        </div>

    </div>
</template>

<style>
    .name-contact-info-container {
        width: 100%;
        height: 100%;
    }

    .contact-list-buttons {
        display: flex;
    }

    textarea {
        padding: 5px;
        border-radius: 5px;
        width: 100%;
        resize:none;
    }

    .contact-info-button-img {
        width: 1rem;
        height: 1rem;
    }

    .contact-info-list {
        list-style: none;
        padding: 0;
    }

    #name {
        resize:none;
        overflow-x: hidden;
    }

    .contact-list-buttons button {
        display: flex;
        flex-direction:row;
        justify-content: center;
        flex: 1;
        border-radius: 5px;
    }

    
    #add-button-contact {
        background-color: lightgreen;
    }

    #remove-button-contact {
        background-color: lightcoral;
    }
    
</style>
