<template>
    <div class="home">
        <h1>SimpleMediaUpscalerLite</h1>
        <div class="table-container">
            <table>
                <tr id="group1" class="group">
                    <td>
                        <label for="algorithm">Upscaler engine</label><br>
                        <select name="engine" id="engine" v-model="upscaleSettings.engine">
                            <option v-for="engine in engines" :key="engine.id" :value="engine.id">{{ engine.displayName }}</option>
                        </select><br>
                    </td>

                    <td>
                        <label for="algorithm">Upscaling algorithm</label><br>
                        <select name="algorithm" id="algorithm" v-model="upscaleSettings.algorithm">
                            <option v-for="engine in engines[ upscaleSettings.engine ][ 'modes' ]" :key="engine.id" :value="engine.id">{{ engine.displayName }}</option>
                        </select><br>
                    </td>
                </tr>

                <tr id="group2" class="group">
                    <td v-if="engines[ upscaleSettings.engine ][ 'supports' ].includes( 'upscaling' )">
                        <label for="scale">Scale factor</label><br>
                        <input type="number" name="scale" id="scale" v-model="upscaleSettings.scale" min="2" max="4" onkeydown="return false">x<br>
                    </td>

                    <td v-if="engines[ upscaleSettings.engine ][ 'supports' ].includes( 'sharpening' )">
                        <label for="sharpening">Sharpening factor</label><br>
                        <input type="number" step="0.01" name="scale" id="scale" v-model="upscaleSettings.sharpening" min="0" max="1"><br>
                    </td>
                </tr>

                <tr id="group3" class="group">
                    <td>
                        <button @click="runCommand( 'InputFile' )">Input file</button><br>
                        <div v-if="upscaleSettings.InputFile[ 0 ]" id="inputCheck" @mouseenter="showElement( 'inputfile' )" @mouseleave="hideElement( 'inputfile' )">&#10004;</div>
                        <div class="info-container">
                            <div class="info" id="inputfile">
                                {{ upscaleSettings.InputFile[ 0 ] }}
                            </div>
                        </div>
                    </td>
                    <td>
                        <button @click="runCommand( 'OutputFile' )">Output file</button><br>
                        <div v-if="upscaleSettings.OutputFile" id="outputCheck" @mouseenter="showElement( 'outputfile' )" @mouseleave="hideElement( 'outputfile' )">&#10004;</div>
                        <div class="info-container">
                            <div class="info" id="outputfile">
                                {{ upscaleSettings.OutputFile }}
                            </div>
                        </div>
                    </td>
                </tr>
            </table>
            <button @click="start()" id="start">Start upscaling</button>
        </div>

        <div class="output-box-wrapper">
            <p id="cmd" @click="showCmdOutput()">Command output</p>
            <div class="output-box" id="output" v-html="output">
            </div>
        </div>

        <dialog id="processing">
            <div class="dialog-container">
                Your file is being processed. You will be notified when the upscaling process has finished.
                <form method="dialog">
                    <button>OK</button>
                </form>
            </div>
        </dialog>

        <dialog id="wrong">
            <div class="dialog-container">
                Some entries are missing. Please ensure that you have specified an input file!
                <form method="dialog">
                    <button>OK</button>
                </form>
            </div>
        </dialog>

        <dialog id="completed">
            <div class="dialog-container">
                <p style="width: 90%; word-wrap: break-word;">{{ finishMessage }}</p>
                <form method="dialog">
                    <button>OK</button>
                </form>
            </div>
        </dialog>

        <dialog id="error">
            <div class="dialog-container">
                <p style="width: 90%; word-wrap: break-word;">{{ errorMessage }}</p>
                <form method="dialog">
                    <button>OK</button>
                </form>
            </div>
        </dialog>

        <dialog id="fileExtension">
            <div class="dialog-container">
                File extension of input and output file don't match! Please ensure that they are the same.
                Click the button below to fix it.
                <button @click="fixFileExtension();">Fix</button>
                <p v-if="fixed">Fixed!</p>
                <form method="dialog">
                    <button @click="this.fixed = false;">OK</button>
                </form>
            </div>
        </dialog>
    </div>
</template>

<script>
import { ipcRenderer } from 'electron';

