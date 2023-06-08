module.exports = {
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true,
      "appId": "com.janishutz.smuL",
      "copyright": "Copyright (c) 2023 SimpleMediaUpscalerLite contributors",
      "buildVersion": "V2.0.0-dev2",
      builderOptions: {
        files: [
          "**/*",
          {
            from: "./*",
            to: "./*",
            filter: [ "**/*" ]
          }
        ],
        extraFiles: [
          {
            from: "./lib",
            to: "./",
            filter: [ "**/*" ]
          }
        ]
      }
    }
  }
}