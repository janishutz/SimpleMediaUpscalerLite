<template>
    <div class="about">
        <h1>Settings</h1>
        <h3>Engines</h3>
    </div>
</template>

<script>
import run_script from '@/background.js'

export default {
    methods: {
        run() {
            run_script( 'ls' )
        }
    }
}
</script>
