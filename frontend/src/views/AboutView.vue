<template>
    <div class="about">
        <img src="@/assets/logo.png">
        <h1>About ImageVideoUpscaler</h1>
        <p>ImageVideoUpscaler is an application that allows you to upscale your videos and / or images. It uses an Electron GUI (Graphical User Interface) and a Python CLI (Command Line Interface).</p>
        <div class="version-info">
            <h3>You are currently running version {{ appVersion }}. {{ versionNotice[ isUpToDate ] }}.</h3>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            versionNotice: { true: '==> up to date', false: '==> New version available' },
            appVersion: 'V2.0.0',
            latestVersion: '',
            isUpToDate: true,
        }
    },
    mounted () {
        fetch( 'https://api.github.com/repos/simplePCBuilding/ImageVideoUpscaler/releases/latest' ).then( res => {
            res.json().then( data => {
                this.latestVersion = data.tag_name;
                if ( data.tag_name != this.appVersion ) {
                    this.isUpToDate = false;
                }
            } );
        } );
    }
}
</script>
