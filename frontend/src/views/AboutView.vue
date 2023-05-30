<template>
    <div class="about">
        <img src="@/assets/logo.png">
        <h1>About ImageVideoUpscaler</h1>
        <p>ImageVideoUpscaler is an application that allows you to upscale your videos and / or images. It uses an Electron GUI (Graphical User Interface) and a Python CLI (Command Line Interface).</p>
        <h3>Contributors</h3>
        <ul>
            <li>Janis Hutz (simplePCBuilding): Maintainer, CLI & GUI development, Packaging</li>
            <li>ThatPlasma: App name, Logo, testing, Windows installer</li>
        </ul>
        <div class="version-info">
            <h3>You are currently running version 1.1.0</h3>
            <h3>Changelog</h3>
            <ul>
                <li>
                    Version 1.0
                    <ul></ul>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            version: '',
            isUpToDate: true,
        }
    },
    mounted () {
        fetch( 'https://github.com/simplePCBuilding/ImageVideoUpscaler/blob/master/package.json' ).then( res => {
            console.log( res );
        })
    }
}
</script>
