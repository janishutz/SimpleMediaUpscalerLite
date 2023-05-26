<template>
    <nav>
        <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link>
    </nav>
    <router-view v-slot="{ Component, route }">
        <transition :name="route.meta.transition || 'scale'" mode="out-in">
            <component :is="Component" />
        </transition>
    </router-view>
</template>

<script>
export default {
    name: 'app',
    data () {
        return {
            theme: '',
        }
    },
    methods: {
        changeTheme () {
            if ( this.theme === '&#9788;' ) {
                document.documentElement.classList.remove( 'dark' );
                document.documentElement.classList.add( 'light' );
                sessionStorage.setItem( 'theme', '&#9789;' );
                this.theme = '&#9789;';
            } else if ( this.theme === '&#9789;' ) {
                document.documentElement.classList.remove( 'light' );
                document.documentElement.classList.add( 'dark' );
                sessionStorage.setItem( 'theme', '&#9788;' );
                this.theme = '&#9788;';
            }
        }
    },
    created () {
        this.theme = sessionStorage.getItem( 'theme' ) ? sessionStorage.getItem( 'theme' ) : '';
        if ( window.matchMedia( '(prefers-color-scheme: dark)' ).matches || this.theme === '&#9788;' ) {
            document.documentElement.classList.add( 'dark' );
            this.theme = '&#9788;';
        } else {
            document.documentElement.classList.add( 'light' );
            this.theme = '&#9789;';
        }
    }
}
</script>

<style>
:root, :root.light {
    --background-color: rgb(224, 222, 222);
    --foreground-color: #2c3e50;
    --highlight-color: rgb(221, 0, 0);
}

:root.dark {
    --background-color: rgb(34, 34, 34);
    --foreground-color: white;
}

body, html {
    height: 100%;
    width: 100%;
    margin: 0;
    padding: 0;
}

#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    background-color: var( --background-color );
    color: var( --foreground-color );
    width: 100%;
    height: 100%;
}

nav {
    padding: 30px;
}

nav a {
    font-weight: bold;
    color: #2c3e50;
}

nav a.router-link-exact-active {
    color: #42b983;
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
</style>
