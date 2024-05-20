<!--
*				libreevent - App.vue
*
*	Created by Janis Hutz 05/14/2023, Licensed under the GPL V3 License
*			https://janishutz.com, development@janishutz.com
*
*
-->

<template>
    <div>
        <nav>
            <router-link to="/" class="main-nav-item">Home</router-link> | 
            <router-link to="/about" class="main-nav-item">About</router-link> | 
            <router-link to="/settings" class="main-nav-item">Settings</router-link>
        </nav>
        <router-view v-slot="{ Component, route }" id="main-view">
            <transition :name="route.meta.transition ? String( route.meta.transition ) : 'fade'" mode="out-in">
                <component :is="Component"></component>
            </transition>
        </router-view>
    </div>
</template>

<style>
body {
    background-color: var(--background-color);
}

:root,
:root.light {
    --primary-color: #0a1520;
    --secondary-color: white;
    --background-color: rgb(221, 221, 221);
    --nav-background: white;
    --hover-color: #00457a;
    --popup-color: rgb(224, 224, 224);
    --overlay-color: rgba(0, 0, 0, 0.7);
    --PI: 3.14159265358979;
    --gray-color: rgb(53, 53, 53);
    --footer-background: rgb(233, 233, 233);
    --accent-background: rgb(195, 235, 243);
}

:root.dark {
    --primary-color: white;
    --secondary-color: black;
    --background-color: rgb(32, 32, 32);
    --nav-background: rgb(54, 54, 54);
    --popup-color: rgb(58, 58, 58);
    --hover-color: #007ddd;
    --overlay-color: rgba(104, 104, 104, 0.575);
    --gray-color: rgb(207, 207, 207);
    --footer-background: rgb(53, 53, 53);
    --accent-background: rgb(24, 12, 58);
}

@media (prefers-color-scheme: dark) {
    :root {
        --primary-color: white;
        --secondary-color: black;
        --background-color: rgb(32, 32, 32);
        --nav-background: rgb(54, 54, 54);
        --popup-color: rgb(58, 58, 58);
        --hover-color: #007ddd;
        --overlay-color: rgba(104, 104, 104, 0.575);
        --gray-color: rgb(207, 207, 207);
        --footer-background: rgb(53, 53, 53);
        --accent-background: rgb(24, 12, 58);
    }
}

::selection {
    background-color: #7c8cec;
    color: white;
}

html,
body {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    font-size: 17px;
}

#app {
    transition: 0.5s;
    background-color: var(--background-color);
    font-family: 'Plus Jakarta Sans', sans-serif;
    /* font-family: Avenir, Helvetica, Arial, sans-serif; */
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: var(--primary-color);
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    width: 100vw;
    margin: 0;
}

#main-view {
    min-height: 60vh;
}

.scale-enter-active,
.scale-leave-active {
    transition: all 0.5s ease;
}

.scale-enter-from,
.scale-leave-to {
    opacity: 0;
    transform: scale(0.9);
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.material-symbols-outlined {
    font-variation-settings:
        'FILL' 0,
        'wght' 400,
        'GRAD' 0,
        'opsz' 48
}

.clr-open {
    border: black solid 1px !important;
}
</style>

<style>
    nav {
        height: 10vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .main-nav-item {
        color: black;
    }

    .main-nav-item.router-link-exact-active {
        color: #2080ca;
    }
</style>

<style>
.fancy-button {
    text-decoration: none;
    color: white;
    padding: 20px;
    border-radius: 20px;
    border: none;
    background: linear-gradient(45deg, rgb(0, 33, 139), rgb(151, 0, 0));
    font-size: larger;
    transition: all 0.5s;
    background-size: 150%;
    cursor: pointer;
}

.fancy-button:hover {
    border-radius: 5px;
    background-position: 50%;
}

.fancy-button-inactive {
    background: linear-gradient(45deg, rgba(0, 33, 139, 0.6), rgba(151, 0, 0, 0.6));
    cursor: not-allowed;
}

.fancy-button-inactive:hover {
    border-radius: 20px;
    background-position: 0px;
}
</style>

<script setup lang="ts">
import { RouterView } from 'vue-router';
import { ref } from 'vue';

let isAtTop = ref( true );

if ( window.scrollY === 0 ) {
    isAtTop.value = true;
} else {
    isAtTop.value = false;
}
</script>