export default {
    name: 'HomeView',
    data() {
        return {
            upscaleSettings: { 'engine': 'ffc', 'algorithm': 'fsr', 'scale': 2, 'sharpening': 0, 'InputFile': [], 'OutputFile': '' },
            engines: { 'ffc':{ 'displayName': 'FidelityFX CLI', 'id': 'ffc', 'modes': { 'fsr': { 'displayName': 'FidelityFX Super Resolution', 'id': 'fsr' }, 'c': { 'displayName': 'Cubic', 'id': 'c' }, 'hqc': { 'displayName': 'High Quality Cubic', 'id': 'hqc' } }, 'supports': [ 'upscaling', 'sharpening' ] }, 'ss':{ 'displayName': 'REAL-ESRGAN', 'id': 'ss', 'modes': { 'av3': { 'displayName': 'realesr-animevideov3', 'id': 'av3' }, 'x4plus': { 'displayName': 'realesrgan-x4plus-anime', 'id': 'x4plus' } }, 'supports': [ 'upscaling' ] } },
            fixed: false,
            output: '',
            finishMessage: '',
            errorMessage: '',
        }
    },
    methods: {
        runCommand ( command ) {
            ipcRenderer.send( 'select' + command );
            ipcRenderer.on( 'select' + command, ( event, data ) => {
                if ( command == 'InputFile' ) {
                    this.upscaleSettings[ 'OutputFile' ] = data[ 'data' ][ 0 ].substring( 0, data[ 'data' ][ 0 ].length - 4 ) + '_upscaled' + data[ 'data' ][ 0 ].substring( data[ 'data' ][ 0 ].length - 4 );
                }
                this.upscaleSettings[ command ] = data[ 'data' ];
            } );
        },
        start() {
            this.output = '';
            ipcRenderer.send( 'startUpscaling', JSON.stringify ( this.upscaleSettings ) );
            ipcRenderer.on( 'startUpscaling', ( event, data ) => {
                if ( data.data == 'upscaling' ) {
                    try {
                        document.getElementById( 'processing' ).showModal();
                    } catch ( error ) {
                        console.log( error );
                    }
                } else if ( data.data == 'dataMissing' ) {
                    document.getElementById( 'wrong' ).showModal();
                } else {
                    document.getElementById( 'fileExtension' ).showModal();
                }
            } );

            let self = this;

            ipcRenderer.on( 'progress', function ( evt, message ) {
                self.output += message;
            });

            ipcRenderer.on( 'finish', function ( evt, message ) {
                if ( self.errorMessage == '' ) {
                    self.finishMessage = message;
                    try {
                        document.getElementById( 'processing' ).close();
                        document.getElementById( 'completed' ).showModal();
                    } catch ( error ) {
                        console.log( error );
                    }
                }
            } )

            ipcRenderer.on( 'error', function ( evt, message ) {
                self.errorMessage = message;
                try {
                    document.getElementById( 'processing' ).close();
                    document.getElementById( 'error' ).showModal();
                } catch ( error ) {
                    console.log( error );
                }
            } )
        },
        showCmdOutput () {
            document.getElementById( 'output' ).classList.toggle( 'shown' );
        },
        fixFileExtension () {
            let fileExtension = this.upscaleSettings.InputFile[ 0 ].substring( this.upscaleSettings.InputFile[ 0 ].length - 4 );
            this.upscaleSettings.OutputFile = this.upscaleSettings.OutputFile.slice( 0, this.upscaleSettings.OutputFile[ 0 ].length - 5 ) + fileExtension;
            this.fixed = true;
        },
        showElement( element ) {
            document.getElementById( element ).classList.add( 'shown' );
        },
        hideElement( element ) {
            document.getElementById( element ).classList.remove( 'shown' );
        }
    },
}
</script>

<style scoped>
    .info-container {
        position: relative;
    }

    .info {
        display: none;
        position: absolute;
        background-color: var( --dialog-color );
        padding: 2vw;
        width: 20vw;
        height: 20vh;
        word-wrap: break-word;
    }

    .shown {
        display: block;
    }
    .table-container {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    table {
        border-spacing: 3vw 0;
    }

    #start {
        margin-top: 5vh;
        padding: 1vw 2vw;
        margin-bottom: 0;
        cursor: pointer;
    }

    button {
        background-color: var( --input-color );
        margin-top: 1vw;
        padding: 0.5vw 1vw;
        border-radius: 20px;
        border-style: none;
        cursor: pointer;
        transition: all 0.4s;
    }

    button:hover {
        background-color: #42b983;
    }

    input, select {
        background-color: var( --input-color );
        margin-bottom: 1vw;
        margin-top: 0.3vw;
        padding: 0.5vw 1vw;
        border-radius: 20px;
    }

    .output-box-wrapper {
        margin-top: 3%;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    .output-box {
        display: none;
        overflow-y: scroll;
        overflow-x: hidden;
        word-wrap: normal;
        height: 20vh;
        width: 60%;
        text-align: justify;
		white-space: pre-line;
    }

    .shown {
        display: block;
    }

    dialog {
        border-radius: 10px;
        height: 30vh;
        width: 30vw;
        background-color: var( --background-color );
        border-style: none;
        color: var( --primary-color );
    }

    .dialog-container {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    #cmd {
        text-align: justify;
        width: 60%;
        cursor: pointer;
        user-select: none;
    }
</style>
