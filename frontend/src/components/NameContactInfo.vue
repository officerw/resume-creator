<script setup lang="ts">
    import { ref, watch } from "vue"

    type NameContactInfo = {
        name: string
        contact_info: Array<ContactInfo>
    }

    type ContactInfo = {
        id: number
        info: string
    }

    const nameContactInfo = defineModel<NameContactInfo>({
        default: {
            name: "",
            contact_info: [{ id: 1, info: "" }]
        },
        required: true
    })

    // Add another field of contact information
    function addContactInfo() {
        // Get current index
        let index = nameContactInfo.value.contact_info[nameContactInfo.value.contact_info.length - 1].id + 1

        nameContactInfo.value.contact_info.push({ id: index, info: "" })
    }

    // Remove field of contact information
    function removeContactInfo() {
        nameContactInfo.value.contact_info.pop()
    }

</script>

<template>
    <div class="name-contact-info-container">
        <h4>Name/Title of Resume:</h4>
        <textarea id="name" v-model="nameContactInfo.name" rows="1" name="Name" placeholder="Name/Title Goes Here" maxlength="50"></textarea>
 
        <!-- Display contact information textarea fields for user to populate -->
        <h4>Contact Information:</h4>
        <ul class="contact-info-list">
            <li v-for="contact in nameContactInfo.contact_info" :key="contact.id">
                <textarea v-model="contact.info" rows="1" name="ContactInfo" v-bind:placeholder="'Contact Information ' + contact.id.toString()" maxlength="50"></textarea>
            </li>
        </ul>

        <!-- The following section allows the user to add and remove contact information fields -->
        <div class="contact-list-buttons">
            <button id="add-button-contact" v-if="nameContactInfo.contact_info.length<6" @click="addContactInfo()"><img class="contact-info-button-img" src="/static/plus.png" alt="+"/></button>
            <button id="remove-button-contact" v-if="nameContactInfo.contact_info.length>1" @click="removeContactInfo()"><img class="contact-info-button-img" src="/static/minus.png" alt="-"/></button>
        </div>

    </div>
</template>

<style>

    .name-contact-info-container h4 {
        font-weight: bold;
    }

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
        overflow:hidden;
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
